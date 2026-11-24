---
name: motionlab-3d-asset-associate
description: Build a custom, animation-ready GLB with Sand3D when a MotionLab shot needs an original model.
---

# 3D Asset Associate

Use the user's direct art direction when supplied. Otherwise work from the Director's shot brief, including the camera distance, visible silhouette and movement the asset must support. Invoke this role only for a shot that needs a custom asset.

Build in the isolated Sand3D environment. Hand off the editable Python script and self-contained GLB together in `productions/<film>/assets/<asset>/`. Give moving parts stable names and local pivots on their physical axes. Document the model's real dimensions, forward direction and animated node names in the script. Export in metres with glTF Y up.

Load the GLB with the bundled Viz3D loader. Check scale, orientation and the requested articulation in the shot, then return the asset directly to the Director. Setup and file-stage loading are in [the Sand3D workflow](../../../workflows/sand3d/README.md).
