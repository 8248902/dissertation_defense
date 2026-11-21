#!/usr/bin/env python3
"""Real-data flow panels for the defense motivation slide: MVSEC reference / ground truth / vox estimate.

Input: one window saved by custom_event_based_optical_flow/scripts/analysis/defense_flow_example.py
(solver and alpha recorded in the window's meta.json; 50 Jacobi iterations, EV-FlowNet protocol,
dt = one APS frame), i.e. real float fields, not re-decoded renders.

  python3 export.py /scratch/dblauvel/defense_flow_example_20261120/vox_indoor_flying2/window_XXXX.npz

Rendering (both panels of a kind use the same rule):
  - region: GT-valid pixels (finite, nonzero GT); outside it is white (color) or arrow-free (quiver);
  - color: hue = direction (image y down), brightness = |flow| / P, black = zero, white = no GT;
    wheel.png is drawn by the same function;
  - quiver: stride STRIDE px, cell-averaged, arrow length = |flow| / P * STRIDE * 0.9;
  - *_color_masked.png: color only at pixels that received events in the window (no dilation), white
    elsewhere, pale style (hue = direction, saturation = |flow| / P), legend wheel_masked.png;
  - display region: GT-valid pixels plus holes up to HOLE px, GT filled from the nearest valid pixel;
  - P = the GT's 95th-percentile |flow|, shared by GT and estimate panels (same scale).
"""
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb
from scipy.ndimage import binary_closing, distance_transform_edt

HERE = Path(__file__).resolve().parent
if len(sys.argv) > 2:
    HERE = Path(sys.argv[2]); HERE.mkdir(parents=True, exist_ok=True)
STRIDE = 14
HOLE = 5


def color(u, v, region, p95):
    ang = (np.arctan2(v, u) % (2 * np.pi)) / (2 * np.pi)
    val = np.clip(np.hypot(u, v) / p95, 0, 1)
    rgb = hsv_to_rgb(np.stack([ang, np.ones_like(ang), val], -1))
    rgb[~region] = 1.0
    return rgb


def color_pale(u, v, region, p95):
    ang = (np.arctan2(v, u) % (2 * np.pi)) / (2 * np.pi)
    sat = np.clip(np.hypot(u, v) / p95, 0, 1)
    rgb = hsv_to_rgb(np.stack([ang, sat, np.ones_like(ang)], -1))
    rgb[~region] = 1.0
    return rgb


def color_pale_wheel(path, n=301):
    r = np.linspace(-1, 1, n)
    u, v = np.meshgrid(r, r)
    rgb = color_pale(u, v, u ** 2 + v ** 2 <= 1, 1.0)
    fig = plt.figure(figsize=(1.2, 1.2), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.imshow(rgb, extent=(-1, 1, 1, -1))
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, lw=0.6, color="0.6"))
    fig.savefig(path, dpi=300, transparent=True); plt.close(fig)


def save_img(arr, path):
    h, w = arr.shape[:2]
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.imshow(arr, cmap="gray" if arr.ndim == 2 else None, vmin=0, vmax=255 if arr.ndim == 2 else 1,
              interpolation="nearest")
    fig.savefig(path, dpi=300); plt.close(fig)


