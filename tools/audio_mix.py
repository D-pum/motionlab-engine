"""Mix stereo sample cues, mechanical DSP and optional sidechain-prioritized voice."""
import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import wave

import numpy as np

RATE = 48000
LIBRARY = Path(__file__).resolve().parents[1] / "assets" / "sfx"
MASTER = "loudnorm=I=-14:TP=-1.5:LRA=11"

@lru_cache(maxsize=24)
def sample(name):
    path = (LIBRARY / name).resolve()
    if not path.is_relative_to(LIBRARY) or path.suffix.lower() not in {".mp3",".ogg",".wav"}:
        raise ValueError(f"Invalid library file {name}")
    data = subprocess.check_output(["ffmpeg","-v","error","-i",str(path),"-vn","-ar","48000",
                                    "-ac","2","-f","f32le","pipe:1"])
    pcm = np.frombuffer(data,"<f4").reshape(-1,2)
    # Common working level keeps quiet field recordings audible alongside transients.
    rms = np.sqrt(np.mean(pcm**2))
    return pcm * min(12, .21/max(rms,1e-6), .98/max(np.max(np.abs(pcm)),1e-6))

@lru_cache(maxsize=20)
def looped(name):
    pcm = sample(name)
    n = min(len(pcm)//8, round(.035*RATE))
    if n < 2:
        return pcm
    blend = np.linspace(0,1,n,dtype=np.float32)[:,None]
    seam = pcm[-n:]*(1-blend) + pcm[:n]*blend
    return np.concatenate((pcm[n:-n],seam))

def lowpass(data,hz):
    if not 0 < hz <= RATE/2:
        raise ValueError(f"Invalid lowpass frequency {hz}")
    # Parallel prefix form of the one-pole filter y[n]=(1-a)x[n]+a*y[n-1].
    a = math.exp(-2*math.pi*hz/RATE)
    out = data * (1-a)
    shift = 1
    while shift < len(out) and a > 1e-8:
        out[shift:] += a*out[:-shift]
        a *= a
        shift *= 2
    return out

def playback(event,t):
    name = event["file"]
    looping = event.get("loop",False)
    pcm = looped(name) if looping else sample(name)
    start = event.get("rate",1)
    end = event.get("end_rate",start)
    if min(start,end)<=0:
        raise ValueError("Playback rates must be positive")
    index = RATE*(event.get("offset",0)+start*t+.5*(end-start)*t*t/event["duration"])
    if looping:
        index %= len(pcm)
    left = np.floor(index).astype(np.int64)
    fraction = (index-left)[:,None]
    if looping:
        return pcm[left]*(1-fraction)+pcm[(left+1)%len(pcm)]*fraction
    valid = (left>=0)&(left<len(pcm))
    left = np.clip(left,0,len(pcm)-1)
    return valid[:,None]*(pcm[left]*(1-fraction)+pcm[np.minimum(left+1,len(pcm)-1)]*fraction)

def synth(event,t):
    kind=event["type"]
    d=event["duration"]
    u=t/d
    f=event["pitch"]
    noise=np.random.default_rng(event.get("seed",0)).uniform(-1,1,len(t))
    end=event.get("end_pitch",f)
    angle=2*np.pi*(f*t+.5*(end-f)*t*u)
    if kind in {"piston_fire","sub_hit","footstep"}:
        a=2*np.pi*f*(1.4*t-.32*t*u)
        signal=(np.sin(a)+.32*np.sin(2*a)+.18*np.sin(3*a))*np.exp(-5*u)
        signal+=lowpass(noise,1700)*np.exp(-12*u)*.70
    elif kind in {"inverter","whine","alarm","chime","riser"}:
        if kind=="alarm":
            angle+=4*np.sin(2*np.pi*5*t)
        if kind=="riser":
            angle+=2*np.pi*f*t*u
        signal=(.65*np.sin(angle)+.23*np.sin(2*angle)+.12*np.sin(4*angle+.3))
        signal=signal*(.93+.07*np.sin(31*t))+.16*lowpass(noise,2100)
        if kind=="chime":
            signal*=np.exp(-4*u)
        if kind=="riser":
            signal*=u
    elif kind=="tick":
        signal=(noise+.2*np.sin(angle*3))*np.exp(-20*u)
    else:
        raise ValueError(f"Unknown effect {kind}")
    return np.column_stack((signal,signal))

def mix(folder,duration,voice=None):
    track=np.zeros((round(duration*RATE),2),np.float32)
    for e in json.loads((folder/"sfx_events.json").read_text(encoding="utf-8-sig")):
        start=round(e["time"]*RATE)
        if start<0 or e["duration"]<=0:
            raise ValueError("Invalid cue timing")
        dest=track[start:start+round(e["duration"]*RATE)]
        if not len(dest):
            continue
        t=np.arange(len(dest))/RATE
        audio=playback(e,t) if "file" in e else synth(e,t)
        if "lowpass" in e:
            audio=lowpass(audio,e["lowpass"])
        fades=np.minimum(1,t/max(1/RATE,e.get("fade_in",.001)))
        fades*=np.minimum(1,(e["duration"]-t)/max(1/RATE,e.get("fade_out",.004)))
        pan=e.get("pan",0)
        dest+=audio*(fades*e["gain"])[:,None]*np.sqrt([1-max(0,pan),1+min(0,pan)])
    with tempfile.TemporaryDirectory(dir=folder) as tmp:
        fx=Path(tmp)/"effects.wav"
        with wave.open(str(fx),"wb") as out:
            out.setparams((2,2,RATE,0,"NONE",""))
            out.writeframes((track*(29490/max(1,np.abs(track).max()))).astype("<i2").tobytes())
        inputs=["ffmpeg","-hide_banner","-nostats","-y","-i",str(fx)]
        graph="[0:a]"
        if voice:
            inputs+=["-i",str(voice)]
            graph=("[1:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=65,"
                   "apad,atrim=end_sample="+str(len(track))+",asplit[v][key];"
                   "[0:a]volume=0.65[fx];[fx][key]sidechaincompress=threshold=0.025:"
                   "ratio=7:attack=8:release=220[duck];[duck][v]amix=inputs=2:normalize=0,")
        measure=subprocess.run(inputs+["-filter_complex",graph+MASTER+":print_format=json",
                           "-f","null","-"],capture_output=True,text=True,check=True)
        stats=json.loads(re.findall(r'\{[^{}]+\}',measure.stderr)[-1])
        params=dict(measured_I="input_i",measured_TP="input_tp",measured_LRA="input_lra",
                    measured_thresh="input_thresh",offset="target_offset")
        norm=MASTER
        if all(math.isfinite(float(stats[k])) for k in params.values()):
            norm+=":linear=true"+"".join(f":{key}={stats[val]}" for key,val in params.items())
        output=Path(tmp)/"master.wav"
        subprocess.run(inputs+["-v","error","-filter_complex",graph+norm+",aresample=48000,apad,atrim=end_sample="+str(len(track)),
                               "-c:a","pcm_s24le",str(output)],check=True)
        # Gated mechanical pulses can miss the target in dynamic loudnorm mode.
        # Measure the actual PCM and leave headroom for AAC reconstruction peaks.
        for attempt in range(3):
            check=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",str(output),
                "-af",MASTER+":print_format=json","-f","null","-"],
                capture_output=True,text=True,check=True)
            reading=json.loads(re.findall(r'\{[^{}]+\}',check.stderr)[-1])
            error=-14-float(reading["input_i"])
            if not math.isfinite(error) or (abs(error)<.09 and float(reading["input_tp"])<=-1.95):
                break
            adjusted=Path(tmp)/f"trim{attempt}.wav"
            subprocess.run(["ffmpeg","-v","error","-i",str(output),"-af",
                f"volume={error}dB,aresample=192000,alimiter=limit=0.79:level=0:latency=1,aresample=48000,apad,atrim=end_sample={len(track)}",
                "-c:a","pcm_s24le",str(adjusted)],check=True)
            output=adjusted
        output.replace(folder/"audio_mix.wav")

