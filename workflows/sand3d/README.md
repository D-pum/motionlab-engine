# Custom GLB assets for Viz3D

The [3D Asset Associate](../../.agents/skills/motionlab-3d-asset-associate/SKILL.md) builds an asset when a shot calls for it. The production stage uses the exported model with the existing `Viz3D.GLTFLoader`. Sand3D runs only at authoring time.

## Install on Windows x64

The tested pair is Sand3D 1.6.3 and Blender's Python module bpy 5.2.4, using CPython 3.13.18. The pins are in this directory's requirements file. [Sand3D v1.6.3 source and API](https://github.com/Sandflow-ai/sand3d/tree/v1.6.3).

From the checkout root, with Python 3.13 installed:

```powershell
py -3.13 -m venv tools/sand3d/.venv
tools/sand3d/.venv/Scripts/python.exe -m pip install -r workflows/sand3d/requirements.txt
```

Alternatively, with uv available, keep the managed interpreter, cache and environment inside the ignored tools directory:

```powershell
$env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD 'tools/sand3d/python'
$env:UV_CACHE_DIR = Join-Path $PWD 'tools/sand3d/cache'
uv venv --managed-python --python 3.13.18 tools/sand3d/.venv
uv pip install --python tools/sand3d/.venv/Scripts/python.exe -r workflows/sand3d/requirements.txt
```

## Load an asset on the file stage

Keep the editable model script and its binary GLB in the shot's production asset folder. Chromium blocks relative file fetches from the renderer's `file://` stage. After each export, package the exact GLB bytes as a classic script alongside the model. This step uses the Python standard library and can run from the renderer environment.

```powershell
tools/sand3d/.venv/Scripts/python.exe productions/FILM/assets/tractor/tractor.py
.venv/Scripts/python.exe workflows/sand3d/embed_glb.py productions/FILM/assets/tractor/tractor.glb
```

Load the generated script after `viz3d.js`. Give each asset script its own element ID. In the stage's async setup, add the loaded scene and resolve the named animation nodes before setting `OPENER.ready` to true.

```html
<script id="tractor-glb" src="assets/tractor/tractor.glb.js"></script>
```

```js
const url = document.getElementById("tractor-glb").dataset.url;
const { scene: tractor } = await new Viz3D.GLTFLoader().loadAsync(url);
scene.add(tractor);
const axle = tractor.getObjectByName("axle_rear_right");
const axis = new Viz3D.THREE.Vector3().fromArray(axle.userData.s3d_joint.axis).normalize();
const rest = axle.quaternion.clone();
// Inside OPENER.seek(seconds), use the shot's absolute wheel angle in radians.
axle.quaternion.copy(rest);
axle.rotateOnAxis(axis, angle);
```

A stage already served over HTTP can pass the relative GLB URL directly to the same loader.

## Tractor integration test

Run from the checkout root. Use a fresh ignored production folder. The test builds four named wheels and checks the rear-right wheel's quarter-turn and return to rest, the axle centre, chassis dimensions and the three stationary wheels. The stage becomes ready only after those checks pass. The normal master renderer then exports one frame at the quarter-turn.

```powershell
$test = 'productions/_sand3d-tractor-check'
New-Item -ItemType Directory -Path "$test/assets/tractor" -Force | Out-Null
Copy-Item workflows/sand3d/tests/tractor.py "$test/assets/tractor/"
Copy-Item workflows/sand3d/tests/stage.html "$test/index.html"
tools/sand3d/.venv/Scripts/python.exe "$test/assets/tractor/tractor.py"
.venv/Scripts/python.exe workflows/sand3d/embed_glb.py "$test/assets/tractor/tractor.glb"
ffmpeg -v error -y -f lavfi -i anullsrc=r=48000:cl=mono -t 1 "$test/silence.wav"
.venv/Scripts/python.exe workflows/viz3d/render.py "$test/index.html" --audio "$test/silence.wav" --duration 1 --start 0.5 --end 0.516666666667 --fps 60 --output "$test/frame.mp4"
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=codec_name,width,height,nb_read_frames "$test/frame.mp4"
```
