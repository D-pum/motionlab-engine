"""Compact tractor. Dimensions in mm, -Y forward (+Z in glTF), +X axle.
The exported GLB is in metres. Animate axle_<position> around its s3d_joint axis.
"""
from pathlib import Path

import sand3d as s3d


def block(name, size, xyz, color):
    part = s3d.at(s3d.box(name, *size), x=xyz[0], y=xyz[1], z=xyz[2])
    s3d.material(part, "painted_metal", color=color)
    return part


def make_wheel(position, x, y, radius):
    width = radius * 0.55
    # Each wheel group has its origin at the centre of its tyre.
    tire = s3d.at(s3d.cylinder(f"tire_{position}", 2 * radius, width), ry=90, x=-width / 2)
    s3d.material(tire, "rubber", color="#24272a")
    side = 1 if x > 0 else -1
    outside = side * width / 2
    hub = s3d.at(s3d.cylinder(f"hub_{position}", radius, 20), ry=90 * side, x=outside)
    s3d.material(hub, "painted_metal", color="#efbe46")
    marker = block(f"marker_{position}", (12, 25, radius / 4),
                   (outside + side * 22, 0, radius / 8), "#533816")
    wheel = s3d.group(f"wheel_{position}", tire, hub, marker)
    return s3d.at(wheel, x=x, y=y, z=radius)


def build():
    chassis = block("chassis", (720, 2050, 230), (0, 0, 410), "#355743")
    hood = block("hood", (680, 1000, 520), (0, -500, 640), "#579452")
    seat = block("seat", (510, 350, 95), (0, 510, 835), "#343737")
    back = block("seat_back", (510, 95, 290), (0, 660, 875), "#343737")
    exhaust = s3d.at(s3d.cylinder("exhaust", 68, 430), x=220, y=-350, z=1160)
    s3d.material(exhaust, "steel", color="#55565a")
    positions = {
        "front_left": (-490, -720, 270), "front_right": (490, -720, 270),
        "rear_left": (-510, 680, 420), "rear_right": (510, 680, 420),
    }
    wheels = {name: make_wheel(name, *xyz) for name, xyz in positions.items()}
    anchors = {name: s3d.Frame(xyz) for name, xyz in positions.items()}
    tractor = s3d.assembly("tractor", chassis, hood, seat, back, exhaust, *wheels.values(), **anchors)
    for name, wheel in wheels.items():
        s3d.joint(f"axle_{name}", wheel, getattr(tractor, name), kind="continuous", axis="+X")
    return tractor


if __name__ == "__main__":
    s3d.empty_scene()
    s3d.export(build(), Path(__file__).with_suffix(".glb"))
