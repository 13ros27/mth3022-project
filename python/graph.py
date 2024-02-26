class Graph:
	def __init__(self, undirected: bool = True):
		self.vertices = set()
		self.edges = []
		self.undirected = undirected

	def to_wolfram(self) -> str:
		edges = []
		for (a, b) in self.edges:
			if self.undirected:
				edges.append(a + '\\[UndirectedEdge]' + b)
			else:
				edges.append(a + '->' + b)
		return 'dg = Graph[{' + ','.join(self.vertices) + '}, {' + ','.join(edges) + '}];'

	@staticmethod
	def from_depth(depths: dict[(str, str), int], min_depth: int):
		this = Graph(undirected = True)
		for ((a, b), depth) in depths.items():
			this.vertices.add(a)
			this.vertices.add(b)
			if depth >= min_depth:
				this.edges.append((a, b))
		return this
