from __future__ import annotations

import tkinter as tk
from forced_aligner import ForcedAligner
from video_mapper import video_map

DROP_DOWN_WIDTH = 50

TYPE_DROP_X = 10
TYPE_DROP_Y = 200

TITLE_DROP_X = TYPE_DROP_X + DROP_DOWN_WIDTH + 499
TITLE_DROP_Y = TYPE_DROP_Y


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')
        self.root.geometry('1920x1080')
        self.root.title('Video Selector')

        self.selected_title = None

        self.title_entry = None
        self.min_title_length = 5
        self.max_title_length = 70
        self.video_type_menu = None
        self.type_drop_down = None
        self.video_title_menu = None
        self.title_drop_down = None
        self.outline_button = None
        self.video_button = None

        self.generate_widgets()

        self.root.register(self.validate_title)

    def generate_widgets(self):
        self.create_title_entry()
        self.create_video_type_drop_down()
        self.create_video_title_drop_down()
        self.create_outline_button()
        self.create_video_button()

    def create_title_entry(self):
        label = tk.Label(self.root, text='', font=('Arial', 18))
        label.pack(padx=20, pady=20)

        def handle_focus_in(_):
            self.title_entry.delete(0, tk.END)
            self.title_entry.config(fg='black')

        self.title_entry = tk.Entry(
            self.root,
            width=100,
            font=('Arial', 16),
            validate='all',
            validatecommand=(self.validate_title, '%P'),
        )
        self.title_entry.insert(0, 'Create a title')
        self.title_entry.config(fg='grey')
        self.title_entry.pack()

        self.title_entry.bind('<FocusIn>', handle_focus_in)

    def validate_title(self, title):
        if len(title) < self.min_title_length or len(title) > self.max_title_length:
            return False
        return True

    def create_video_type_drop_down(self):
        self.video_type_menu = tk.StringVar()
        self.video_type_menu.set('Select video topic')

        options = {video_map[key]['type'] for key in video_map}

        self.type_drop_down = tk.OptionMenu(
            self.root,
            self.video_type_menu,
            *options,
            command=self.type_selected,
        )
        self.type_drop_down.configure(width=DROP_DOWN_WIDTH)
        self.type_drop_down.place(x=TYPE_DROP_X, y=TYPE_DROP_Y)

    def type_selected(self, selected_type):
        options = {
            video_map[video]['title']
            for video in video_map if video_map[video]['type'] == selected_type
        }
        self.create_video_title_drop_down(options)

    def create_video_title_drop_down(self, options=['']):
        self.video_title_menu = tk.StringVar()
        self.video_title_menu.set('Select a Video')

        self.title_drop_down = tk.OptionMenu(
            self.root,
            self.video_title_menu,
            *options,
            command=self.title_selected,
        )
        self.title_drop_down.configure(width=DROP_DOWN_WIDTH)
        self.title_drop_down.place(x=TITLE_DROP_X, y=TITLE_DROP_Y)

    def title_selected(self, selected_title):
        self.selected_title = selected_title

    def create_outline_button(self):
        self.outline_button = tk.Button(
            self.root, text='Create outline', font=(
            'Arial', 18,
            ), width=30, command=self.create_outline,
        )
        self.outline_button.place(
            x=SCREEN_WIDTH // 2 - 250, y=SCREEN_HEIGHT // 2,
        )

    def create_outline(self):
        forced_aligner = ForcedAligner(title=self.selected_title)
        forced_aligner.run()

    def create_video_button(self):
        self.video_button = tk.Button(
            self.root, text='Create video', font=(
            'Arial', 18,
            ), width=30, command=self.create_video,
        )
        self.video_button.place(
            x=SCREEN_WIDTH // 2 -
            250, y=SCREEN_HEIGHT // 2 + 100,
        )

    def create_video(self):
        pass


if __name__ == '__main__':
    app = App()
    app.root.mainloop()

    # forced_aligner = ForcedAligner(title=app.selected_title)
