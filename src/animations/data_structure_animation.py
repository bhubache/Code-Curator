from .singly_linked_list import data_structure_animator
from .subanimation_group import SubanimationGroup
from manim import Animation


from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class DataStructureAnimation(Animation):
    def __init__(self, sll, data_structure_animator):
        super().__init__(sll, run_time=data_structure_animator.get_run_time())
        self._sll = sll
        self._animator = data_structure_animator
        self._subanimation_group: SubanimationGroup = self._animator.get_subanimation_group()

    def begin(self):
        self._subanimation_group.init_run_time()
        super().begin()

    def interpolate_mobject(self, alpha):
        self._subanimation_group.interpolate(alpha)

    def clean_up_from_scene(self, scene) -> None:
        self._subanimation_group.clean_up_from_scene(scene)
        self._animator.clean_up_mobject()
        return super().clean_up_from_scene(scene)
