from .singly_linked_list import data_structure_animator
from manim import Animation


from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class DataStructureAnimation(Animation):
    def __init__(self, sll, data_structure_animator):
        super().__init__(sll, run_time=data_structure_animator.get_run_time())
        self._sll = sll
        self._animator = data_structure_animator

    def begin(self):
        self._animator.begin()
        super().begin()

    def interpolate_mobject(self, alpha):
        self._animator.interpolate_mobject(alpha)

    def clean_up_from_scene(self, scene) -> None:
        self._animator.clean_up_from_scene(scene)
        # self._animator.clean_up_mobject()
        return super().clean_up_from_scene(scene)
