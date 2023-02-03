import os
import docx
# import pyautogui as pa
from pynput import mouse
from pynput.mouse import Controller as mouse_ctrl
from pynput import keyboard
from pynput.keyboard import Controller as key_ctrl
from pynput.keyboard import Key

import shutil

import time

from fix_timings_file import AlignmentFileFixer

class ForcedAligner:
    def __init__(self, title):

        self.exe_path = r'C:\Users\brand\Reading_App_Builder.lnk'
        self.problem_dir = fr'C:\Users\brand\Documents\ManimCS\leetcode_problems\{"_".join(title.strip().split())}'

        self.audio_path = os.path.join(self.problem_dir, 'audio.mp3')
        self.aligner_path = os.path.join(self.problem_dir, 'aligner_file.docx')

        self.mouse = None
        self.mouse_listener = None

    def run(self):
        self.create_comma_separated_list_script()
        self.open_application()
        self.perform_alignment()
        self.move_timings_and_parsings()

    def create_comma_separated_list_script(self):
        script_exact = None
        with open(os.path.join(self.problem_dir, 'script_exact.txt'), 'r') as in_file:
            with open(os.path.join(self.problem_dir, 'script_comma_separated_list.txt',), 'w') as out_file:
                script_minus_commas = in_file.read().replace(',', '')
                out_file.write(','.join(script_minus_commas.split()))
                
        with open(os.path.join(self.problem_dir, 'script_comma_separated_list.txt',), 'r') as read_file:
            doc = docx.Document()
            doc.add_paragraph(read_file.read())
            doc.save(os.path.join(self.problem_dir, 'aligner_file.docx'))

    def open_application(self):
        os.system(self.exe_path)

    def perform_alignment(self):
        self.mouse = mouse_ctrl()
        self.keyboard = key_ctrl()

        # self.mouse_listener = mouse.Listener(on_click=self.on_click)
        # self.mouse_listener.start()
        # self.mouse_listener.join()

        cursor_locations = [
            (554, 212),
            (612, 523),
            (1237, 283),
            (1197, 274),
            (838, 529),
            (1054, 588),
            (1137, 603),
            (1137, 603),
            (684, 570),
            (1254, 265),
            (1131, 339),
            (931, 587),
            (1264, 265),
            (1123, 330),
            (1176, 649),
            (664, 574),
            (775, 694),
            (1163, 578),
            (1163, 578),
            (1163, 577),
            (1163, 577),
            (1163, 577),
            (1163, 577),
            (1163, 577),
            (1163, 577),
            (1163, 577),
            (664, 574),
            (775, 774),
            (1318, 139),
            (882, 553),
        ]

        time.sleep(10)
        for i, location in enumerate(cursor_locations):
            self.mouse.position = location
            time.sleep(0.5)
            if i != 15 and i != 26:
                self.mouse.click(mouse.Button.left, 1)
                time.sleep(0.5)
            
            # Enter in file path for audio
            if i == 4:
                for char in self.aligner_path:
                    self.keyboard.press(char)
                    self.keyboard.release(char)
            elif i == 11:
                for char in self.audio_path:
                    self.keyboard.press(char)
                    self.keyboard.release(char)
            elif i == 15 or i == 26:
                self.mouse.click(mouse.Button.right, 1)
                time.sleep(0.5)
            elif i == 24:
                time.sleep(10)
                with self.keyboard.pressed(Key.alt):
                    self.keyboard.press(Key.f4)
                    self.keyboard.release(Key.f4)

    def move_timings_and_parsings(self):
        self.parsings_dir = r'C:\Users\brand\OneDrive\Documents\App Builder\Reading Apps\Phrases\org.branhub.textaligner'
        to_parsings_path = os.path.join(self.problem_dir, 'parsings.txt')
        for filename in os.listdir(self.parsings_dir):
            if filename.endswith('.txt'):
                
                shutil.copy2(os.path.join(self.parsings_dir, filename), to_parsings_path)

            # Remove all files from aneas parsings directory
            # so the next time a parsing is created, we can grab
            # the singular text file without having to worry about
            # any others
            os.remove(os.path.join(self.parsings_dir, filename))


        self.timings_dir = r'C:\Users\brand\OneDrive\Documents\App Builder\Reading Apps\Timings\org.branhub.textaligner'
        to_timings_path = os.path.join(self.problem_dir, 'timings.txt')
        for filename in os.listdir(self.timings_dir):
            if filename.endswith('.txt'):
                shutil.copy2(os.path.join(self.timings_dir, filename), to_timings_path)
            
            # Remove all files from aneas timings directory
            # so the next time a timing is created, we can grab
            # the singular text file without having to worry about
            # any others
            os.remove(os.path.join(self.timings_dir, filename))

        alignment_fixer = AlignmentFileFixer(parsings_path=to_parsings_path, timings_path=to_timings_path)
        alignment_fixer.run()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            print(self.mouse.position)



# ForcedAligner()