def quiver(gray, u, v, region, p95, path, col):
    h, w = gray.shape
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.imshow(gray, cmap="gray", vmin=0, vmax=255, interpolation="nearest")
    ys, xs = np.mgrid[STRIDE // 2:h:STRIDE, STRIDE // 2:w:STRIDE]
    # average the field over each cell so a single noisy pixel does not set the arrow
    k = STRIDE // 2
    U = np.array([[u[max(0, y - k):y + k, max(0, x - k):x + k][region[max(0, y - k):y + k, max(0, x - k):x + k]].mean()
                   if region[max(0, y - k):y + k, max(0, x - k):x + k].any() else np.nan for x in xs[0]] for y in ys[:, 0]])
    V = np.array([[v[max(0, y - k):y + k, max(0, x - k):x + k][region[max(0, y - k):y + k, max(0, x - k):x + k]].mean()
                   if region[max(0, y - k):y + k, max(0, x - k):x + k].any() else np.nan for x in xs[0]] for y in ys[:, 0]])
    s = STRIDE * 0.9 / p95
    ok = np.isfinite(U) & np.isfinite(V)
    ax.quiver(xs[ok], ys[ok], U[ok] * s, V[ok] * s, color=col, angles="xy", scale_units="xy", scale=1,
              width=0.0045, headwidth=3.5, headlength=4, headaxislength=3.5)
    ax.set_xlim(0, w); ax.set_ylim(h, 0)
    fig.savefig(path, dpi=300); plt.close(fig)


def wheel(path, n=301):
    r = np.linspace(-1, 1, n)
    u, v = np.meshgrid(r, r)
    inside = u ** 2 + v ** 2 <= 1
    rgb = color(u, v, inside, 1.0)
    rgb[~inside] = 1.0
    fig = plt.figure(figsize=(1.2, 1.2), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.imshow(rgb, extent=(-1, 1, 1, -1))
    fig.savefig(path, dpi=300, transparent=True); plt.close(fig)


def main():
    src = Path(sys.argv[1])
    z = np.load(src)
    u, v, du, dv, mask, gray = z["u"], z["v"], z["du"], z["dv"], z["mask"], z["gray"]
    region = np.isfinite(du) & np.isfinite(dv) & (np.hypot(np.nan_to_num(du), np.nan_to_num(dv)) > 0)
    du, dv = np.nan_to_num(du), np.nan_to_num(dv)
    # Display only: MVSEC GT has isolated missing pixels (speckle). Close holes up to HOLE px and fill
    # them from the nearest valid GT pixel. Statistics below use the solver's own mask, not this fill.
    closed = binary_closing(region, structure=np.ones((HOLE, HOLE)))
    _, (iy, ix) = distance_transform_edt(~region, return_indices=True)
    du_d, dv_d = du[iy, ix], dv[iy, ix]
    region_d = closed | region
    p_gt = float(np.percentile(np.hypot(du, dv)[region], 95))
    p_est = float(np.percentile(np.hypot(u, v)[region], 95))

    save_img(gray, HERE / "reference.png")
    save_img(color(du_d, dv_d, region_d, p_gt), HERE / "gt_color.png")
    save_img(color(u, v, region_d, p_gt), HERE / "est_color.png")
    # Event-masked color panels, as the thesis-era vox_focus figures: color only at pixels that received
    # events in this window (no dilation), white elsewhere; pale style (saturation = |flow| / P).
    ev = z["count"] > 0
    for name, (a, b) in (("gt", (du_d, dv_d)), ("est", (u, v))):
        save_img(color_pale(a, b, ev & region_d, p_gt), HERE / f"{name}_color_masked.png")
    color_pale_wheel(HERE / "wheel_masked.png")
    quiver(gray, du_d, dv_d, region_d, p_gt, HERE / "gt_quiver.png", "#d62728")
    quiver(gray, u, v, region_d, p_gt, HERE / "est_quiver.png", "#00c853")
    wheel(HERE / "wheel.png")

    e = np.hypot(u - du, v - dv)[mask]
    gm, em = np.hypot(du, dv)[mask], np.hypot(u, v)[mask]
    ang = np.degrees(np.arccos(np.clip((u * du + v * dv)[mask] / np.maximum(em * gm, 1e-12), -1, 1)))
    meta = json.loads((src.parent / "meta.json").read_text())
    meta.update(window_file=str(src), window_idx=int(src.stem.split("_")[-1]),
                eval_pixels=int(mask.sum()),
                aee_px=round(float(e.mean()), 3), zero_flow_aee_px=round(float(gm.mean()), 3),
                angular_error_deg_mean=round(float(ang.mean()), 2),
                angular_error_deg_median=round(float(np.median(ang)), 2),
                gt_mag_mean_px=round(float(gm.mean()), 3), est_mag_mean_px=float(f"{em.mean():.3g}"), mag_ratio=float(f"{em.mean() / gm.mean():.3g}"),
                p95_px=dict(gt=float(f"{p_gt:.4g}"), estimate=float(f"{p_est:.3g}")),
                rendering=__doc__.split("Rendering")[1].strip(),
                exporter="drafts/dissertation_defense/figures/flow_motivation_mvsec/export.py")
    meta["sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob("*.png"))}
    (HERE / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({k: meta[k] for k in ("window_idx", "aee_px", "zero_flow_aee_px", "angular_error_deg_mean",
                                            "angular_error_deg_median", "p95_px")}, indent=1))


if __name__ == "__main__":
    main()
