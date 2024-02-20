from __future__ import annotations

import hashlib
from pathlib import Path

from ._forced_alignment_parser import create_aligned_script
from ._montreal_forced_aligner import MontrealForcedAligner


class AlignmentTextCreator:
    def __init__(self, dev_files_dir_path: Path) -> None:
        self.dev_files_dir_path = dev_files_dir_path

    @classmethod
    def create_alignment_text(cls, script_path: str | os.PathLike, audio_path: str | os.PathLike) -> Path:
        cached_hash_script_path = Path("/", "tmp", "cached_hash_script")
        cached_alignments_path = Path("/", "tmp", "cached_alignments")
        new_hash = hashlib.sha256(script_path.read_text().encode("UTF-8")).hexdigest()
        use_cached_file = True

        script_path = Path(script_path)
        try:
            cached_hash = cached_hash_script_path.read_text()
        except FileNotFoundError:
            use_cached_file = False
        else:
            if cached_hash != new_hash or not cached_alignments_path.exists():
                use_cached_file = False

        if use_cached_file:
            textgrid_path = cached_alignments_path
        else:
            textgrid_path: Path = MontrealForcedAligner.perform_alignment(
                script_path=script_path,
                audio_path=audio_path,
            )

            cached_alignments_path.write_text(new_hash)
            cached_alignments_path.write_text(textgrid_path.read_text())

        return create_aligned_script(textgrid_path, Path("/", "tmp", "aligned_script"))
