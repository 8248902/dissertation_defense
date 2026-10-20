#!/usr/bin/env python3
"""Export a slide-ready indoor_flying2 event-only example from saved arrays."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import h5py
import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
RELEASE = Path("/scratch/dblauvel/ch2_mvsec_release_20261018")
RUN_ID = "indoor_flying2_bump_05"
FRAME_INDEX = 80  # zero-based solved latent frame
WIDTH, HEIGHT = 346, 260


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = RELEASE / RUN_ID / "reconstruction.h5"
    reference_source = RELEASE / "reference" / "indoor_flying2.npz"
    with h5py.File(source) as h:
        if h.attrs["run_id"] != RUN_ID:
            raise ValueError("Saved run ID does not match")
        if h.attrs["bump_parameter"] != "gaussian(sigma=0.050)":
            raise ValueError("Unexpected temporal kernel")
        if h.attrs["regularization_rule"] != "sigmoid":
            raise ValueError("Unexpected regularization")
        time_s = h["latent_time_s"][:]
        pixels = h["processed_flat_index"][:]
        f_raw = h["f_raw"][:]
        event_prefix_sha256 = str(h.attrs["event_prefix_sha256"])
    if f_raw.shape[1] != len(time_s) or FRAME_INDEX >= len(time_s):
        raise ValueError("Unexpected solved frame dimensions")

    full = np.zeros((len(time_s), WIDTH * HEIGHT), dtype=np.float64)
    full[:, pixels] = f_raw.T
    counts, edges = np.histogram(full, bins=1000)
    peak = int(np.argmax(counts))
    background = float((edges[peak] + edges[peak + 1]) / 2)
    low, high = np.percentile(full, [1, 99])
    maximum_deviation = max(abs(low - background), abs(high - background))
    scale = 0.45 / maximum_deviation if maximum_deviation > 0 else 0.45
    display = np.clip(
        (full[FRAME_INDEX].reshape(HEIGHT, WIDTH) - background) * scale + 0.4,
        0, 1,
    )
    reconstruction_path = ROOT / "event_only_reconstruction.png"
    Image.fromarray(np.rint(255 * display).astype(np.uint8), "L").save(reconstruction_path)

    with np.load(reference_source) as z:
        reference_times = z["timestamps_s"]
        reference_index = int(np.argmin(np.abs(reference_times - time_s[FRAME_INDEX])))
        reference = z["frames"][reference_index]
        original_reference_sha256 = str(z["source_sha256"])
    if reference.shape != (HEIGHT, WIDTH):
        raise ValueError("Unexpected reference geometry")
    reference_path = ROOT / "reference.png"
    Image.fromarray(reference.astype(np.uint8), "L").save(reference_path)

    preview = Image.new("RGB", (WIDTH * 2, HEIGHT + 24), "white")
    draw = ImageDraw.Draw(preview)
    draw.text((4, 4), "Reference", fill="black")
    draw.text((WIDTH + 4, 4), "Event-only reconstruction (Gaussian 50 ms)", fill="black")
    preview.paste(Image.open(reference_path).convert("RGB"), (0, 24))
    preview.paste(Image.open(reconstruction_path).convert("RGB"), (WIDTH, 24))
    preview_path = ROOT / "preview.png"
    preview.save(preview_path)

    metadata = {
        "dataset": "MVSEC indoor_flying2",
        "camera": "left DAVIS",
        "geometry_px": [WIDTH, HEIGHT],
        "run_id": RUN_ID,
        "source_reconstruction_h5": str(source),
        "source_reference_npz": str(reference_source),
        "reference_source_original_sha256": original_reference_sha256,
        "event_prefix_sha256": event_prefix_sha256,
        "method": "event-only; Gaussian temporal kernel sigma 50 ms; sigmoid regularization",
        "estimator_rerun": False,
        "solved_frame_index_zero_based": FRAME_INDEX,
        "solved_time_epoch_s": float(time_s[FRAME_INDEX]),
        "reference_index_zero_based_in_saved_subset": reference_index,
        "reference_time_epoch_s": float(reference_times[reference_index]),
        "reference_minus_solved_ms": float(1000 * (reference_times[reference_index] - time_s[FRAME_INDEX])),
        "reference_selection": "nearest saved actual left-camera frame by epoch timestamp",
        "display": {
            "rule": "histogram-mode background; one 1st/99th-percentile scale over all 100 solved frames; clip((f-background)*scale+0.4,0,1); round to uint8",
            "background": background,
            "scale": float(scale),
            "clipped_fraction_at_selected_frame": float(np.mean((display == 0) | (display == 1))),
            "spatial_processing": "none; no sharpening, denoising, interpolation, or geometry change",
            "reference": "saved native 8-bit camera frame, unchanged",
        },
        "sha256": {p.name: digest(p) for p in [reference_path, reconstruction_path, preview_path]},
        "source_revision_note": "The saved 2026-10-18 release run has input hashes and a manifest; exact runtime checkout revision was not embedded in reconstruction.h5.",
    }
    (ROOT / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps({"solved_time_epoch_s": metadata["solved_time_epoch_s"], "reference_minus_solved_ms": metadata["reference_minus_solved_ms"], "clipped_fraction": metadata["display"]["clipped_fraction_at_selected_frame"]}))


if __name__ == "__main__":
    main()
