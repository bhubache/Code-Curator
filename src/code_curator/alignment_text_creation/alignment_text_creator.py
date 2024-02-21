from __future__ import annotations

import hashlib
import logging
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from . import _montreal_forced_aligner
from ._forced_alignment_parser import create_aligned_script

if TYPE_CHECKING:
    import os

logger = logging.getLogger(__name__)


def create_alignment_text(script_text: str | os.PathLike, audio_path: str | os.PathLike) -> Path:
    cached_hash_script_path = Path("/", "tmp", "cached_hash_script")
    cached_alignments_path = Path("/", "tmp", "cached_alignments")
    new_hash = hashlib.sha256(script_text.encode("UTF-8")).hexdigest()
    use_cached_file = True

    try:
        cached_hash = cached_hash_script_path.read_text()
    except FileNotFoundError:
        logger.debug("cached hash script path doesn't exist")
        use_cached_file = False
    else:
        if cached_hash != new_hash:
            logger.debug("script contents have changed")
            use_cached_file = False
        elif not cached_alignments_path.exists():
            logger.debug("cached alignments doesn't exist")
            use_cached_file = False

    if use_cached_file:
        logger.debug("using cached alignments file")
        textgrid_path = cached_alignments_path
    else:
        logger.debug("creating new alignments file")
        with tempfile.NamedTemporaryFile("r+t") as script_file:
            script_file.write(script_text)
            script_file.seek(0)

            textgrid_path: Path = _montreal_forced_aligner.perform_alignment(
                script_path=script_file.name,
                audio_path=audio_path,
            )

        cached_alignments_path.write_text(new_hash)
        cached_alignments_path.write_text(textgrid_path.read_text())

    return create_aligned_script(textgrid_path)
