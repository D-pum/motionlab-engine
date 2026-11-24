"""Align sampled effects to the supplied narration while preserving natural voice pace."""
import json,math
from pathlib import Path
P=Path(__file__).resolve().parent
TARGET=P/'narrated'
MAP=[(0,0),(13.357542,6),(20.714417,11.5),(26.670250,16.5),(38.851292,25),(46.230292,33),(53,39.5),(55.5,42)]
def remap(value,index=0):
 for a,b in zip(MAP,MAP[1:]):
  if value<=b[index]:
   u=max(0,min(1,(value-a[index])/(b[index]-a[index])))
   return a[1-index]+u*(b[1-index]-a[1-index])
 return MAP[-1][1-index]
def clock(t):
 if t<26.670250:return t
 if t<38.851292:return 26.670250+(t-26.670250)/50
 end=26.670250+(38.851292-26.670250)/50
 if t<46.230292:
  u=t-38.851292;return end+.5*u+.25*u*u/(46.230292-38.851292)
 return end+.75*(46.230292-38.851292)+t-46.230292
def main():
 events=[];last=-1;times=[]
 for i in range(555001):
  t=i/10000;n=math.floor(clock(t)*8+1e-8)
  if n==last:continue
  last=n
  if 13.357542<=t<20.714417:continue
  slow=26.670250<=t<38.851292
  events.append(dict(time=t,file='tick.wav' if n%2==0 else 'tick2.wav',duration=.45 if slow else .075,rate=.36 if slow else 1,gain=.055 if t<53 else .22,fade_out=.015,pan=-.12 if n%2==0 else .12))
  times.append(t)
 # Transfer mechanical release and rewind accents to their new visual timings.
 for e in json.loads((P/'sfx_events.json').read_text()):
  if 6<=e['time']<11.5:
   e['time']=remap(e['time'],1)
   e['gain']*=.22
   events.append(e)
 TARGET.mkdir(exist_ok=True)
 (TARGET/'sfx_events.json').write_text(json.dumps(events,indent=2))
 (TARGET/'impulses.json').write_text(json.dumps(times,indent=2))
 plan=json.loads((P/'production-plan.json').read_text())
 plan['duration']=55.5;plan['output']['duration_s']=55.5
 for cue,start in zip(plan['narration_script'],[.298,13.357542,20.714417,26.67025,38.851292,46.230292]):cue['time']=start
 plan['narration_source']='assets/Watch.wav; natural pace retained, voice normalized to -16 LUFS before mixing.'
 plan['timing_map']=[dict(output_s=a,approved_scene_s=b) for a,b in MAP]
 plan['alignment_method']='Six spoken sections aligned using the long pauses in the supplied recording and the supplied exact script.'
 plan['delivery']['review_file']='watch_final_narrated.mp4'
 plan['delivery']['audio']='Supplied Watch.wav with low sampled mechanical effects, speech sidechain ducking and 2.5-second ticking tail.'
 (TARGET/'production-plan.json').write_text(json.dumps(plan,indent=2))
 print(len(times),'narrated impulses, total',len(events),'cues')
if __name__=='__main__':main()
