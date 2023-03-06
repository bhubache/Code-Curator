import difflib
from pprint import pprint

from manim import Mobject, Code, Animation, FadeIn, FadeOut, AnimationGroup, VGroup, DOWN, LEFT, Transform, Square
from code.code_diff import CodeDiff



class CodeTransform:
    def __init__(
        self,
        mobject:                              Mobject,
        target_mobject:                       Mobject,
        path_arc:                             float = 0,
        replace_mobject_with_target_in_scene: bool  = False,
        run_time:                             float = 1,
        **kwargs
    ):
        # super().__init__(mobject, run_time=run_time, rate_func=rate_func, **kwargs)
        self._src_code_obj = mobject
        self._dst_code_obj = target_mobject
        self._diff = CodeDiff(self.src_code_obj, self.dst_code_obj)
        self._lines_checked = [False for _ in self.diff]
        # Map - index in diff to + index in diff
        self._changed_lines = {}

        self._SRC_TO_DST_CHANGED_INDICES = {}

        self._src_to_dst_map = {}

        self._rearrange_diff_lines_as_needed()
        self._animation = self.get_animation()

    def _rearrange_diff_lines_as_needed(self):
        for i, line in enumerate(self.diff):
            if self.diff.line_unique_to_dst_code(line):
                other_line_change_index = None
                highest_similarity_score = 0
                for line_index in range(i + 1, len(self.diff)):
                    if not self.diff.line_unique_to_src_code(self.diff[line_index]):
                        break

                    curr_similarity_score = self.diff.get_sequence_similarity(line, self.diff[line_index])
                    if curr_similarity_score > highest_similarity_score:
                        highest_similarity_score = curr_similarity_score
                        other_line_change_index = line_index
                
                if highest_similarity_score > 0.65:
                    temp = self.diff[i]
                    for swapping_index in range(i, other_line_change_index):
                        self.diff[swapping_index] = self.diff[swapping_index + 1]
                    self.diff[other_line_change_index] = temp



    @property
    def src_code_obj(self):
        return self._src_code_obj

    @property
    def dst_code_obj(self):
        return self._dst_code_obj

    @property
    def diff(self):
        return self._diff

    @property
    def animation(self):
        return self._animation

    @property
    def lines_checked(self):
        return self._lines_checked

    @property
    def src_to_dst_map(self) -> dict:
        return self._src_to_dst_map

    def get_animation(self) -> AnimationGroup:
        matching_line_animations = self._get_matching_line_animations()
        added_line_animations = self._get_added_line_animations()
        removed_line_animations = self._get_removed_line_animations()
        changed_line_animations = self._get_changed_line_animations()

        highlighter_animation = FadeIn(Square().set_opacity(0))
        if self.src_code_obj.has_highlighter():
            if self.src_code_obj.highlighter.curr_line_num not in self.src_to_dst_map:
                # Line with highlighter gets removed
                highlighter_animation = FadeOut(src.src_code_obj.highlighter)
            else:
                dst_line_obj = self.dst_code_obj.get_line_at(self.src_to_dst_map[self.src_code_obj.highlighter.curr_line_num])
                highlighter_animation = self.src_code_obj.highlighter.animate. \
                    stretch_to_fit_width(dst_line_obj.width). \
                    align_to(dst_line_obj, DOWN + LEFT)
            self.src_code_obj.highlighter.curr_line_num = self.src_to_dst_map[self.src_code_obj.highlighter.curr_line_num]

        return AnimationGroup(AnimationGroup(*matching_line_animations, *removed_line_animations, *changed_line_animations, highlighter_animation), AnimationGroup(*added_line_animations), lag_ratio=0.5)

    def _get_matching_line_animations(self) -> list[Animation]:
        animations = []
        for i, line in enumerate(self.diff):
            if self.diff.line_common_to_both_codes(line):
                self._lines_checked[i] = True
                src_line = self.diff.get_source_line(line_index=i)
                dst_line = self.diff.get_destination_line(line_index=i)
                
                # Add line indices to map for highlighter transformation
                self.src_to_dst_map[self.diff.get_source_line_index(i)] = self.diff.get_destination_line_index(i)
                animations.append(src_line.animate.align_to(dst_line, DOWN))
        return animations

    def _get_added_line_animations(self) -> list[Animation]:
        animations = []
        for i, line in enumerate(self.diff):
            # If line unique to destination code
            if self.diff.line_unique_to_dst_code(line):
                if not self.line_connects_back_to_src(i):
                    if not self._lines_checked[i]:
                        self._lines_checked[i] = True
                        animations.append(FadeIn(self.diff.get_destination_line(line_index=i)))

                        # Add line indices to map for highlighter transformation
                        self.src_to_dst_map[self.diff.get_source_line_index(i)] = self.diff.get_destination_line_index(i)
                else:
                    unique_to_src_index = self.src_index_connecting_new_lines(line_index=i)
                    unique_to_src_line = self.diff[unique_to_src_index]

                    other_changed_line_index = -1
                    highest_similarity_score = 0

                    index = unique_to_src_index + 1
                    while(index < len(self.diff) and self.diff.line_unique_to_dst_code(self.diff[index])):
                        similarity_score = self.diff.get_sequence_similarity(unique_to_src_line, self.diff[index])

                        if similarity_score > highest_similarity_score:
                            highest_similarity_score = similarity_score
                            other_changed_line_index = index
                        
                        index += 1

                    self._changed_lines[unique_to_src_index] = other_changed_line_index
                    self._SRC_TO_DST_CHANGED_INDICES[unique_to_src_index] = self.diff.get_destination_line_index(other_changed_line_index)

                    index = unique_to_src_index + 1
                    while(index < len(self.diff) and self.diff.line_unique_to_dst_code(self.diff[index])):
                        if index == other_changed_line_index:
                            index += 1
                            continue

                        if not self._lines_checked[index]:
                            self._lines_checked[index] = True
                            animations.append(FadeIn(self.diff.get_destination_line(line_index=index)))

                            # Add line indices to map for highlighter transformation
                            self.src_to_dst_map[self.diff.get_source_line_index(i)] = self.diff.get_destination_line_index(i)
                        index += 1
        return animations

    def src_index_connecting_new_lines(self, line_index: int) -> int:
        for i in range(line_index, -1, -1):
            if self.diff.line_unique_to_src_code(self.diff[i]): return i
        return -1

    def line_connects_back_to_src(self, line_index: int) -> bool:
        for i in range(line_index, -1, -1):
            if self.diff.line_common_to_both_codes(self.diff[i]): return False
            if self.diff.line_unique_to_src_code(self.diff[i]): return True
        return False

    def _get_removed_line_animations(self) -> list[Animation]:
        animations = []
        for i, line in enumerate(self.diff):
            if self.diff.line_unique_to_src_code(line):
                if i == len(self.diff) - 1 or not self.diff.line_unique_to_dst_code(self.diff[i + 1]):
                    if not self._lines_checked[i]:
                        self._lines_checked[i] = True
                        animations.append(FadeOut(self.diff.get_source_line(line_index=i)))

                        # Add line indices to map for highlighter transformation
                        self.src_to_dst_map[self.diff.get_source_line_index(i)] = self.diff.get_destination_line_index(i)
        return animations

    def _get_changed_line_animations(self) -> list[Animation]:
        for src_index, dst_index in self._SRC_TO_DST_CHANGED_INDICES.items():
            # Add line indices to map for highlighter transformation
            self.src_to_dst_map[src_index] = dst_index
        animations = []
        for src_index, dst_index in self._changed_lines.items():
            # Remove the '- ' or '+ ' from the lines
            cleaned_src_line = self.diff[src_index][2:]
            cleaned_dst_line = self.diff[dst_index][2:]
            # cleaned_src_line = line[2:]
            # cleaned_dst_line = self.diff[line_index + 1][2:]

            # Get the char diff
            char_diff = list(difflib.ndiff(cleaned_src_line, cleaned_dst_line))

            # NOTE: Loose definition right now
            # Separate char diff into tokens by ' ' and '('
            diff_words = []
            string = ''
            for char in char_diff:
                string += char
                if char == '   ' or char == '  (':
                    diff_words.append(string)
                    string = ''
            diff_words.append(string)

            total_word_changes = 0
            for word in diff_words:
                if self.diff.word_contains_added_char(word) or self.diff.word_contains_removed_char(word):
                    total_word_changes += 1


            num_changed = 0
            prev_src_end_index = 0
            prev_dst_end_index = 0
            for word_index, word in enumerate(diff_words):
                # Find a token that has been changed
                if self.diff.word_contains_added_char(word) or self.diff.word_contains_removed_char(word):
                    src_start_index, src_end_index = self._get_src_word_bounds(src_index, word_index, diff_words)
                    dst_start_index, dst_end_index = self._get_dst_word_bounds(src_index, word_index, diff_words)

                    src_line_index = self.diff.get_source_line_index(src_index)
                    dst_line_index = self.diff.get_destination_line_index(dst_index)

                    animations.append(
                        Transform(
                            self.src_code_obj[2][src_line_index][src_start_index : src_end_index],
                            self.dst_code_obj[2][dst_line_index][dst_start_index : dst_end_index]    
                        )
                    )

                    animations.append(
                        self.src_code_obj[2][src_line_index][src_end_index:].animate.align_to(self.dst_code_obj[2][dst_line_index][dst_end_index:], LEFT+DOWN)
                    )
                    # animations.append(
                    #     self.src_code_obj[2][src_line_index][src_end_index:].animate.align_to(self.dst_code_obj[2][dst_line_index][dst_end_index:], DOWN)
                    # )
                    
                    if num_changed == 0:
                        animations.append(
                            self.src_code_obj[2][src_line_index][:src_start_index].animate.align_to(self.dst_code_obj[2][dst_line_index][:dst_start_index], DOWN)
                        )
                    else:
                        if num_changed == total_word_changes - 1:
                            pass
                            # animations.append(
                            #     self.src_code_obj[2][src_line_index][src_end_index:].animate.align_to(self.dst_code_obj[2][dst_line_index][dst_end_index:], DOWN)
                            # )
                        
                        # animations.append(
                        #     self.src_code_obj[2][src_line_index][prev_src_end_index : src_start_index].animate.align_to(self.dst_code_obj[2][dst_line_index][prev_dst_end_index : dst_start_index], DOWN)
                        # )

                    prev_src_end_index = src_end_index
                    prev_dst_end_index = dst_end_index
                    
                    num_changed += 1







            

        # for line_index, line in enumerate(self.diff):
        #     # The last line of a diff can't be a changed line from source
        #     if line_index == len(self.diff) - 1: continue

        #     # Only consider line that could be changed
        #     # Technically, this also captures a the scenario where a line was removed and the
        #     # following line was added but I think we can treat them the same as the animation
        #     # being the same isn't a big deal (I think)
        #     if self.diff.line_unique_to_src_code(line) and self.diff.line_unique_to_dst_code(self.diff[line_index + 1]):
        #         # Remove the '- ' or '+ ' from the lines
        #         cleaned_src_line = line[2:]
        #         cleaned_dst_line = self.diff[line_index + 1][2:]

        #         # Get the char diff
        #         char_diff = list(difflib.ndiff(cleaned_src_line, cleaned_dst_line))

        #         # NOTE: Loose definition right now
        #         # Separate char diff into tokens by ' ' and '('
        #         diff_words = []
        #         string = ''
        #         for char in char_diff:
        #             string += char
        #             if char == '   ' or char == '  (':
        #                 diff_words.append(string)
        #                 string = ''
        #         diff_words.append(string)

        #         for word_index, word in enumerate(diff_words):
        #             # Find a token that has been changed
        #             if self.diff.word_contains_added_char(word) or self.diff.word_contains_removed_char(word):
        #                 src_start_index, src_end_index = self._get_src_word_bounds(line_index, word_index, diff_words)
        #                 dst_start_index, dst_end_index = self._get_dst_word_bounds(line_index, word_index, diff_words)

        #                 print(f'src: {src_start_index} - {src_end_index}')
        #                 print(f'dst: {dst_start_index} - {dst_end_index}')

        #                 src_line_index = self.diff.get_source_line_index(line_index)
        #                 dst_line_index = self.diff.get_destination_line_index(line_index + 1)

        #                 print(src_line_index)
        #                 print(dst_line_index)

        #                 print(self.src_code_obj[2][src_line_index])
        #                 animations.append(
        #                     Transform(
        #                         self.src_code_obj[2][src_line_index][src_start_index : src_end_index],
        #                         self.dst_code_obj[2][dst_line_index][dst_start_index : dst_end_index]    
        #                     )
        #                 )

        #                 animations.append(
        #                     self.src_code_obj[2][src_line_index][src_end_index:].animate.align_to(self.dst_code_obj[2][dst_line_index][dst_end_index:], LEFT)
        #                 )
        return animations

    def _get_word_bounds(self, diff_line_index: int, diff_word_index: int, diff_words: list[str], type_: str) -> tuple[int, int]:
        code_line_obj = None
        if type_ == 'src':
            code_line_obj = self.diff.get_source_line(line_index=diff_line_index)
        else:
            code_line_obj = self.diff.get_destination_line(line_index=diff_line_index)

        start_index = 0
        char_to_ignore = None
        if type_ == 'src':
            char_to_ignore = '+'
        else:
            char_to_ignore = '-'

        for i, diff_word in enumerate(diff_words):
            if i == diff_word_index:
                break

            # Keep length of trailing space
            if diff_word.endswith('   '):
                diff_word = diff_word.replace('   ', '  ?')


            cleaned_word = ''.join(diff_word.split())
            cleaned_word_full = ''.join([char for i, char in enumerate(cleaned_word) if char != '-' and char != '+' and ((i != 0 and cleaned_word[i - 1] != char_to_ignore) or (i == 0 and cleaned_word[i] != char_to_ignore))])

            start_index += len(cleaned_word_full)

        joined_word = ''.join(diff_words[diff_word_index].split())
        joined_word = joined_word.replace('--', '-?-')
        joined_word = joined_word.replace('++', '+?+')
        original_word = ''.join([char for i, char in enumerate(joined_word) if char != '-' and char != '+' and (i != 0 and joined_word[i - 1] != char_to_ignore)])
        
        # Exclusive
        end_index = start_index + len(original_word)
        return start_index, end_index

    def _get_dst_word_bounds(self, diff_line_index: int, diff_word_index: int, diff_words: list[str]) -> tuple[int, int]:
        return self._get_word_bounds(diff_line_index=diff_line_index, diff_word_index=diff_word_index, diff_words=diff_words, type_='dst')

    def _get_src_word_bounds(self, diff_line_index: int, diff_word_index: int, diff_words: list[str]) -> tuple[int, int]:
        return self._get_word_bounds(diff_line_index=diff_line_index, diff_word_index=diff_word_index, diff_words=diff_words, type_='src')
