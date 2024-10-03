from itertools import permutations
from typing import List, Tuple
from maze.util import Coordinates
from maze.maze import Maze
from .dijkstraSolver import DijkstraSolver

class bruteForceSolver:

    def __init__(self):
        self.entrance_exit_paths = {}
        self.cellsExplored = 0
        self.all_solved = False
        self.shortest_total_distance = float('inf')  # Track the minimum total distance

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]):
        all_paths = []
        
        # Generate paths for each entrance-exit pair using Dijkstra's algorithm
        for entrance, exit in zip(entrances, exits):
            solver = DijkstraSolver()
            solver.solveMaze(maze, entrance)
            all_paths.append((solver.m_solverPath, solver.m_cellsExplored, solver))  # Store solver for distance calculation
        
        # Try all permutations to find non-overlapping paths
        for perm in permutations(all_paths):
            if self.checkNonOverlapping(perm):
                total_distance = self.calculateTotalDistance(perm)
                
                # Update if this is the shortest distance so far
                if total_distance < self.shortest_total_distance:
                    self.shortest_total_distance = total_distance
                    self.entrance_exit_paths = {entrances[i]: perm[i][0] for i in range(len(entrances))}
                    self.cellsExplored = sum(p[1] for p in perm)
                    self.all_solved = True
        
        # If no valid non-overlapping paths are found, set all_solved to False
        if not self.all_solved:
            self.entrance_exit_paths = {}
            self.shortest_total_distance = float('inf')
            self.cellsExplored = 0

    def checkNonOverlapping(self, paths: List[Tuple[List[Coordinates], int, DijkstraSolver]]) -> bool:
        visited = set()
        for path, _, _ in paths:
            for cell in path:
                if cell in visited:
                    return False
                visited.add(cell)
        return True

    def calculateTotalDistance(self, paths: List[Tuple[List[Coordinates], int, DijkstraSolver]]) -> int:
        # The total distance is the sum of the distances calculated by each DijkstraSolver
        return sum(solver.m_cellsExplored for _, _, solver in paths)
