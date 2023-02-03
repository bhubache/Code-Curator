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


        # base_config = None
        # with open('leetcode.json', 'r') as file:
        #     base_config = json.load(file)

        # setup_config = base_config['problem_setup']

        # keys = ['title', 'statement_header', 'statement', 'constraints_header', 'constraints']

        # word_timing_index = 0
        # with open(self.aligned_script_path, 'r') as self.timings_path:
        #     word_timings = self.timings_path.readlines()
        #     for i in range(len(word_timings)):
        #         word_timings[i] = word_timings[i].split()
        #     for key in keys:
        #         for i in range(len(setup_config[key]['text'].split())):
        #             # print(word_timings[word_timing_index + i][-1])
        #             print(len(setup_config[key]['text']))
        #             pass
        #             curr_timing = word_timings[word_timing_index + i]
        #             start = float(curr_timing[0])
        #             end = float(curr_timing[1])
        #             word = curr_timing[2]

        #             setup_config[key][word] = {}
        #             setup_config[key][word]['start'] = start
        #             setup_config[key][word]['end'] = end
        #             setup_config[key][word]['duration'] = round(end - start, 2)
        #         word_timing_index += len(setup_config[key]['text'].split())

        # print(json.dumps(setup_config, indent=4))



