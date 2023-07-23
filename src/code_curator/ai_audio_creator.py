from __future__ import annotations

import subprocess
from pathlib import Path

class AIAudioCreator:
    @classmethod
    def create_audio(cls, script_path: Path) -> Path:
        # NOTE: Making audio and text names same for MFA.
        base_name = script_path.stem
        audio_suffix = '.wav'
        script_dir_path = script_path.parents[0]
        audio_path = script_dir_path / f'{base_name}{audio_suffix}'

        cmd: str = f'pico2wave --wave={audio_path} "$(cat {script_path})"'
        subprocess.getoutput(cmd)
        return audio_path
