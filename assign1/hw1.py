############# Write Your Library Here ###########
from collections import deque, defaultdict
import heapq


################################################


def search(maze, func):
    return {
        "bfs": bfs,
        "dfs":dfs,
        "astar": astar,
        "astar_four_circles": astar_four_circles,
        "astar_many_circles": astar_many_circles
    }.get(func)(maze)


def bfs(maze):
    """
    [Problem 01] 제시된 stage1 맵 세 가지를 BFS Algorithm을 통해 최단 경로를 return하시오.
    """
    start_point=maze.startPoint()
    path=[]
    ####################### Write Your Code Here ###############################
    end_point = maze.circlePoints()[0]
    
    queue = deque()
    queue.append(start_point)

    visited = []
    parent = {}

    while queue:
        y, x = queue.popleft()

        if (y, x) == end_point:
            break

        for next_y, next_x in maze.neighborPoints(y, x):
            if (next_y, next_x) not in visited:
                visited.append((next_y,next_x))
                queue.append((next_y,next_x))
                parent[(next_y, next_x)] = (y,x)

    path = [(y,x)]
    while path[-1] != start_point:
        path.append(parent[path[-1]])
    path.reverse()
    
    result = maze.isValidPath(path)
    if result != 'Valid':
        print(result)

    return path

            
    ############################################################################


def dfs(maze):
    """
    [Problem 02] 제시된 stage1 맵 세 가지를 DFS Algorithm을 통해 최단 경로를 return하시오.
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################

    end_point = maze.circlePoints()[0]

    stack = deque()
    stack.append(start_point + (-1,-1))

    visited = []
    parent = {}

    while stack:
        y, x, prev_y, prev_x = stack.pop()
        
        if (y, x) == end_point:
            parent[(y,x)] = (prev_y, prev_x)
            break

        if (y, x) not in visited:
            visited.append((y, x))
            parent[(y, x)] = (prev_y, prev_x)
            for next_y, next_x in maze.neighborPoints(y, x):
                stack.append((next_y,next_x, y, x))

    path = [(y,x)]
    while path[-1] != start_point:
        path.append(parent[path[-1]])
    path.reverse()

    result = maze.isValidPath(path)
    if result != 'Valid':
        print(result)

    return path


    ############################################################################

class Node(object):
    def __init__(self, parent, item, gscore = 0, heuri = 0):
        self.parent = parent
        self.item = item
        self.fscore = 0
        self.gscore = gscore
        self.heuri = heuri

    def __eq__(self, other):
        return self.item == other.item

    def __le__(self, other):
        return self.gscore + self.heuri <= other.gscore + other.heuri

    def __lt__(self, other):
        return self.gscore + self.heuri < other.gscore + other.heuri

    def __ge__(self, other):
        return self.gscore + self.heuri >= other.gscore + other.heuri

    def __gt__(self, other):
        return self.gscore + self.heuri > other.gscore + other.heuri

    


def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def astar(maze):
    """
    [Problem 03] 제시된 stage1 맵 세가지를 A* Algorithm을 통해 최단경로를 return하시오.
    (Heuristic Function은 위에서 정의한 manhattan_dist function을 사용할 것.)
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################

    end_point = maze.circlePoints()[0]

    start_node = Node(None, start_point,0, 0)
    end_node = Node(None, end_point,0, 0)

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while open_list:
        cur_node = open_list[0]
        cur_idx = 0

        for idx, item in enumerate(open_list):
            if item.fscore < cur_node.fscore:
                cur_node = item
                cur_idx = idx

        open_list.pop(cur_idx)
        closed_list.append(cur_node)

        if cur_node == end_node:
            temp = cur_node
            while temp:
                path.append(temp.item)
                temp = temp.parent
            path.reverse()
            break

        for next_y,next_x in maze.neighborPoints(cur_node.item[0], cur_node.item[1]):
            new_node = Node(cur_node, (next_y,next_x), 0, 0)
            if new_node in closed_list:
                continue
            
            new_node.gscore = cur_node.gscore + 1
            new_node.heuri = manhattan_dist(new_node.item, end_node.item)
            new_node.fscore = new_node.gscore + new_node.heuri
            
            flag = 0
            for open_node in open_list:
                if open_node == new_node:
                    if new_node > open_node:
                        flag = 1
                        break
            if(flag != 1):
                open_list.append(new_node)

    result = maze.isValidPath(path)
    if(result != 'Valid'):
        print(result)

    return path

    ############################################################################



def stage2_heuristic(cur_point, end_nodes, visited):

    min_dist = float("inf")
    for i in range(4):
        if not visited[i]:
            min_dist = min(min_dist, manhattan_dist(cur_point, end_nodes[i].item))

    return min_dist



