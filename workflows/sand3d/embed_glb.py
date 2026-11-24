"""Package a self-contained GLB as a classic script for Viz3D's file:// stage."""
import argparse
import base64
from pathlib import Path


def embed_glb(model: Path) -> Path:
    data = model.read_bytes()
    if data[:8] != b"glTF\x02\x00\x00\x00" or int.from_bytes(data[8:12], "little") != len(data):
        raise ValueError(f"Expected a complete glTF 2.0 binary file: {model}")
    script = model.with_suffix(".glb.js")
    payload = base64.b64encode(data).decode("ascii")
    script.write_text(
        f'document.currentScript.dataset.url = "data:model/gltf-binary;base64,{payload}";\n',
        encoding="ascii",
    )
    return script


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    print(embed_glb(parser.parse_args().model))
