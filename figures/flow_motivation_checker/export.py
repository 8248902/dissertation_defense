#!/usr/bin/env python3
"""Reference / ground truth / structure-tensor voxel estimate, as quiver and color-wheel panels.

Scene: v2e-simulated checkerboard rectangle (60 x 40 px) translating diagonally at 3 px per window,
window 22 -- the scene and window of thesis Fig. ch3_quiver_v2e (bottom row) and of the deck's
structure-tensor quiver slide. Run: ch3q_v2e_checker, trial0002 vox_struct, alpha_smooth = 20 (job 1464569,
code 5193805). AEE at this window: 0.983 px (vox_struct_mean_aee, frame_idx 22 of the per-window stats CSV).

No solver is run. Every panel is a crop of a PNG the harness saved:
  - quiver panels: the deck's figures/ch3_quivers_consistent/v2e_checker_f0022/crop/{gt,vox_struct}.png
    (same crop box and arrow scale as the slide that already shows them);
  - color panels and reference: the trial's flow/flow_{gt,vox_struct}_0022.png and gray/gray_0022.png,
    cropped with the same box (thesis figures/ch3_quivers_consistent/crop.py BOX).
The color panels come from ev_flow.utils.analyze_vox.flow_to_color written with cv2.imwrite, which treats
the RGB array as BGR. The legend wheel is generated through exactly that path, so it matches the panels.
Brightness is per panel: magnitude / that panel's 95th-percentile magnitude; black = zero flow.

Run from the optical-flow repo root's Python environment:
  python3 figures/flow_motivation_checker/export.py
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DECK = HERE.parents[1]
REPO = Path("/home/dblauvel/g/r/custom_event_based_optical_flow")
sys.path.insert(0, str(REPO / "src"))
from ev_flow.utils.analyze_vox import flow_to_color  # noqa: E402

TRIAL = Path("/projects/hantil/neuromorphic/vision/dblauvel/dblauvel/optflow_experiments/ch3q_v2e_checker/"
             "v2e_highres_dt1_rectangle_diagonal_checker_v3.0/trial0002_rectangle_diagonal_checker_v3.0_vox_struct_alpha20")
DIAG = TRIAL / "alpha_20.0_dt1_diag_v2"
QUIV = DECK / "figures/ch3_quivers_consistent/v2e_checker_f0022/crop"
BOX = (40, 55, 250, 213)  # thesis figures/ch3_quivers_consistent/crop.py
FRAME = 22


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def wheel(path: Path, n: int = 241) -> None:
    """Legend through the same flow_to_color -> cv2.imwrite path; image y points down."""
    r = np.linspace(-1, 1, n, dtype=np.float32)
    u, v = np.meshgrid(r, r)
    rgb = flow_to_color(np.stack([u, v], -1), max_mag=1.0)
    tmp = path.with_suffix(".tmp.png")
    cv2.imwrite(str(tmp), rgb)  # identical channel handling to the harness
    img = np.asarray(Image.open(tmp).convert("RGB")).copy()
    tmp.unlink()
    img[u ** 2 + v ** 2 > 1] = 255
    Image.fromarray(img).save(path)


def main() -> None:
    sources = {
        "reference.png": DIAG / f"gray/gray_{FRAME:04d}.png",
        "gt_color.png": DIAG / f"flow/flow_gt_{FRAME:04d}.png",
        "ours_color.png": DIAG / f"flow/flow_vox_struct_{FRAME:04d}.png",
    }
    for name, src in sources.items():
        Image.open(src).convert("RGB").crop(BOX).save(HERE / name)
    shutil.copyfile(QUIV / "gt.png", HERE / "gt_quiver.png")
    shutil.copyfile(QUIV / "vox_struct.png", HERE / "ours_quiver.png")
    sources["gt_quiver.png"] = QUIV / "gt.png"
    sources["ours_quiver.png"] = QUIV / "vox_struct.png"
    wheel(HERE / "wheel.png")

    stats = pd.read_csv(TRIAL / "vox_struct_wi1_l2_jacobi_alpha_20.0_dt1_stats.csv").set_index("frame_idx").loc[FRAME]
    aee, ang = float(stats["vox_struct_mean_aee"]), float(stats["vox_struct_mean_ang"])

    # Preview: rows = quiver, color; columns = reference, ground truth, ours.
    w, h = BOX[2] - BOX[0], BOX[3] - BOX[1]
    pad, top = 8, 18
    sheet = Image.new("RGB", (3 * w + 4 * pad + 90, 2 * (h + top) + 3 * pad), "white")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.load_default()
    grid = [["reference.png", "gt_quiver.png", "ours_quiver.png"], ["reference.png", "gt_color.png", "ours_color.png"]]
    heads = ["Reference", "Ground truth", f"Ours (AEE {aee:.2f} px)"]
    for i, row in enumerate(grid):
        for j, name in enumerate(row):
            x, y = pad + j * (w + pad), pad + i * (h + top + pad)
            d.text((x, y), heads[j], fill="black", font=f)
            sheet.paste(Image.open(HERE / name), (x, y + top))
    sheet.paste(Image.open(HERE / "wheel.png").resize((80, 80)), (3 * (w + pad) + pad, pad + h + top + pad + top + 20))
    sheet.save(HERE / "preview.png")

    meta = {
        "scene": "v2e checkerboard rectangle 60x40 px, diagonal translation 3 px/window",
        "window": FRAME,
        "method": "vox_struct (structure-tensor voxel), alpha_smooth = 20, no pyramid",
        "run": str(TRIAL), "slurm_job": 1464569, "code_commit": "5193805",
        "aee_px": round(aee, 3), "angular_error_deg": round(ang, 2),
        "context_aee_px_same_window": {"vox": 2.371, "vox_cont": 2.088, "vox_aniso_tensor": 1.193, "cmax": 0.317,
                                       "ts_and_zero_flow": 3.0,
                                       "source": "thesis shared_bodies/ch3_eb_hs_of_body.tex source comments (manifest.tsv)"},
        "crop_box_px": BOX,
        "color_rule": "flow_to_color (hue = direction, value = magnitude / panel p95), saved via cv2.imwrite; "
                      "wheel.png generated through the same path; black = zero flow",
        "sources": {k: str(v) for k, v in sources.items()},
        "sha256": {p.name: sha(p) for p in sorted(HERE.glob("*.png"))},
        "exporter": "drafts/dissertation_defense/figures/flow_motivation_checker/export.py",
    }
    (HERE / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({k: meta[k] for k in ("aee_px", "angular_error_deg")}))


if __name__ == "__main__":
    main()
