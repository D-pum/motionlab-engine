import argparse,runpy,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--landscape',action='store_true');a=p.parse_args()
sys.argv=[str(a.folder/'verify.py')]+(['--landscape'] if a.landscape else [])
runpy.run_path(sys.argv[0],run_name='__main__')
