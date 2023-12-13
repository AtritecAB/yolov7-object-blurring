import random
import argparse
from pathlib import Path
import cv2
import numpy as np
from utils.plots import plot_one_box
from tqdm import tqdm
from mpire import WorkerPool


def process_image_func(orig_dir: Path, out_dir: Path):
    def process_image(text_file: Path, original_image: str):
        img = cv2.imread(str(orig_dir / original_image))
        height, width, _ = img.shape
        with open(text_file) as f:
            for det in f:
                cls, x, y, w, h = det.strip().split(" ")
                x, y, w, h = [float(val) for val in [x, y, w, h]]
                xywh = np.array(
                    [int(x * width), int(y * height), int(w * width), int(h * height)]
                )
                xyxy = np.array(
                    [
                        xywh[0] - xywh[2] / 2,
                        xywh[1] - xywh[3] / 2,
                        xywh[0] + xywh[2] / 2,
                        xywh[1] + xywh[3] / 2,
                    ]
                )
                plot_one_box(
                    xyxy, img, label=cls, color=colors[int(cls)], line_thickness=3
                )
            cv2.imwrite(str(out_dir / original_image), img)

    return process_image


if __name__ == "__main__":
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(100)]

    parser = argparse.ArgumentParser()
    parser.add_argument("originals", type=Path, help="Path to experiment dir.")
    parser.add_argument("experiment", type=Path, help="Path to experiment dir.")
    parser.add_argument(
        "--jobs", type=int, default=8, help="Number of jobs for execution."
    )
    args = parser.parse_args()

    outdir = args.experiment / "with_boxes"

    if not outdir.exists():
        outdir.mkdir()

    files_with_detections = (args.experiment / "labels").glob("*.txt")
    files_with_detections = {det: f"{det.stem}.jpg" for det in files_with_detections}

    with WorkerPool(n_jobs=args.jobs) as pool:
        pool.map(
            process_image_func(args.originals, outdir),
            files_with_detections.items(),
            iterable_len=len(files_with_detections),
            progress_bar=True,
        )
