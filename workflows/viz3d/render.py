"""Render and mux the 60 fps master with Chromium WebCodecs and FFmpeg."""
from argparse import ArgumentParser
from base64 import b64decode
from os import environ
from math import isfinite
from uuid import uuid4
from pathlib import Path
from subprocess import BELOW_NORMAL_PRIORITY_CLASS, PIPE, Popen

from playwright.sync_api import sync_playwright

WIDTH, HEIGHT = 1080, 1920
CONFIGURE = """async ([width,height,fps]) => {
    OPENER.resize(width,height);
    const config = {codec:"avc1.64002a",width,height,framerate:fps,bitrate:13500000,
      hardwareAcceleration:"prefer-hardware",latencyMode:"realtime",avc:{format:"annexb"}};
    if (!(await VideoEncoder.isConfigSupported(config)).supported)
      throw new Error("Native H.264 encoding is unavailable.");
    const chunks=[];
    const native={chunks,error:null};
    native.encoder=new VideoEncoder({
      output(chunk){
        const copy=new Uint8Array(chunk.byteLength);
        chunk.copyTo(copy);
        chunks.push(copy);
      },
      error(error){native.error=String(error);}
    });
    native.encoder.configure(config);
    window.nativeCapture=native;
}"""
CAPTURE = """async ([start,first,count,fps]) => {
    const {encoder,chunks}=window.nativeCapture;
    const stage=document.getElementById("stage");
    for(let offset=0;offset<count;offset++){
      const frameIndex=first+offset;
      OPENER.seek(start+frameIndex/fps);
      const frame=new VideoFrame(stage,{timestamp:Math.round(frameIndex*1000000/fps)});
      encoder.encode(frame,{keyFrame:offset===0});
      frame.close();
      while(encoder.encodeQueueSize>10 && !window.nativeCapture.error)
        await new Promise(resolve=>setTimeout(resolve,2));
      if(window.nativeCapture.error)throw new Error(window.nativeCapture.error);
    }
    await encoder.flush();
    if(chunks.length!==count)
      throw new Error("Encoded "+chunks.length+" frames, expected "+count);
    let payload="";
    for(const bytes of chunks)
      for(let i=0;i<bytes.length;i+=16384)
        payload+=String.fromCharCode(...bytes.subarray(i,i+16384));
    chunks.length=0;
    return btoa(payload);
}"""


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("scene", type=Path, help="Production index.html with OPENER.ready, resize and seek")
    parser.add_argument("--audio", required=True, type=Path, help="Finished narration, music and effects mix")
    parser.add_argument("--duration", required=True, type=float, help="Full timeline length in seconds")
    parser.add_argument("--start", type=float, default=0)
    parser.add_argument("--end", type=float)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--width", type=int, default=WIDTH)
    parser.add_argument("--height", type=int, default=HEIGHT)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    fps = args.fps
    if min(args.width, args.height) < 2 or args.width % 2 or args.height % 2:
        parser.error("Choose positive even output dimensions.")
    end = args.duration if args.end is None else args.end
    if not all(map(isfinite, (args.duration, args.start, end))) or not 0 <= args.start < end <= args.duration or fps < 1:
        parser.error("Choose a positive frame rate and a range inside the production timeline.")
    if not args.scene.is_file() or not args.audio.is_file():
        parser.error("The scene and final audio mix must exist.")
    frames = round((end - args.start) * fps)
    if frames < 1:
        parser.error("The requested range is shorter than one frame.")
    pending = args.output.with_name(f"{args.output.stem}.{uuid4().hex}.partial.mp4")
    cached_browser = Path.home() / "AppData/Local/ms-playwright"
    if cached_browser.is_dir():
        environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(cached_browser))
    command = [
        "ffmpeg", "-y", "-loglevel", "error", "-r", str(fps), "-f", "h264", "-i", "-",
        "-ss", str(args.start), "-i", str(args.audio.resolve()), "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", "-t", str(frames / fps), str(pending)
    ]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            channel="chromium", args=["--enable-gpu", "--use-angle=d3d11", "--disable-software-rasterizer"]
        )
        page = browser.new_page(viewport={"width": 540, "height": 960})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(args.scene.resolve().as_uri(), wait_until="load")
        if errors:
            raise RuntimeError("\n".join(errors))
        page.wait_for_function("window.OPENER?.ready", timeout=15000, polling=100)
        page.evaluate(CONFIGURE, [args.width, args.height, fps])
        with Popen(command, stdin=PIPE, creationflags=BELOW_NORMAL_PRIORITY_CLASS) as encoder:
            try:
                batch = 2 * fps
                for first in range(0, frames, batch):
                    if first % (8 * fps) == 0:
                        print(f"Viz3D: {first}/{frames} frames", flush=True)
                    count = min(batch, frames - first)
                    data = page.evaluate(CAPTURE, [args.start, first, count, fps])
                    encoder.stdin.write(b64decode(data))
                    if errors:
                        raise RuntimeError("\n".join(errors))
            finally:
                encoder.stdin.close()
            if encoder.wait() != 0:
                raise RuntimeError("FFmpeg could not mux the native H.264 stream.")
        browser.close()
    pending.replace(args.output)
    print(args.output, flush=True)


if __name__ == "__main__":
    main()
