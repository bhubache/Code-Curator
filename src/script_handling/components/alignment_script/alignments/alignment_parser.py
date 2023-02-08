from .aligned_script import AlignedScript

# TODO:
# This class will probably have at least two purposes, so this should at some point be refactored to have only one responsibility,
# probably a parser class and a class to house the data

# TODO:
# Make an 'interface' of sorts using an ABC for a parser?

class AlignmentParser:
    def __init__(self, file_path: str):
        self._file_path: str = file_path
        self._info: dict = {}

    def parse(self) -> AlignedScript:
        word_alignments = None
        with open(self._file_path, 'r', encoding='UTF-8') as alignment_file:
            word_alignments = alignment_file.read().splitlines()

        first_word_start = float(word_alignments[0].split()[0])
        last_word_end = float(word_alignments[-1].split()[1])
        self._info['duration'] = round(last_word_end - first_word_start , 2)

        for i, line in enumerate(word_alignments):
            word_number = i + 1
            line_parts = line.split()

            self._info[word_number] = {}
            self._info[word_number]['start'] = float(line_parts[0])
            self._info[word_number]['end'] = float(line_parts[1])
            self._info[word_number]['text'] = line_parts[2]

        return AlignedScript(self._info)
