class Graph:
    def __init__(self, undirected: bool = True):
        self.vertices = set()
        self.edges = []
        self.labels = []
        self.undirected = undirected

    def to_wolfram(self) -> str:
        edges = []
        for (a, b) in self.edges:
            if self.undirected:
                edges.append(a + '\\[UndirectedEdge]' + b)
            else:
                edges.append(a + '->' + b)
        labels = ''
        if self.labels:
            labels = ', EdgeLabels -> {' + ','.join(map(str, self.labels)) + '}'
        return 'dg = Graph[{' + ','.join(self.vertices) + '}, {' + ','.join(edges) + '}' + labels + '];'

    def to_rdf(self, label: str) -> str:
        if self.undirected:
            return 'rdf = RDFStore[{' + ','.join([f'RDFTriple[ex["{b}"], ex["{label}"], ex["{a}"]]' for (a, b) in self.edges]) + '}]'
        else:
            return 'rdf = RDFStore[{' + ','.join([f'RDFTriple[ex["{a}"], ex["{label}"], ex["{b}"]]' for (a, b) in self.edges]) + '}]'

    @staticmethod
    def from_depth(depths: dict[(str, str), int], min_depth: int):
        this = Graph(undirected = True)
        for ((a, b), depth) in depths.items():
            this.vertices.add(a)
            this.vertices.add(b)
            if depth >= min_depth:
                this.edges.append((a, b))
        return this

    @staticmethod
    def from_depth_conns(depths: dict[(str, str), int], connections: int):
        this = Graph(undirected = False)
        edges = {}
        for ((a, b), depth) in depths.items():
            this.vertices.add(a)
            this.vertices.add(b)

            if edges.get(a) is None:
                edges[a] = {b: depth}
            elif len(edges[a]) < connections:
                edges[a][b] = depth
            elif depth > min(edges[a].values()):
                for (name, val) in edges[a].items():
                    if val < depth:
                        del edges[a][name]
                        edges[a][b] = depth
                        break

            if edges.get(b) is None:
                edges[b] = {a: depth}
            elif len(edges[b]) < connections:
                edges[b][a] = depth
            elif depth > min(edges[b].values()):
                for (name, val) in edges[b].items():
                    if val < depth:
                        del edges[b][name]
                        edges[b][a] = depth
                        break

        for (a, contents) in edges.items():
            for (b, depth) in contents.items():
                this.edges.append((a, b))
                this.labels.append(depth)
        return this;
