from __future__ import annotations

import tarfile
from pathlib import Path

import docker


ALIGNMENT_HAS_CHANGED = False


class MontrealForcedAligner:
    def __init__(self, dev_files_dir_path: Path) -> None:
        self.dev_files_dir_path = dev_files_dir_path
        self.mfa_dir_path = self.dev_files_dir_path / "MFA"
        self.input_dir_path = self.mfa_dir_path / "input"
        self.output_dir_path = self.mfa_dir_path / "output"

        self.mfa_dir_path.mkdir(parents=True, exist_ok=True)
        self.input_dir_path.mkdir(parents=True, exist_ok=True)
        self.output_dir_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def perform_alignment(cls, script_path: str | os.PathLike, audio_path: str | os.PathLike) -> Path:
        client = docker.from_env()
        image_name = "mmcauliffe/montreal-forced-aligner"
        image_tag = "v2.2.17"

        # client.images.pull(image_name, tag=image_tag)
        # mfa_image = client.images.get(f"{image_name}:{image_tag}")

        # mfa_container = client.containers.create(mfa_image)

        # client.containers.run(mfa_image, command="mfa model download acoustic english_us_arpa")
        # client.containers.run(mfa_image, command="mfa model download dictionary english_us_arpa")

        script_file_path = Path("/", "tmp", "curator", "MFA", "input", "ai_script.txt")
        audio_file_path = Path("/", "tmp", "test", "ai_audio.wav")
        docker_script_file_path = Path("/", "ai_script.txt")
        docker_audio_file_path = Path("/", "ai_audio.wav")

        tar_path = Path("script_and_audio_tar")
        with tarfile.open(tar_path, "w") as tar:
            tar.add(script_file_path, arcname="script.txt")
            tar.add(audio_file_path, arcname="audio.wav")

        with open(tar_path, "rb") as tar:
            if not mfa_container.put_archive(path="/", data=tar):
                raise RuntimeError("Putting archive in MFA container failed")

        docker_alignment_files_dir = Path("/", "mfa", "alignment_files")
        client.containers.run(mfa_image, command=f"mkdir -p {docker_alignment_files_dir}")
        client.containers.run(mfa_image, command=f"tar -xvf {Path('/', tar_path)} -C {docker_alignment_files_dir}")

        client.containers.run(
            mfa_image,
            command=" ".join(
                (
                    "mfa",
                    "align",
                    docker_alignment_files_dir,
                    "english_us_arpa",
                    "english_us_arpa",
                    "/mfa/mfa_output",
                )
            )

        # tar aligned file
        # retrieve archive from docker container

        # aligner = MontrealForcedAligner(dev_files_dir_path)

        # aligner._verify_file_structure()
        # return aligner._perform_alignment()

    def _verify_file_structure(self) -> None:
        self._verify_mfa_dir_exists()
        self._verify_input_and_output_dirs()
        self._verify_input_dir_has_two_files()
        self._verify_input_dir_has_text_and_audio()
        self._verify_audio_and_text_have_same_name()

    def _verify_mfa_dir_exists(self) -> None:
        if not self.mfa_dir_path.exists():
            raise FileNotFoundError(f"The directory {mfa_dir} is needed for montreal forced alignment.")

    def _verify_input_and_output_dirs(self) -> None:
        if not self.input_dir_path.exists() or not self.output_dir_path.exists():
            raise FileNotFoundError(
                f"The following two directories are required for montreal forced aligned: {self.input_dir_path} and"
                f" {self.output_dir_path}",
            )

    def _verify_input_dir_has_two_files(self) -> None:
        if (num_files := len(list(self.input_dir_path.iterdir()))) != 2:
            raise ValueError(
                f"{self.input_dir_path} must only have 2 files: a text file and an audio file... {num_files} found.",
            )

    def _verify_input_dir_has_text_and_audio(self) -> None:
        allowed_audio_suffixes: tuple[str, str] = (".wav", ".mp3")
        allowed_text_suffixes: tuple[str] = (".txt",)

        files: list[Path] = list(self.input_dir_path.iterdir())

        if not [file_name for file_name in files if file_name.suffix in allowed_audio_suffixes]:
            raise FileNotFoundError(f"Unable to find audio file in {self.input_dir_path}")

        if not [file_name for file_name in files if file_name.suffix in allowed_text_suffixes]:
            raise FileNotFoundError(f"Unable to find text file in {self.input_dir_path}")

    def _verify_audio_and_text_have_same_name(self) -> None:
        file_one, file_two = list(self.input_dir_path.iterdir())

        if file_one.stem != file_two.stem:
            raise ValueError(
                f"Text and audio file in {self.input_dir_path} must have the same names: found {file_one.stem} and"
                f" {file_two.stem}",
            )

    def _perform_alignment(self) -> Path:
        conda_venv = "aligner"
        cwd = self.mfa_dir_path
        python_run_alignment_script = (
            Path.cwd() / "src" / "code_curator" / "alignment_text_creation" / "run_alignment.py"
        )

        if not ALIGNMENT_HAS_CHANGED:
            return list(self.output_dir_path.iterdir())[0]

        subprocess.run(f"conda run -n {conda_venv} python3 {python_run_alignment_script } --cwd={cwd}".split())

        return list(self.output_dir_path.iterdir())[0]
