from __future__ import annotations

import logging
import shlex
import shutil
import subprocess
import tarfile
from pathlib import Path

import docker

logger = logging.getLogger(__name__)


ALIGNMENT_HAS_CHANGED = False


class MontrealForcedAligner:

    @classmethod
    def perform_alignment(cls, script_path: str | os.PathLike, audio_path: str | os.PathLike) -> Path:
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
                f"mfa model download acoustic english_us_arpa && mfa model download dictionary english_us_arpa && mfa align /tmp/mfa/input english_us_arpa english_us_arpa /tmp/mfa/output",
            ],
            volumes=[f"{volume_dir}:{volume_dir}"],
            tty=True,
        )

        return output_mfa_dir / "script.TextGrid"

