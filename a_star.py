
# Nama : Brilliant Irano Mardin
# NIM  : 32602200140
# Mata Kuliah : Kecerdasan Buatan_FKCBD_20251

import heapq
import math

# Graph dan koordinat node (untuk heuristic)
graph = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 4), ('E', 1)],
    'C': [('F', 2)],
    'D': [('G', 2)],
    'E': [('G', 5)],
    'F': [('G', 1)],
    'G': []
}

coords = {
    'A': (0, 0),
    'B': (2, 1),
    'C': (1, 4),
    'D': (4, 2),
    'E': (3, 0),
    'F': (5, 4),
    'G': (6, 1)
}


def heuristic(node, goal):
    """
    Heuristic h(n): jarak Euclidean dari node ke goal.
    """
    x1, y1 = coords[node]
    x2, y2 = coords[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def a_star(graph, start, goal):
    """
    Implementasi algoritma A* (A Star Search).
    f(n) = g(n) + h(n)
    - g(n): cost dari start ke node n
    - h(n): heuristic dari n ke goal
    """
    frontier = []
    g_cost = {start: 0}
    f_start = g_cost[start] + heuristic(start, goal)
    heapq.heappush(frontier, (f_start, start))

    parent = {start: None}

    while frontier:
        f_current, current = heapq.heappop(frontier)
        # print(f"A* mengunjungi: {current} dengan f={f_current}, g={g_cost[current]}")

        if current == goal:
            break

        for neighbor, edge_cost in graph[current]:
            tentative_g = g_cost[current] + edge_cost

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_neighbor = tentative_g + heuristic(neighbor, goal)
                parent[neighbor] = current
                heapq.heappush(frontier, (f_neighbor, neighbor))

    if goal not in parent:
        return None, float('inf')

    # Rekonstruksi path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path, g_cost[goal]


def main():
    start = 'A'
    goal = 'G'
    print("=== A* Search (Heuristic Search) ===")
    path, cost = a_star(graph, start, goal)
    if path:
        print(f"Path A* dari {start} ke {goal}: {path}")
        print(f"Total cost (g): {cost}")
    else:
        print("Goal tidak ditemukan dengan A*.")


if __name__ == "__main__":
    main()
