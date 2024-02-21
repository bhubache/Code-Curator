from __future__ import annotations

import hashlib
import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


def create_audio(script_text: str) -> Path:
    cached_hash_script_path = Path("/", "tmp", "cached_hash_script")
    cached_audio_path = Path("/", "tmp", "cached_audio")
    use_cached_file = True
    new_hash = hashlib.sha256(script_text.encode("UTF-8")).hexdigest()

    try:
        cached_hash = cached_hash_script_path.read_text()
    except FileNotFoundError:
        logger.debug("cached hash of script does not exist")
        use_cached_file = False
    else:
        if cached_hash != new_hash:
            logger.debug("contents of script have changed")
            use_cached_file = False
        elif not cached_audio_path.exists():
            logger.debug("cached audio file doesn't exist")
            use_cached_file = False

    if use_cached_file:
        logger.debug("Using cached audio file")
        return cached_audio_path

    logger.debug("Creating new audio file")

    with tempfile.NamedTemporaryFile("r+t") as script_file:
        script_file.write(script_text)

        with tempfile.NamedTemporaryFile("r+t") as audio_file:
            cmd = f"text2wave -o {audio_file.name} {script_file.name}"
            subprocess.getoutput(cmd)

            cached_hash_script_path.write_text(new_hash)
            shutil.copy(audio_file.name, cached_audio_path)

    return cached_audio_path
