"""Cross-platform build. Publishes only an explicit list of public artifacts."""
from pathlib import Path
import shutil
import subprocess
import sys
import json
from importlib.metadata import distribution

ROOT=Path(__file__).resolve().parents[1]

def main():
    # Resolve before cleaning: never remove a path outside this checkout.
    dist=(ROOT/'dist').resolve()
    if dist.parent!=ROOT.resolve() or dist.name!='dist':raise RuntimeError('Unexpected output directory')
    if dist.exists():shutil.rmtree(dist)
    dist.mkdir()
    book_output=(ROOT/'book/_build').resolve()
    if book_output.parent!=(ROOT/'book').resolve() or book_output.name!='_build':raise RuntimeError('Unexpected book output directory')
    if book_output.exists():shutil.rmtree(book_output)
    labs=ROOT/'book/labs';labs.mkdir(exist_ok=True)
    for notebook in (ROOT/'content').glob('*.ipynb'):shutil.copy2(notebook,labs/notebook.name)
    static=ROOT/'book/_static/generated';static.mkdir(parents=True,exist_ok=True)
    for asset in (ROOT/'assets').glob('*'):
        if asset.suffix in ['.svg','.png']:shutil.copy2(asset,static/asset.name)
    # pip --user on Windows can put extension assets outside sys.prefix.
    kernel_dist=distribution('jupyterlite-pyodide-kernel')
    package=next(kernel_dist.locate_file(f).resolve() for f in kernel_dist.files
                 if str(f).replace('\\','/').endswith('pyodide-kernel-extension/package.json'))
    extra=[]
    if package.parents[2] != (Path(sys.prefix)/'share/jupyter/labextensions').resolve():
        extra=['--LiteBuildConfig.federated_extensions='+json.dumps([package.parent.as_posix()])]
    subprocess.run([sys.executable,'-c','from jupyterlite_core.app import main; main()','build','--contents','content','--output-dir',str(dist/'lab'),*extra],cwd=ROOT,check=True)
    config=json.loads((dist/'lab/jupyter-lite.json').read_text(encoding='utf-8'))
    extensions=config['jupyter-config-data']['federated_extensions']
    if not any(e['name']=='@jupyterlite/pyodide-kernel-extension' for e in extensions):
        raise RuntimeError('Build omitted the Python kernel extension')
    # Lite 0.6's root redirect drops/mishandles query strings. Keep existing
    # public /lab/index.html?path=... links working, including on Pages subpaths.
    (dist/'lab/index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<title>Open WorldView notebooks</title><script id="jupyter-config-data" type="application/json" data-jupyter-lite-root=".">{}</script>
<script>location.replace('lab/index.html'+location.search+location.hash);</script>
<a href="lab/index.html">Open JupyterLite Lab</a></html>''',encoding='utf-8')
    subprocess.run([sys.executable,'-c','from jupyter_book.cli.main import main; main()','build','book','--warningiserror','--keep-going'],cwd=ROOT,check=True)
    shutil.copytree(ROOT/'book/_build/html',dist/'book')
    for directory in ['dashboard','scenes','assets','licenses']:shutil.copytree(ROOT/directory,dist/directory)
    shutil.copytree(ROOT/'content/data',dist/'data')
    for name in ['index.html','LICENSE','THIRD_PARTY_NOTICES.md','CITATION.cff']:shutil.copy2(ROOT/name,dist/name)
    (dist/'.nojekyll').touch()
    print('Built site:',dist)

if __name__=='__main__':main()