def astar_four_circles(maze):
    """
    [Problem 04] 제시된 stage2 맵 세 가지를 A* Algorithm을 통해 최단경로를 return하시오.
    (Heuristic Function은 직접 정의할것 )
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################
    
    end_points = maze.circlePoints()

    start_node = Node(None, start_point, 0, 0)
    end_nodes = [Node(None, end_point, 0, 0) for end_point in end_points]
    
    visited = [False, False, False, False]
    

    for i in range(4):
        open_list = []
        closed_list = []
        
        if not path:
            open_list.append(start_node)
        else:
            open_list.append(Node(None,path[-1],0,0))
        
        while open_list:
            cur_node = open_list[0]
            cur_idx = 0

            for idx, item in enumerate(open_list):
                if item.fscore < cur_node.fscore:
                    cur_node =  item
                    cur_idx = idx

            open_list.pop(cur_idx)
            closed_list.append(cur_node)

            if cur_node in end_nodes and not visited[end_nodes.index(cur_node)]:
                visited[end_nodes.index(cur_node)] = True
                temp = cur_node
                path_temp = []
                while temp:
                    path_temp.append(temp.item)
                    temp = temp.parent
                
                path = path[0:len(path)-1] + path_temp[::-1]
                break

            for next_y, next_x in maze.neighborPoints(cur_node.item[0], cur_node.item[1]):
                new_node = Node(cur_node, (next_y, next_x), 0, 0)
                if new_node in closed_list:
                    continue

                new_node.gscore = cur_node.gscore + 1
                new_node.heuri = stage2_heuristic(new_node.item, end_nodes, visited)
                new_node.fscore = new_node.gscore + new_node.heuri

                flag = 0
                for open_node in open_list:
                    if new_node == open_node:
                        if new_node > open_node:
                            flag = 1
                            break
                if flag != 1:
                    open_list.append(new_node)


    result = maze.isValidPath(path)
    if result != 'Valid':
        print(result)

    return path

    ############################################################################


def mst(start_point, remain_points):
    total_weight = 0
    
    graph = defaultdict(list)
    
    for y, x in remain_points:
        graph[start_point].append(((manhattan_dist(start_point,(y,x))), (y,x)))
        graph[(y,x)].append(((manhattan_dist(start_point,(y,x))), start_point))

    for y1, x1 in remain_points:
        for y2, x2 in remain_points:
            if y1 != y2 and x1 != x2:
                graph[(y1,x1)].append(((manhattan_dist((y1,x1),(y2,x2))), (y2,x2)))
                graph[(y2,x2)].append(((manhattan_dist((y1,x1),(y2,x2))), (y1,x1)))

    visited = set([start_point])
    candidate = graph[start_point]
    heapq.heapify(candidate)

    while(candidate):
        weight, u = heapq.heappop(candidate)

        if u in visited:
            continue
        visited.add(u)
        total_weight += weight

        for edge in graph[u]:
            if edge[1] not in visited:
                heapq.heappush(candidate, edge)

    return total_weight

def stage3_heuristic(cur_point, end_nodes, visited):
    remain_end_points = []

    for i in range(len(visited)):
        if not visited[i]:
            remain_end_points.append(end_nodes[i].item)

    return mst(cur_point, remain_end_points)


def astar_many_circles(maze):
    """
    [Problem 04] 제시된 stage3 맵 다섯 가지를 A* Algorithm을 통해 최단 경로를 return하시오.
    (Heuristic Function은 직접 정의 하고, minimum spanning tree를 활용하도록 한다.)
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################
    
    end_points = maze.circlePoints()

    start_node = Node(None, start_point, 0, 0)
    end_nodes = [Node(None, end_point) for end_point in end_points]
    
    visited = [False for i in range(len(end_points))]

    for i in range(len(end_points)):
        open_list = []
        closed_list = []

        if not path:
            open_list.append(start_node)
        else:
            open_list.append(Node(None,path[-1],0,0))
        
        while open_list:
            cur_node = open_list[0]
            cur_idx = 0

            for idx, item in enumerate(open_list):
                if item.fscore < cur_node.fscore:
                    cur_node = item
                    cur_idx = idx

            open_list.pop(cur_idx)
            closed_list.append(cur_node)
            
            if cur_node in end_nodes and not visited[end_nodes.index(cur_node)]:
                visited[end_nodes.index(cur_node)] = True
                
                temp = cur_node
                path_temp = []
                while temp:
                    path_temp.append(temp.item)
                    temp = temp.parent

                path = path[0:len(path)-1] + path_temp[::-1]
                break

            for next_y, next_x in maze.neighborPoints(cur_node.item[0], cur_node.item[1]):
                new_node = Node(cur_node, (next_y,next_x), 0, 0)
                if new_node in closed_list:
                    continue

                new_node.gscore = cur_node.gscore + 1
                new_node.heuri = stage3_heuristic(new_node.item, end_nodes, visited)
                new_node.fscore = new_node.gscore + new_node.heuri

                flag = 0
                for open_node in open_list:
                    if open_node == new_node:
                        if open_node < new_node:
                            flag = 1
                            break
                if flag != 1:
                    open_list.append(new_node)

    result = maze.isValidPath(path)
    if(result != 'Valid'):
        print(result)


    return path

    ############################################################################
