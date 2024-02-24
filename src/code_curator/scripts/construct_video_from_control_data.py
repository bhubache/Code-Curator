"""Plays the video/image from the latest graphical unit test that generated control data.

Usage: ``python3 path/to/construct_video_from_control_data.py``
"""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path

import distro
import extract_frames
from moviepy.editor import concatenate_videoclips
from moviepy.editor import ImageClip


def main() -> None:
    tests_path = next(path for path in Path.cwd().iterdir() if path.name == "tests") / "test_graphical_units"
    latest_control_data_file = sorted(
        [path for path in tests_path.rglob("*") if path.suffix == ".npz"],
        key=os.path.getctime,
    )[-1]

    print("----------------------------")
    print(latest_control_data_file.name)
    print("----------------------------")

    frames_dir = Path("/", "tmp", "test_frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    Path.mkdir(frames_dir, parents=True)

    extract_frames.main(
        npz_file=latest_control_data_file,
        output_dir=frames_dir,
    )

    ordered_frame_paths = sorted(
        frames_dir.iterdir(),
        key=lambda path: int(path.stem.replace("frame", "")),
    )

    clips = [ImageClip(str(image)).set_duration(0.25) for image in ordered_frame_paths]

    concatenated_clip = concatenate_videoclips(clips, method="compose")
    concatenated_clip.write_videofile(str(frames_dir / "video.mp4"), fps=6)
    if distro.id() == "arch":
        google_executable = "google-chrome-stable"
    elif distro.id() == "ubuntu":
        google_executable = "google-chrome"

    subprocess.run(shlex.split(f"{google_executable} {frames_dir / 'video.mp4'}"))


if __name__ == "__main__":
    raise SystemExit(main())
