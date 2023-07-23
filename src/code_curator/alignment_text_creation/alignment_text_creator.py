from __future__ import annotations

from pathlib import Path

from ._forced_alignment_parser import create_aligned_script
from ._montreal_forced_aligner import MontrealForcedAligner


class AlignmentTextCreator:
    def __init__(self, dev_files_dir_path: Path) -> None:
        self.dev_files_dir_path = dev_files_dir_path

    @classmethod
    def create_alignment_text(cls, dev_files_dir_path: Path) -> Path:
        textgrid_path: Path = MontrealForcedAligner.perform_alignment(dev_files_dir_path)
        return create_aligned_script(textgrid_path, dev_files_dir_path / 'ai_generated_alignment_script.txt')
