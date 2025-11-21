# Nama : Brilliant Irano Mardin
# NIM  : 32602200140
# Mata Kuliah : Kecerdasan Buatan_FKCBD_20251

from collections import deque
import heapq

# Graph contoh: tiap edge berupa (neighbor, cost)
graph = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 4), ('E', 1)],
    'C': [('F', 2)],
    'D': [('G', 2)],
    'E': [('G', 5)],
    'F': [('G', 1)],
    'G': []
}

def bfs(graph, start, goal):
    """
    Implementasi Breadth-First Search (BFS)
    Assume semua edge punya cost sama (1 langkah).
    Mengembalikan path (list node) dari start ke goal.
    """
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        # print(f"BFS mengunjungi: {current}")

        if current == goal:
            break

        for neighbor, _ in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # Rekonstruksi path
    if goal not in parent:
        return None  # goal tidak tercapai

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def ucs(graph, start, goal):
    """
    Implementasi Uniform Cost Search (UCS).
    Menggunakan priority queue (min-heap).
    Mengembalikan (path, total_cost).
    """
    frontier = []
    heapq.heappush(frontier, (0, start))  # (cost, node)
    cost_so_far = {start: 0}
    parent = {start: None}

    while frontier:
        current_cost, current = heapq.heappop(frontier)
        # print(f"UCS mengunjungi: {current} dengan cost {current_cost}")

        if current == goal:
            break

        for neighbor, edge_cost in graph[current]:
            new_cost = current_cost + edge_cost

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(frontier, (new_cost, neighbor))

    if goal not in parent:
        return None, float('inf')

    # Rekonstruksi path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path, cost_so_far[goal]


def main():
    start = 'A'
    goal = 'G'

    print("=== BFS (Blind Search) ===")
    bfs_path = bfs(graph, start, goal)
    if bfs_path:
        print(f"Path BFS dari {start} ke {goal}: {bfs_path}")
        print(f"Jumlah langkah: {len(bfs_path) - 1}")
    else:
        print("Goal tidak ditemukan dengan BFS.")

    print("\n=== UCS (Blind Search) ===")
    ucs_path, ucs_cost = ucs(graph, start, goal)
    if ucs_path:
        print(f"Path UCS dari {start} ke {goal}: {ucs_path}")
        print(f"Total cost: {ucs_cost}")
    else:
        print("Goal tidak ditemukan dengan UCS.")


if __name__ == "__main__":
    main()
