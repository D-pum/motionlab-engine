"""Inspect six frames, both aspect ratios, and deterministic seeks on the Viz3D stage."""
import argparse,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
def main():
 p=argparse.ArgumentParser();p.add_argument('--landscape',action='store_true');a=p.parse_args()
 w,h=(1920,1080) if a.landscape else (1080,1920);label='landscape' if a.landscape else 'portrait'
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='chromium',args=['--enable-gpu','--use-angle=d3d11','--disable-software-rasterizer'])
  page=b.new_page(viewport={"width":w,"height":h});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto((ROOT/'index.html').as_uri());page.wait_for_function('OPENER.ready')
  page.evaluate('([w,h])=>OPENER.resize(w,h)',[w,h])
  shots=[]
  for i,t in enumerate([.5,6.5,12.,20.,29.,39.5]):
   page.evaluate('(t)=>OPENER.seek(t)',t);path=ROOT/f'{label}-{i}.png';page.locator('#stage').screenshot(path=str(path));shots.append(path)
  hashes=page.evaluate("""()=>{OPENER.seek(20);const a=document.querySelector('canvas').toDataURL();OPENER.seek(4);OPENER.seek(20);return a===document.querySelector('canvas').toDataURL()}""")
  assert hashes and not errors,(hashes,errors)
  # Compose review sheet in the browser. Original frames remain independent.
  data=page.evaluate("""async paths=>{const c=document.createElement('canvas');c.width=900;c.height=Math.round(600*(await (async()=>{const im=new Image();im.src=paths[0];await im.decode();return im.height/im.width})()));const x=c.getContext('2d');for(let i=0;i<paths.length;i++){const im=new Image();im.src=paths[i];await im.decode();x.drawImage(im,(i%3)*300,Math.floor(i/3)*(c.height/2),300,c.height/2)}return c.toDataURL('image/png').split(',')[1]}""",
   ['data:image/png;base64,'+__import__('base64').b64encode(s.read_bytes()).decode() for s in shots])
  import base64
  (ROOT/('contact_sheet_landscape.png' if a.landscape else 'contact_sheet.png')).write_bytes(base64.b64decode(data))
  b.close()
 (ROOT/f'verify_{label}.json').write_text(json.dumps({'dimensions':[w,h],'frames':6,'deterministic_seek':hashes,'page_errors':errors},indent=2))
 print(label,'PASS')
if __name__=='__main__':main()
