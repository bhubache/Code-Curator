from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import docker

if TYPE_CHECKING:
    import os

logger = logging.getLogger(__name__)


def perform_alignment(script_path: str | os.PathLike, audio_path: str | os.PathLike) -> Path:
    script_path = Path(script_path)
    audio_path = Path(audio_path)

    volume_dir = Path("/", "tmp")
    base_mfa_dir = volume_dir / "mfa"
    input_mfa_dir = base_mfa_dir / "input"
    output_mfa_dir = base_mfa_dir / "output"

    shutil.rmtree(base_mfa_dir, ignore_errors=True)
    input_mfa_dir.mkdir(parents=True)
    output_mfa_dir.mkdir(parents=True)

    shutil.copy(script_path, input_mfa_dir / "script.txt")
    shutil.copy(audio_path, input_mfa_dir / "script.wav")

    client = docker.from_env()
    image_name = "mmcauliffe/montreal-forced-aligner"
    image_tag = "latest"

    client.images.pull(image_name, tag=image_tag)
    mfa_image = client.images.get(f"{image_name}:{image_tag}")

    client.containers.run(
        mfa_image,
        command=[
            "bash",
            "-c",
            (
                "mfa model download acoustic english_us_arpa && mfa model download dictionary english_us_arpa &&"
                f" mfa align {input_mfa_dir} english_us_arpa english_us_arpa {output_mfa_dir}"
            ),
        ],
        volumes=[f"{volume_dir}:{volume_dir}"],
        tty=True,
    )

    return output_mfa_dir / "script.TextGrid"
