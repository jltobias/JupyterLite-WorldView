"""Execute every lab in an isolated temporary directory; save visible outputs."""
from pathlib import Path
import argparse
import shutil
import tempfile
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true',help='Update committed notebook outputs')
    args=parser.parse_args()
    for source in sorted((ROOT/'content').glob('*.ipynb')):
        with tempfile.TemporaryDirectory(prefix='worldview-lab-') as tmp:
            work=Path(tmp);shutil.copy(ROOT/'content/worldview_lab.py',work)
            shutil.copytree(ROOT/'content/data',work/'data')
            nb=nbformat.read(source,as_version=4);nbformat.validate(nb)
            NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(work)}}).execute()
            if args.write:nbformat.write(nb,source)
            print('PASS',source.name,flush=True)

if __name__=='__main__':main()
