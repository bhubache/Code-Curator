import json
import os

class AlignmentFileFixer:
    def __init__(self, parsings_path, timings_path):
        self.parsings_path = parsings_path
        self.timings_path = timings_path
        self.aligned_script_path = os.path.join(os.path.dirname(self.parsings_path), 'aligned_script.txt')

    def run(self):
        self.combine_parsings_and_timings()

    def combine_parsings_and_timings(self):
        words = []
        with open(self.parsings_path, 'r') as file:
            content = file.read()
            for line in content.splitlines():
                word = line.split('|')[-1].strip()
                if word.endswith(','):
                    word = word[:-1]
                words.append(word)

        timings_contents = None
        with open(self.timings_path, 'r') as file:
            timings_contents = file.read()

        with open(self.aligned_script_path, 'w') as file:
            for i, line in enumerate(timings_contents.splitlines()):
                timing_parts = line.strip().split()
                timing_parts = timing_parts[:-1]
                line = '  '.join(timing_parts)
                file.write(f'{line}  {words[i]}\n')



