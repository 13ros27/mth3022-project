from PyPDF2 import PdfReader
from os import listdir

import cache, words
from graph import Graph

@cache.cache
def read_syllabus_plan(file: str, *, start: str = 'SYLLABUS PLAN - summary of the structure and academic content of the module', end: str = 'LEARNING AND TEACHING'):
    pages = PdfReader(file).pages
    text = '\n'.join([page.extract_text() for page in pages])
    return text[text.find(start) + len(start):text.find(end)]

def read_all_files(folder: str, *, start: str = 'SYLLABUS PLAN - summary of the structure and academic content of the module', end: str = 'LEARNING AND TEACHING') -> dict[str, str]:
    return {f[f.find('MTH'):f.find('MTH')+7]: read_syllabus_plan(folder + '/' + f, start=start, end=end) for f in listdir(folder)}

if __name__ == '__main__':
    words_map = {k: words.split(v) for (k, v) in read_all_files('C:/Users/willi/Downloads/ModuleInfo').items()}
    depths = {}
    for (k1, v1) in words_map.items():
        for (k2, v2) in words_map.items():
            if k1 < k2:
                tree = words.compare(v1, v2)
                depths[(k1, k2)] = tree.depth()
    print(Graph.from_depth(depths, 5).to_wolfram())
