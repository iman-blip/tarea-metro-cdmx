import math

# 1. CLASES BASE (Problem y Node)
class Problem:
    """Clase base para modelar el problema de búsqueda en el Metro de la CDMX."""
    def __init__(self, initial_state, goal_state, graph, coordinates=None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.graph = graph
        self.coordinates = coordinates or {}

    def actions(self, state):
        """Devuelve los transbordos o estaciones vecinas directas."""
        return list(self.graph.get(state, {}).keys())

    def result(self, state, action):
        """La estación a la que llegas tras moverte."""
        return action

    def is_goal(self, state):
        """Revisa si ya llegamos a la estación destino."""
        return state == self.goal_state

    def value(self, state):
        """
        Función de evaluación (Heurística) para Hill Climbing.
        Calcula la distancia euclidiana en línea recta hacia la estación destino.
        Se usa en negativo porque Hill Climbing busca maximizar la función.
        """
        if not self.coordinates or self.goal_state not in self.coordinates:
            return 0

        x1, y1 = self.coordinates[state]
        x2, y2 = self.coordinates[self.goal_state]
        # Distancia en línea recta
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return -distance


class Node:
    """Clase para representar cada estación/estado en el camino."""
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def expand(self, problem):
        """Genera los nodos de las estaciones vecinas accesibles."""
        return [
            Node(
                state=problem.result(self.state, action),
                parent=self,
                action=action,
                path_cost=self.path_cost + problem.graph[self.state][action]
            )
            for action in problem.actions(self.state)
        ]

    def path(self):
        """Arma la lista completa del camino recorrido desde el origen."""
        node, path_back = self, []
        while node:
            path_back.append(node.state)
            node = node.parent
        return list(reversed(path_back))


# 2. ALGORITMO HILL CLIMBING
def hill_climbing(problem):
    """
    Algoritmo de Búsqueda Local por Escalamiento de Cima (Hill Climbing).
    Evalúa a los vecinos directos y avanza hacia la estación con mejor valor.
    Se detiene si llega al destino o si cae en un máximo local.
    """
    current = Node(problem.initial_state)
    
    while True:
        if problem.is_goal(current.state):
            return current.path(), current.path_cost

        neighbors = current.expand(problem)
        if not neighbors:
            break

        # Seleccionamos al vecino que mejor nos acerque al destino (menor distancia)
        best_neighbor = max(neighbors, key=lambda node: problem.value(node.state))

        # Si el mejor vecino no mejora la distancia de la estación actual, el algoritmo se atora
        if problem.value(best_neighbor.state) <= problem.value(current.state):
            break

        current = best_neighbor

    return current.path(), current.path_cost
