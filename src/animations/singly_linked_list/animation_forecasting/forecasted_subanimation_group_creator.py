from .. import data_structure_animator
from ...subanimation_group import SubanimationGroup

class ForecastedSubanimationGroupCreator:
    def __init__(
        self,
        animator,
        subanimation_builder_helpers,
    ) -> None:
        self._animator: data_structure_animator.DataStructureAnimator = animator
        self._subanimation_builder_helpers = subanimation_builder_helpers

    @classmethod
    def create_forecasted_subanimation_group(cls, animator, subanimation_builder_helpers):
        forecasted_package_creator = ForecastedSubanimationGroupCreator(animator=animator, subanimation_builder_helpers=subanimation_builder_helpers)
        return forecasted_package_creator._create_successive_subanimations()

    def _create_successive_subanimations(self) -> SubanimationGroup:
        self._chain_subanimations()

        self._replace_subanimations_with_successive_counterparts()
        self._set_default_clean_up_mobject()
        return self._animator.get_subanimation_group()

    def _chain_subanimations(self) -> None:
        for builder_helper_func in self._subanimation_builder_helpers:
            builder_helper_func(self._animator)

    def _replace_subanimations_with_successive_counterparts(self) -> None:
        # TODO: Replace with higher level of abstraction

        # TODO: Change name of method called
        self._animator.create_subanimation_group_successive_counterpart()
        # self._forecasted_package.set_subanimation_group(self._forecasted_package.create_subanimation_group_successive_counterpart())

    def _set_default_clean_up_mobject(self) -> None:
        self._animator.clean_up_mobject = lambda : None
