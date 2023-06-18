from __future__ import annotations

from pathlib import Path


PROBLEM_DIR: str = 'Delete_Node_in_a_Linked_List'
TEXT_TO_ADD: str = (
    '''and not all values in the linked list were unique, then there would be ambiguity about which node to delete. however, we are given the node to be deleted, and so, like the prior constraint, this can be disregarded.'''
)

print(__file__)

BASE_PATH = Path(__file__).parents[1]

aligned_script_path = Path(
    BASE_PATH,
    'leetcode',
    'problems',
    PROBLEM_DIR,
    'generated_files',
    'aligned_script.txt',
)

# aligned_script_path: str = os.path.join(
#     os.getcwd(
#     ), 'leetcode', 'problems', PROBLEM_DIR, 'generated_files', 'aligned_script.txt',
# )

content_lines: list[str] = []

with open(aligned_script_path) as read_file:
    content_lines = read_file.read().splitlines()

start_time = float(content_lines[-1].split()[1])


for word in TEXT_TO_ADD.split():
    next_time = round(start_time + 0.5, 1)
    content_lines.append(f'{start_time}  {next_time}  {word}')
    start_time = next_time
with open(aligned_script_path, 'w') as write_file:
    write_file.write('\n'.join(content_lines))
