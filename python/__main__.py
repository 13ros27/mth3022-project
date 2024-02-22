from PyPDF2 import PdfReader
from os import listdir

from cache import cache

@cache
def read_syllabus_plan(file: str, *, start: str = 'SYLLABUS PLAN - summary of the structure and academic content of the module', end: str = 'LEARNING AND TEACHING'):
    pages = PdfReader(file).pages
    text = '\n'.join([page.extract_text() for page in pages])
    return text[text.find(start) + len(start):text.find(end)]

def read_all_files(folder: str, *, start: str = 'SYLLABUS PLAN - summary of the structure and academic content of the module', end: str = 'LEARNING AND TEACHING') -> dict[str, str]:
    return {f[f.find('MTH'):f.find('MTH')+7]: read_syllabus_plan(folder + '/' + f, start=start, end=end) for f in listdir(folder)}

def words(text: str) -> list[str]:
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

if __name__ == '__main__':
    print([words(t) for t in read_all_files('C:/Users/willi/Downloads/ModuleInfo/').values()])
