from manim import Animation, VGroup

class BaseSLLAnimation(Animation):
    def __init__(
        self,
        sll,
        index,
        node,
        mob_groups,
        **kwargs
    ):
        super().__init__(sll, **kwargs)
        self.sll = sll
        self.index = index
        self.node = node
        self.group_to_shift = VGroup(*[node for i, node in enumerate(self.sll) if i > self.index], self.sll.tail_pointer)
        self.mob_groups = mob_groups
        self.num_animations = len(self.mob_groups)
        self.alpha_thresholds = {num: num / self.num_animations for num in self.mob_groups}
        self.alpha_step_size = 1 / self.num_animations

    def _get_normalized_alpha(self, alpha: float, animation_num: int) -> float:
        start_alpha = self.alpha_thresholds[animation_num] - self.alpha_step_size
        end_alpha = start_alpha + self.alpha_step_size

        if alpha < start_alpha:
            return 0
        elif start_alpha <= alpha <= end_alpha:
            alpha = (alpha - (self.alpha_step_size * (animation_num - 1))) / self.alpha_step_size
            if alpha > 1:
                alpha = 1
            return alpha
        elif alpha > end_alpha:
            return 1000
        else:
            raise Exception(f'Animation number {animation_num} has alpha {alpha}')
        
    def _get_mob_animation_num(self, mob_name: str) -> int:
        for animation_num, mob_group in self.mob_groups.items():
            if mob_name in mob_group:
                return animation_num
        raise