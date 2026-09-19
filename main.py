from collections import deque

# Clase base para problemas de búsqueda
class Problem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return self.goal == state

# Adaptación para grafos
class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, state):
        return list(self.graph[state].keys())

    def result(self, state, action):
        return action

    def action_cost(self, state1, action, state2):
        return self.graph[state1][state2]

# Estructura del nodo
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def path(self):
        lista_path = []
        node = self
        while node:
            lista_path.append(node.state)
            node = node.parent
        return lista_path[::-1]

    def expand(self, problem):
        lista = []
        for action in problem.actions(self.state):
            lista.append(self.child_node(problem, action))
        return lista

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        step_cost = problem.action_cost(self.state, action, next_state)
        return Node(next_state, self, action, self.path_cost + step_cost)

# Algoritmo DFS (Profundidad)
def depth_first_graph_search(problem):
    start_node = Node(problem.initial)
    if problem.is_goal(start_node.state):
        return start_node
    frontier = [start_node]
    explored = set()

    while frontier:
        node = frontier.pop()
        explored.add(node.state)

        if problem.is_goal(node.state):
            return node

        for child in node.expand(problem):
            if child.state not in explored and not any(n.state == child.state for n in frontier):
                frontier.append(child)
    return None

# Algoritmo BFS (Anchura)
def breadth_first_graph_search(problem):
    start_node = Node(problem.initial)
    if problem.is_goal(start_node.state):
        return start_node
    frontier = deque([start_node])
    explored = set()

    while frontier:
        node = frontier.popleft()
        explored.add(node.state)

        if problem.is_goal(node.state):
            return node

        for child in node.expand(problem):
            if child.state not in explored and not any(n.state == child.state for n in frontier):
                frontier.append(child)
    return None

# Grafo del metro simplificado (costo 1 por estacion)
metro = {
    'Cuatro Caminos': {'Tacuba': 1},
    'Tacuba': {'Cuatro Caminos': 1, 'Hidalgo': 1, 'Tacubaya': 1},
    'Hidalgo': {'Tacuba': 1, 'Bellas Artes': 1, 'Balderas': 1, 'La Raza': 1},
    'Bellas Artes': {'Hidalgo': 1, 'Pino Suárez': 1, 'Salto del Agua': 1},
    'Pino Suárez': {'Bellas Artes': 1, 'Pantitlán': 1, 'Chabacano': 1},
    'Pantitlán': {'Pino Suárez': 1, 'Oceanía': 1, 'Jamaica': 1},
    'Politécnico': {'La Raza': 1},
    'La Raza': {'Politécnico': 1, 'Hidalgo': 1, 'Consulado': 1},
    'Balderas': {'Hidalgo': 1, 'Centro Médico': 1, 'Tacubaya': 1},
    'Centro Médico': {'Balderas': 1, 'Zapata': 1, 'Chabacano': 1},
    'Zapata': {'Centro Médico': 1, 'Ermita': 1, 'Mixcoac': 1},
    'Ermita': {'Zapata': 1, 'Taxqueña': 1, 'Chabacano': 1},
    'Taxqueña': {'Ermita': 1},
    'Oceanía': {'Pantitlán': 1, 'Consulado': 1, 'San Lázaro': 1},
    'Consulado': {'La Raza': 1, 'Oceanía': 1, 'Morelos': 1},
    'San Lázaro': {'Oceanía': 1, 'Pino Suárez': 1, 'Morelos': 1},
    'Morelos': {'Consulado': 1, 'San Lázaro': 1},
    'Chabacano': {'Pino Suárez': 1, 'Centro Médico': 1, 'Ermita': 1, 'Jamaica': 1},
    'Jamaica': {'Chabacano': 1, 'Pantitlán': 1},
    'Tacubaya': {'Tacuba': 1, 'Balderas': 1, 'Mixcoac': 1},
    'Mixcoac': {'Tacubaya': 1, 'Zapata': 1},
    'Salto del Agua': {'Bellas Artes': 1, 'Balderas': 1}
}

# --- PRUEBAS DE LAS 3 RUTAS ---

# 1. Cuatro Caminos -> Pantitlan
prob1 = GraphProblem('Cuatro Caminos', 'Pantitlán', metro)
sol_bfs1 = breadth_first_graph_search(prob1)
sol_dfs1 = depth_first_graph_search(prob1)

print("Ruta 1: Cuatro Caminos a Pantitlan")
print("BFS:", sol_bfs1.path())
print("DFS:", sol_dfs1.path())
print("-" * 40)

# 2. Politécnico -> Taxqueña
prob2 = GraphProblem('Politécnico', 'Taxqueña', metro)
sol_bfs2 = breadth_first_graph_search(prob2)
sol_dfs2 = depth_first_graph_search(prob2)

print("Ruta 2: Politecnico a Taxqueña")
print("BFS:", sol_bfs2.path())
print("DFS:", sol_dfs2.path())
print("-" * 40)

# 3. Zapata -> Oceanía
prob3 = GraphProblem('Zapata', 'Oceanía', metro)
sol_bfs3 = breadth_first_graph_search(prob3)
sol_dfs3 = depth_first_graph_search(prob3)

print("Ruta 3: Zapata a Oceania")
print("BFS:", sol_bfs3.path())
print("DFS:", sol_dfs3.path())