from copy import deepcopy

from tree import Tree

def split(text: str) -> list[str]:
    replaced = []
    for char in text:
        if char == '-':
            continue
        elif char.isalpha():
            replaced.append(char.lower())
        else:
            replaced.append(' ')
    IGNORED = ['and', 'for', 'of', 'from', 'to', 'the', 'in', 'is', 'or', 'a', 'these', 'this', 'their', 'by', 'be', 'will', 'at', 'work', 'on', 'as', 'are', 'you', 'module', 'application']
    split = list(filter(lambda t: len(t) > 2 and t not in IGNORED, ''.join(replaced).split(' ')))

    # Remove plurals
    for i in range(0, len(split)):
        if split[i][-3:] == 'ies':
            split[i] = split[i][:-3] + 'y' # Just hope no lecturer put pies in their module information
        elif split[i][-2:] == '\'s':
            split[i] = split[i][:-2]
        elif split[i][-1] == 's':
            split[i] = split[i][:-1]
    return split

def _find_all(word: str, words: list[str]) -> list[int]:
    return [i for (i, w) in enumerate(words) if w == word]

def _get_spread(word: str, words: list[str], spread: int) -> set[str]:
    spread_words = set()
    for index in _find_all(word, words):
        for i in range(max(0, index-spread), min(len(words)-1, index+spread+1)):
            spread_words.add(words[i])
    return spread_words

def _compare(words1: list[str], words2: list[str], shared: set[str], ignore: set[str], spread: int) -> Tree:
    tree = Tree()
    for word in shared:
        new_words1 = _get_spread(word, words1, spread)
        new_words2 = _get_spread(word, words2, spread)

        new_ignore = deepcopy(ignore)
        new_ignore.add(word)
        shared = new_words1.intersection(new_words2).difference(new_ignore)
        branch = _compare(words1, words2, shared, new_ignore, spread)
        branch.name = word
        tree.add_branch(branch)
    return tree

def compare(words1: list[str], words2: list[str], spread: int = 2) -> Tree:
    shared = set(words1).intersection(set(words2))
    return _compare(words1, words2, shared, set(), spread)
