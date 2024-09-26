# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Kruskal's maze generator.
#
# __author__ = Anh Minh Bui
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze import Maze
from maze.util import Coordinates
import random

class Edge:
    """
    Represents an edge in the graph, consisting of two vertices and a weight.
    """
    def __init__(self):
        self.edges = []
    
    def addEdge(self, u, v, weight):
        """Add an edge between two vertices with a given weight."""
        self.edges.append((u, v, weight))

class DisjointSet:
    """
    Represents the disjoint-set (union-find) data structure.
    """
    def __init__(self, n):
        # Initialize parent and rank arrays
        self.parent = list(range(n))  # Each vertex is initially its own parent
        self.rank = [0] * n  # Rank is used to keep track of the tree depth
    
    def find(self, u):
        """Find the representative of the set containing u (with path compression)."""
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Path compression
        return self.parent[u]
    
    def union(self, u, v):
        """Union by rank, merges the sets containing u and v."""
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

class KruskalMazeGenerator:
    """
    Kruskal's algorithm maze generator with weighted edges.
    """
    
    def generateMaze(self, maze: Maze):
        graph = Edge()  # Graph to store the edges
        cells = maze.getCoords()  # All the cells (vertices) in the maze
        num_cells = len(cells)
        
        # Map cell coordinates to an index for the DisjointSet (since it uses integers)
        cell_index = {cell: idx for idx, cell in enumerate(cells)}
        
        # Add all the walls (edges) between neighboring cells
        for cell in cells:
            neighbors = maze.neighbours(cell)
            for neighbor in neighbors:
                if maze.hasEdge(cell, neighbor):  # Ensure an edge exists
                    weight = maze.edgeWeight(cell, neighbor)  # Get edge weight
                    graph.addEdge(cell, neighbor, weight)

        # Initialize disjoint sets for all cells
        disjoint_set = DisjointSet(num_cells)

        # Sort the edges based on their weights (for the weighted approach)
        graph.edges.sort(key=lambda edge: edge[2])  # Sort by the weight

        # Process each edge in sorted order (Kruskal's algorithm)
        for edge in graph.edges:
            u, v, weight = edge
            u_idx = cell_index[u]
            v_idx = cell_index[v]

            # If u and v are not in the same set, remove the wall between them
            if disjoint_set.find(u_idx) != disjoint_set.find(v_idx):
                maze.removeWall(u, v)  # Remove the wall between u and v
                disjoint_set.union(u_idx, v_idx)  # Merge the sets
                
        # Add outer walls except the entrance and exit
        self.addOuterWalls(maze)

        return maze
    
    def addOuterWalls(self, maze: Maze):
        """Adds outer walls to the maze except for the entrance and exit."""
        width = maze.colNum()
        height = maze.rowNum()

        # Add walls to the top and bottom rows
        for x in range(width):
            top_cell = Coordinates(0, x)
            bottom_cell = Coordinates(height - 1, x)
            top_outer = Coordinates(-1, x)
            bottom_outer = Coordinates(height, x)

            # Add wall between outer top and top row, if not the entrance
            if top_outer not in maze.getEntrances() and top_outer not in maze.getExits():
                maze.addWall(top_outer, top_cell)

            # Add wall between bottom row and outer bottom, if not the exit
            if bottom_outer not in maze.getEntrances() and bottom_outer not in maze.getExits():
                maze.addWall(bottom_cell, bottom_outer)

        # Add walls to the left and right columns
        for y in range(height):
            left_cell = Coordinates(y, 0)
            right_cell = Coordinates(y, width - 1)
            left_outer = Coordinates(y, -1)
            right_outer = Coordinates(y, width)

            # Add wall between outer left and leftmost column, if not the entrance
            if left_outer not in maze.getEntrances() and left_outer not in maze.getExits():
                maze.addWall(left_outer, left_cell)

            # Add wall between rightmost column and outer right, if not the exit
            if right_outer not in maze.getEntrances() and right_outer not in maze.getExits():
                maze.addWall(right_cell, right_outer)