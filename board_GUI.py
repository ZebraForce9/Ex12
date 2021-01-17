import tkinter as tk
from typing import List

WELCOME_MESSAGE = 'Welcome\n Press "New Game" to start'


class BoardGUI:
    def __init__(self) -> None:
        self.__root = tk.Tk()
        self.__root.title('Boggle')
        self.__root.resizable(False, False)
        self.__letter_buttons = []
        self.__timer = ['3', '00']
        self.__timer_stopped = True

        self.__upper_frame = tk.Frame(self.__root)
        self.__display = tk.Label(self.__upper_frame, text=WELCOME_MESSAGE, height=3, relief='ridge')

        self.__mid_frame = tk.Frame(self.__root)
        self.__score = tk.Label(self.__mid_frame, text=0, height=5)
        self.__timer_label = tk.Label(self.__mid_frame, text='3:00', height=5)
        self.__new_game = tk.Button(self.__mid_frame, text='New Game', height=5, bg='lightgrey')
        self.__end_game = tk.Button(self.__mid_frame, text='End Game', height=5, bg='lightgrey')

        self.__lower_frame = tk.Frame(self.__root)
        self.__words_found = tk.Label(self.__lower_frame, height=3, wraplength=500)

        self.pack_board()

        self.create_buttons()

    def clear_board(self):
        for button in self.__letter_buttons:
            button.configure(state='normal', bg='lightgrey')
        self.__display['text'] = ''

    def reset_stats(self):
        self.__words_found['text'] = ''
        self.__score['text'] = 0

    def set_display(self, text):
        self.__display['text'] = text

    def set_words_found(self, word: str):
        self.__words_found['text'] = self.__words_found['text'] + word + ', '

    def pack_board(self) -> None:
        self.__upper_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__display.pack(fill=tk.BOTH, expand=True)

        self.__score.grid(row=0, column=4)
        self.__timer_label.grid(row=1, column=4)
        self.__new_game.grid(row=2, column=4)
        self.__end_game.grid(row=3, column=4)

        self.__mid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__lower_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__words_found.pack(side=tk.LEFT)

    def create_buttons(self) -> None:
        for i in range(4):
            for j in range(4):
                button = tk.Button(self.__mid_frame, state='disabled', height=5, width=15, borderwidth=1, bg='lightgrey')
                button.grid(row=i, column=j)
                self.__letter_buttons.append(button)

    def update_timer(self):
        self.__timer_stopped = False

        if self.__timer[0] != '0' and self.__timer[1] == '00':
            self.__timer[0] = str(int(self.__timer[0]) - 1)
            self.__timer[1] = '59'

        elif self.__timer[1] == '10':
            self.__timer[1] = '09'

        elif self.__timer[1][0] == '0' and int(self.__timer[1][1]) < 10:
            self.__timer[1] = '0' + str(int(self.__timer[1][1]) - 1)

        elif self.__timer[1] != '00':
            self.__timer[1] = str(int(self.__timer[1]) - 1)

        if self.__timer[0] == '0' and self.__timer[1] == '00':
            self.__timer_label['text'] = ':'.join(self.__timer)
            for button in self.__letter_buttons:
                button['state'] = 'disabled'
            self.__display['text'] = 'Well played, press "New Game" to play again'
            self.__timer_stopped = True
            return

        self.__timer_label['text'] = ':'.join(self.__timer)
        self.__root.after(1000, self.update_timer)

    def set_score(self, num: int):
        self.__score['text'] = self.__score['text'] + num

    def timer_stopped(self):
        return self.__timer_stopped

    def get_buttons(self) -> List[tk.Button]:
        return self.__letter_buttons

    def get_display(self):
        return self.__display['text']

    def get_root(self):
        return self.__root

    def get_new_game(self):
        return self.__new_game

    def get_end_game(self):
        return self.__end_game

    def set_timer(self, time):
        self.__timer = time

    def run(self) -> None:
        self.__root.mainloop()
