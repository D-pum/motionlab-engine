"""Generate sample-based watch cues from the stage's exact simulated clock."""
import json,math
from pathlib import Path
P=Path(__file__).resolve().parent
def sim(t):
 if t<16.5:return t
 if t<25:return 16.5+(t-16.5)/50
 if t<33:
  u=t-25;return 16.67+.5*u+u*u/32
 return 22.67+t-33
def main():
 events=[];times=[]
 last=-1
 for i in range(420001):
  t=i/10000
  n=math.floor(sim(t)*8+1e-8)
  if n==last:continue
  last=n
  if 6<=t<11.5:continue
  times.append(t)
  slow=16.5<=t<25
  events.append(dict(time=t,file='tick.wav' if n%2==0 else 'tick2.wav',duration=.45 if slow else .075,rate=.36 if slow else (1 if n%2==0 else .93),gain=.32 if slow else .22,fade_out=.015,pan=(-.15 if n%2==0 else .15)))
 # Sample-derived unspooling rattle; granular time/rate changes make speed audible.
 for i in range(44):
  u=i/43;t=6+.6*u
  events.append(dict(time=t,file='lightclunk1.wav',duration=.09,rate=1+u*4,gain=.12*(1-u*.7),fade_out=.035,pan=math.sin(i)*.5))
 for i in range(22):
  u=i/21
  events.append(dict(time=10.5+u*.8,file='tick2.wav',duration=.12,rate=3-2*u,gain=.12*(1-u*.5),fade_out=.06,pan=.3*math.cos(i)))
 events.append(dict(time=6,file='fan_interval.wav',duration=.8,rate=1.2,end_rate=6,loop=True,gain=.22,fade_in=.01,fade_out=.2))
 events.append(dict(time=10.5,file='watch_rewind.wav',duration=.9,rate=3,end_rate=.7,loop=True,gain=.20,fade_in=.05,fade_out=.2))
 (P/'sfx_events.json').write_text(json.dumps(events,indent=2))
 (P/'impulses.json').write_text(json.dumps(times,indent=2))
 print(len(times),'clock impulses;',len(events),'sample cues')
if __name__=='__main__':main()
