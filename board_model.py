from ex12_utils import *
from boggle_board_randomizer import *
from typing import Tuple


class BoardModel:
    def __init__(self):
        self.__board = randomize_board()
        self.__words = load_words_dict('boggle_dict.txt')
        self.__path = []
        self.__words_found = {}

    def randomize_board_ours(self):
        self.__board = randomize_board()

    def get_board_letters(self):
        return [letter for line in self.__board for letter in line]

    def update_path(self, coordinate: Tuple[int, int]):
        self.__path.append(coordinate)

    def add_word(self, word: str):
        self.__words_found[word] = True

    def check_path(self):
        return is_valid_path(self.__board, self.__path, self.__words)

    def clear_path(self):
        del self.__path[:]

    def clear_words_found(self):
        self.__words_found = {}

    def get_words_found(self):
        return self.__words_found

    def get_path_length(self) -> int:
        return len(self.__path)
