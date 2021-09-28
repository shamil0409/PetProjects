#Author: Nguyen Anh Tu, Dinh-Mao Bui
#Topic: finding a shortest path for a robot vacuum in an 8x8 grid board

def heuristic(pos, goal):
    # Compute the Chebyshev distance from current position to the goal. 
    # Use the Chebyshev distance as a heuristic which allows our robot 
    # to move one square either adjacent or diagonal.
    """
    Args: 
        pos: coordinate of current node
        goal: coordinate of goal node
    Return:
        Chebyshev distance from current position to the goal
    """
    return max(abs(pos[0] - goal[0]),abs(pos[1] - goal[1]))

def get_neighbors(pos):
    # Get the positions of neighbors of current node on the grid board
    """
    Args: 
        pos: coordinate of current node
    Return:
        neighbors: list of coordinates of neighbors
    """
    neighbors = []
    for ix, iy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
        nx = pos[0] + ix
        ny = pos[1] + iy
        if nx < 1 or nx > 8 or ny < 1 or ny > 8:
            continue
        neighbors.append((nx,ny))
    return neighbors

def move_cost(next_node, barrier):
    # Compute the movement cost when moving to next node. 
    # If the next node is the point on the barrier, the cost is extremely high (i.e., 200). 
    # Otherwise, just set to the standard cost = 1
    """
    Args: 
        next_node: coordinate of next node
        barrier: list of coordinates of the points belonging to the barrier
    Return:
        movement cost
    """
    for bar_pos in barrier:
        if next_node in bar_pos:
            return 200
    return 1 



def UCSearch(start, goal, barrier):
    # Implementation of Unoform-Cost Search (2 points)
    """
    Args: 
        start: coordinate of start node
        goal: coordinate of goal node
        barrier: list of coordinates of the points belonging to the barrier
    Return:
        path: list of coordinates of the points belonging to optimal path
        expandedNodes: set of coordinates of expanded nodes
        cost: path cost at the goal state
    """
    ######################################################################################
    
    # Firstly, create a dictonary that stores the path cost so far to reach each node from 
    # the start position. For example, G ={(3, 3): 2} depicts that path cost of (3,3) is 2.
    
    G = {} 
    
    #Initialize value at starting position
    G[start] = 0
    
    # Create two sets. One set (i.e. expandedNodes) is used to store the expanded nodes, 
    # and another set (i.e. fringe) is to store nodes on the fringe. With this data structure,
    # you can use add() (e.g. fringe.add(node)) or remove() (e.g. fringe.remove(node)) functions
    # to update nodes on the given set.
    
    expandedNodes = set() 
    fringe = set([start]) 
    
    # create a dictonary that keeps track of parents of the opened nodes on the path to the goal.
    # For example, parent = {(1, 2): (1, 1)} depicts that (1,1) is a parent of (1,2).
    # This data structure can help to retrace the path when we reach to the goal.
    parent = {} 
    
    while len(fringe) > 0:
        #Pick the node in the fringe with the lowest G score
        lowest = {j : G[j] for j in fringe}
        curNode = list(lowest.keys())[list(lowest.values()).index(min(lowest.values()))]
        curGscore = G[curNode]
        
        for pos in fringe:
            if curNode is None or G[pos] < curGscore:
                curGscore = G[pos]
                curNode = pos
        fringe.remove(curNode)
        
        #Check if our robot has reached the goal
        if curNode == goal:
            #Retrace our path backward
            path = [curNode]
            while curNode in parent:
                curNode = parent[curNode]
                path.append(curNode)
            path.reverse()
            return path, expandedNodes, G[goal]
        else:
            expandedNodes.add(curNode)
            for neighbour in get_neighbors(curNode):
                cost = move_cost(neighbour, barrier)
                if neighbour not in expandedNodes and (neighbour not in fringe or G[neighbour] > G[curNode] + cost):
                    G[neighbour] = G[curNode] + cost
                    parent[neighbour] = curNode
                    if neighbour not in fringe:
                        fringe.add(neighbour)

    raise RuntimeError("UCS failed to find a solution")
    


def aStarSearch(start, goal, barrier):
    # Implementation of A Star Search (3 points)
    """
    Args: 
        start: coordinate of start node
        goal: coordinate of goal node
        barrier: list of coordinates of the points belonging to the barrier
    Return:
        path: list of coordinates of the points belonging to optimal path
        expandedNodes: set of coordinates of expanded nodes
        cost: total estimated path cost at the goal state
    """
    ######################################################################################
    
    # Firstly, create two dictonaries that store the path cost (g) and total estimated cost (f)
    # to reach each node from the start position. 
    # For example, F ={(3, 3): 7} depicts that total cost of (3,3) is 7.
    
    G = {} 
    F = {} 
    
    #Initialize values at starting position
    G[start] = 0
    F[start] = heuristic(start, goal)
    
    # Create two sets. One set (i.e. expandedNodes) is used to store the expanded nodes, 
    # and another set (i.e. fringe) is to store nodes on the fringe. With this data structure,
    # you can use add() (e.g. fringe.add(node)) or remove() (e.g. fringe.remove(node)) functions
    # to update nodes on the given set.
    
    expandedNodes = set() 
    fringe = set([start]) 
    
    # create a dictonary that keeps track of parents of the opened nodes on the path to the goal.
    # For example, parent ={(1, 2): (1, 1)} depicts that (1,1) is a parent of (1,2).
    # This data structure can help to retrace the path when we reach to the goal.
    parent = {} 
    
    while len(fringe) > 0:
        lowest = {j : F[j] for j in fringe}
        curNode = list(lowest.keys())[list(lowest.values()).index(min(lowest.values()))]
        curFscore = F[curNode]
        
        for pos in fringe:
            if curNode is None or F[pos] < curFscore:
                curFscore = F[pos]
                curNode = pos
        fringe.remove(curNode)
        
        #Check if our robot has reached the goal
        if curNode == goal:
            #Retrace our path backward
            path = [curNode]
            while curNode in parent:
                curNode = parent[curNode]
                path.append(curNode)
            path.reverse()
            return path, expandedNodes, F[goal] #Done!
        else:
            expandedNodes.add(curNode)
            for neighbour in get_neighbors(curNode):
                cost = move_cost(neighbour, barrier)
                if neighbour not in expandedNodes and (neighbour not in fringe or G[neighbour] > G[curNode] + cost):
                    G[neighbour] = G[curNode] + cost
                    F[neighbour] = heuristic(neighbour, goal) + G[curNode] + cost
                    parent[neighbour] = curNode
                    if neighbour not in fringe:
                        fringe.add(neighbour)

    raise RuntimeError("A* failed to find a solution")