def packets(path):
    result=subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_packets",
        "-show_entries","packet=pts,dts,duration,data_hash","-show_data_hash","sha256","-of","csv=p=0",str(path)])
    if not result.strip():
        raise ValueError(f"No video packets in {path}")
    return hashlib.sha256(result).hexdigest()

def remux(folder, destination=None):
    original=folder/"preview_sfx.mp4"
    expected=packets(original)
    with tempfile.TemporaryDirectory(dir=folder) as tmp:
        output=Path(tmp)/"remux.mp4"
        subprocess.run(["ffmpeg","-v","error","-i",str(original),"-i",str(folder/"audio_mix.wav"),
            "-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000",
            "-af","apad=pad_dur=0.002","-shortest","-movflags","+faststart",str(output)],check=True)
        if packets(output)!=expected:
            raise RuntimeError("Remux changed video packet data or timing")
        output.replace(destination or original)
    print(f"{folder.name}: video packet and timing hash verified {expected}",flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("folder",type=Path)
    p.add_argument("--duration",type=float)
    p.add_argument("--voice",type=Path)
    p.add_argument("--remux",action="store_true")
    p.add_argument("--output",type=Path,help="Write a separate remuxed MP4, preserving preview_sfx.mp4")
    a=p.parse_args()
    duration=a.duration if a.duration is not None else json.loads((a.folder/"production-plan.json").read_text(encoding="utf8"))["duration"]
    mix(a.folder,duration,a.voice)
    if a.remux or a.output:
        remux(a.folder,a.output)
