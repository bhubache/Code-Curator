from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from ...subanimation_group import SubanimationGroup
from ..subanimations.base_subanimation import BaseSubanimation
from ..subanimations.leaf_subanimation import LeafSubanimation


class InterdependentSubanimationFinder:
    def __init__(self, subanimation_group: SubanimationGroup):
        self._subanimation_group: SubanimationGroup = subanimation_group
        self._csv_file_name: str = 'subanimation_interdependency.csv'

    def get_interdependent_subanimations(self) -> list[LeafSubanimation]:
        interdepenent_subanimations = []
        for group in self._subanimation_group:
            if group.has_one_subanimation() or group.is_successive_group():
                continue

            flattened_group: SubanimationGroup = list(group.flatten())

            for i, _ in enumerate(flattened_group):
                for j, _ in enumerate(flattened_group):

                    if i == j:
                        continue

                    if self._subanimation_pair_is_interdependent(flattened_group[i], flattened_group[j]):
                        if flattened_group[i] not in interdepenent_subanimations:
                            interdepenent_subanimations.append(
                                flattened_group[i],
                            )
                        if flattened_group[j] not in interdepenent_subanimations:
                            interdepenent_subanimations.append(
                                flattened_group[j],
                            )
        return interdepenent_subanimations

    def _subanimation_pair_is_interdependent(self, first_sub: BaseSubanimation, second_sub: BaseSubanimation) -> bool:
        subanimations_to_ignore = ['FadeInMobject', 'FadeOutMobject']
        first_sub_name = first_sub.__class__.__name__
        second_sub_name = second_sub.__class__.__name__
        if first_sub_name in subanimations_to_ignore or second_sub_name in subanimations_to_ignore:
            return False

        base_path: Path = Path(__file__).parent
        df_subanimation_orth = pd.read_csv(
            os.path.join(base_path, self._csv_file_name),
            index_col=0,
        )

        first_order_interdependency = df_subanimation_orth.at[first_sub_name, second_sub_name]
        second_order_interdependency = df_subanimation_orth.at[second_sub_name, first_sub_name]

        order_interdependencies_to_check = [
            first_order_interdependency, second_order_interdependency,
        ]

        return 'yes' in order_interdependencies_to_check
