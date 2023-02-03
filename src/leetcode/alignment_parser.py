# from .parser import Parser
from .aligned_script import AlignedScript

# TODO:
# This class will probably have at least two purposes, so this should at some point be refactored to have only one responsibility,
# probably a parser class and a class to house the data

# TODO:
# Make an 'interface' of sorts using an ABC for a parser?

class AlignmentParser:
    def __init__(self, alignment_path):
        self._alignment_path: str = alignment_path
        self._alignment_info: dict = {}

    def parse(self):
        word_alignments = None
        with open(self._alignment_path, 'r', encoding='UTF-8') as alignment_file:
            word_alignments = alignment_file.read().splitlines()

        duration_of_section = float(word_alignments[0].split()[0]) + float(word_alignments[-1].split()[1])
        self._alignment_info['duration'] = duration_of_section
        for i, line in enumerate(word_alignments):
            word_number = i + 1
            line_parts = line.split()

            self._alignment_info[word_number] = {}
            self._alignment_info[word_number]['start'] = float(line_parts[0])
            self._alignment_info[word_number]['end'] = float(line_parts[1])
            self._alignment_info[word_number]['text'] = line_parts[2]

        return self._get_parsed_script(self._alignment_info)

    def _get_parsed_script(self, parsed_info: dict):
        return AlignedScript(parsed_info)
