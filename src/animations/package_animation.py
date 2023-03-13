from .animation_package import AnimationPackage
from manim import Animation

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class PackageAnimation(Animation):
    def __init__(self, sll, animation_package: AnimationPackage):
        super().__init__(sll, run_time=animation_package.get_num_animations())
        self._sll = sll
        self._package = animation_package
        logger.info(id(self._sll))

    def begin(self):
        self._package.begin()
        super().begin()

    def interpolate_mobject(self, alpha):
        self._package.interpolate_mobject(alpha)

    def clean_up_from_scene(self, scene) -> None:
        self._package.clean_up_from_scene(scene)
        return super().clean_up_from_scene(scene)