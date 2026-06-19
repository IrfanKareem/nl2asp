# Problem Statement
Write an Answer Set Programming (ASP) program that models the Traveling Salesperson Problem (TSP) by translating the natural-language rules below into ASP rules.
The problem is about finding a Hamiltonian cycle (a cycle that visits each vertex exactly once) in an undirected graph. Every edge in the graph is associated with a positive weight.
The goal is to find a Hamiltonian cycle in a graph such that the sum of the edges weights is at most a given maximum weight w.


## Natural-Language Rules
- For any weighted edge connecting two nodes, it is either in the path or out of the path.
- A node must have only one outgoing edge in the path.
- It is required that a node has just one incoming edge in the path.
- The node designated as the start is reached.
- A node that has an edge in the path from a reached node is also considered reached.
- All nodes have to be reached.
- The sum of the weights of all edges that are in the path must not exceed the maximum weight defined by the maxweight predicate.
