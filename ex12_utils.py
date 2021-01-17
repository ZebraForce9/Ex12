from typing import Dict, List, Tuple, Optional, NewType

LEGAL_MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
Path = NewType('Path', List[Tuple[int, int]])


def load_words_dict(file_path: str) -> Dict[str, bool]:
    """
    Load words for game from a file into a dictionary.

    Args:
        file_path: The path to the words file.

    Returns:
        A dictionary with all the words for the game.
    """
    words_dict = {}

    with open(file_path) as words_file:
        for line in words_file:
            words_dict[line[:-1]] = True

    return words_dict


def is_valid_path(board: List[List[str]], path: Path, words: Dict[str, bool]) -> Optional[str]:
    """
    Check if a given path follows the rules of the game, is within the board and produces a word from the dictionary.

    Args:
        board: The game board.
        path: The given path to check.
        words: A dictionary with all the words for the game.

    Returns:
        The word the path produces if it's legal, None otherwise.
    """
    if len(path) != len(set(path)):
        return

    word = ''

    for j, coordinate in enumerate(path):
        if not 0 <= coordinate[0] <= 3 or not 0 <= coordinate[1] <= 3:
            return

        letter = board[coordinate[0]][coordinate[1]]

        if j == len(path)-1:
            word += letter
            break

        difference = (coordinate[0] - path[j+1][0], coordinate[1] - path[j+1][1])

        if difference not in LEGAL_MOVES:
            return

        word += letter

    if word in words:
        return word


def find_length_n_words(n: int, board: List[List[str]], words: Dict[str, bool]) -> List[Tuple[str, Path]]:
    """
    Find all words from the dictionary that appear on the board and are created from 'n' squares.

    Args:
        n: Number of squares needed to create a word.
        board: The game board.
        words: A dictionary with all the words for the game.

    Returns:
        A list of tuples, each containing the word and a path to the word.
    """
    letters = create_letters_dict(board)
    n_words = []

    for word in words:
        beginnings = create_word_beginnings(word)
        for beginning in beginnings:
            if beginning in letters:
                locations = letters[beginning]
                paths = find_word_paths(n, board, word, beginning, locations)
                for path in paths:
                    n_words.append((word, path))

    return n_words


def find_word_paths(n: int, board: List[List[str]], word: str, beginning: str,
                    locations: List[Tuple[int, int]]) -> List[Path]:
    """
    Find all the paths that create a word.

    Args:
        n: Number of squares needed to create a word.
        board: The game board.
        word: The word we look for.
        beginning: The beginning of the word. Changes from the first letter up to all the letters except the last 2.
        locations: Where on the board the beginnings are located.

    Returns:
        A list with the paths.
    """
    paths = []

    for location in locations:
        temp_word = beginning
        current_path = [location]
        _find_word_paths_helper(n, board, word, location, paths, temp_word, current_path)

    return paths


def _find_word_paths_helper(n: int, board: List[List[str]], word: str, location: Tuple[int, int],
                            paths: List[Path], temp_word: str, current_path: Path):
    """
    A recursive helper function for 'find_word_paths'.
    """
    if temp_word == word and len(current_path) == n:
        paths.append(current_path[:])
        return

    for move in LEGAL_MOVES:
        next_location = (location[0] + move[0], location[1] + move[1])
        if not 0 <= next_location[0] <= 3 or not 0 <= next_location[1] <= 3:
            continue

        next_letter = board[next_location[0]][next_location[1]]
        length = len(temp_word) + len(next_letter)

        if temp_word + next_letter == word[:length]:
            current_letter = board[location[0]][location[1]]
            board[location[0]][location[1]] = '*'
            temp_word += next_letter
            current_path.append(next_location)

            _find_word_paths_helper(n, board, word, next_location, paths, temp_word, current_path)

            current_path.pop()
            temp_word = temp_word[:-len(next_letter)]
            board[location[0]][location[1]] = current_letter


def create_letters_dict(board: List[List[str]]) -> Dict[str, List[Tuple[int, int]]]:
    """
    Create a dictionary with all the letters on the board and their locations.

    Args:
        board: The game board.

    Returns:
        The created dictionary.
    """
    letters = {}

    for i, line in enumerate(board):
        for j, letter in enumerate(line):
            if letter not in letters:
                letters[letter] = [(i, j)]
            else:
                letters[letter].append((i, j))

    return letters


def create_word_beginnings(word: str) -> List[str]:
    """
    Create all possible beginnings for a word - from the first letter up to all the letters except the last 2.

    Args:
        word: The word we work on.

    Returns:
        A list with all the beginnings.
    """
    beginnings = []

    for j, letter in enumerate(word):
        if j == len(word) - 2:
            break
        beginnings.append(word[:j+1])

    return beginnings
