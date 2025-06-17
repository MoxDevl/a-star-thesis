from queue import PriorityQueue

# СЧИТАЕМ, ЧТО ГРАФ ЯВЛЯЕТСЯ СЕТКОЙ,
# ГДЕ ОТ ВЕРШИНЫ МОЖНО ДВИГАТЬСЯ ВВЕРХ, ВПРАВО, ВНИЗ, ВЛЕВО 

class GridNode:
    def __init__(self, new_x, new_y) -> None:
        self.x = new_x
        self.y = new_y
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    # Прописано, для использования PriorityQueue
    def __lt__(self, other):
        return self.x<other.x and self.y<other.y
    

# Возвращает список прилежащих к node вершин
# node - вершина, вокруг которой ищут прилегающие вершины
# width - ширина сетки графа
# height - высота сетки графа
def find_neighbours(node: GridNode, width: int, height: int) -> list[GridNode]:
    res = []
    if node.x>0:
        res.append(GridNode(node.x-1, node.y))
    if node.y>0:
        res.append(GridNode(node.x, node.y-1))
    if node.x<width-1:
        res.append(GridNode(node.x+1, node.y))
    if node.y<height-1:
        res.append(GridNode(node.x, node.y+1))
    return res

# манхэттенское расстояние между точками a и b;
# start и finish - вершины, между которыми нужно найти расстояние
def man_heuristic(start: GridNode, finish: GridNode) -> int:
    return abs(finish.x-start.x)+abs(finish.y-start.y)

# start - стартовая вершина;
# finish - конечная вершина;
# graph - список булевых списков, имитирующий матрицу вершин,
# значения False в graph имитируют стены, то есть вершины, в которые нельзя перейти из соседней вершины
def a_star(start: GridNode, finish: GridNode, graph: list[list[bool]]) -> list[GridNode]:
    if start==finish:
        raise ValueError('start and finish should be different Nodes')
    width = len(graph[0])
    height = len(graph)

    frontier = PriorityQueue()
    came_from = [[None]*width for x in range(height)]
    cost = [[float('inf')]*width for x in range(height)]

    frontier.put([0, start])
    cost[start.y][start.x] = 0

    while not frontier.empty():
        curr = frontier.get()[1]
        if  curr == finish:
            break
        near = find_neighbours(curr, width, height)
        for n in near:
            # проверка на стену
            if not graph[n.y][n.x]:
                continue
            # если не стена, то делаем по обычному
            n_cost = cost[curr.y][curr.x]+1
            if n_cost<cost[n.y][n.x]:
                cost[n.y][n.x] = n_cost
                came_from[n.y][n.x] = curr
                priority = n_cost+man_heuristic(n, finish)
                frontier.put([priority, n])

    # проверка: достигли ли конечную вершину
    if came_from[finish.y][finish.x] is None:
        return []

    # составляем путь
    curr = finish
    path = []
    while curr!=start:
        path.append(curr)
        curr = came_from[curr.y][curr.x]
    path.append(curr)

    return path[::-1]