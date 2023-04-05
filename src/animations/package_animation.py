from .subanimation_group import SubanimationGroup
from manim import Animation

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class PackageAnimation(Animation):
    def __init__(self, sll, subanimation_group: SubanimationGroup):
        super().__init__(sll, run_time=animation_package.get_num_animations())
        self._sll = sll
        self._subanimation_group = animation_package

    def begin(self):
        self._subanimation_group.begin()
        super().begin()

    def interpolate_mobject(self, alpha):
        self._subanimation_group.interpolate_mobject(alpha)

    def clean_up_from_scene(self, scene) -> None:
        self._subanimation_group.clean_up_from_scene(scene)
        return super().clean_up_from_scene(scene)
