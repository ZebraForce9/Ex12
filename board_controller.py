from board_GUI import *
from board_model import *


class BoardController:
    def __init__(self):
        self.__gui = BoardGUI()
        self.__model = BoardModel()
        self.__buttons = self.__gui.get_buttons()
        self.__timer_running = False

        root = self.__gui.get_root()
        root.bind('<space>', self.press_space)
        self.__gui.get_new_game()['command'] = self.press_new_game
        self.__gui.get_end_game()['command'] = self.press_end_game

    def press_space(self, event):
        word = self.__model.check_path()
        if word and word not in self.__model.get_words_found():
            self.__model.add_word(word)
            score = self.__model.get_path_length() ** 2
            self.__gui.set_score(score)
            self.__gui.set_words_found(word)
        self.__gui.clear_board()
        self.__model.clear_path()

    def press_new_game(self):
        if self.__gui.timer_stopped():
            self.__timer_running = False
        self.__model.randomize_board_ours()
        self.__gui.clear_board()
        self.set_buttons_text()
        self.__gui.set_timer(['3', '00'])
        if not self.__timer_running:
            self.__timer_running = True
            self.__gui.update_timer()
        self.__model.clear_words_found()
        self.__model.clear_path()
        self.__gui.reset_stats()

    def press_end_game(self):
        for button in self.__buttons:
            button['state'] = 'disabled'
        self.__gui.set_timer(['0', '01'])

    def set_buttons_text(self):
        letters = self.__model.get_board_letters()

        for i, button in enumerate(self.__buttons):
            text = letters[i]

            button['text'] = text

            action = self.create_button_action(text, i)

            button['command'] = action
            button['state'] = 'normal'

    def create_button_action(self, letter, index):

        def update_display():
            self.__gui.set_display(self.__gui.get_display() + letter)
            button = self.__buttons[index]
            button.configure(state='disabled', bg='deepskyblue')
            info = button.grid_info()
            self.__model.update_path((info['row'], info['column']))

        return update_display

    def run(self):
        self.__gui.run()


if __name__ == '__main__':
    x = BoardController()
    x.run()
