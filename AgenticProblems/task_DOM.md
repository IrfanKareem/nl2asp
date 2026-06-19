# Problem Statement
Write an Answer Set Programming (ASP) program that models the Connected Dominating Set problem by translating the natural-language rules below into ASP rules.
A dominating set is a subset of vertices where every vertex in the graph is either in the set or adjacent to at least one vertex in the set.
In the Connected Dominating Set problem, the vertices in the dominating set must induce a connected subgraph.
Given a graph and an integer bound k, the program determines whether there exists a connected dominating set containing at most k vertices.


## Natural-Language Rules
- Every node can be dom.
- An uedge exists when an edge goes from a smaller vertex to a larger one.
- An uedge is created for every edge where the second vertex is smaller than the first.
- When there is an uedge relation between two vertices and the first one is dom, then we can model the second vertex as considered.
- Model a vertex as considered when there is an uedge relation between it and a second vertex that is also dom.
- The vertices that are dom are also considered.
- A node is designated as hasLower if it is in dom and there exists another smaller node that is also in dom.
- A node is reach whenever it is dom and is not hasLower
- A node that is dom is also reach if there is a uedge from a node that is reach to it.
- A node that is dom is also reach if there is a uedge from it to a node that is reach.
- All dom nodes must be reach nodes.
- All nodes must be designated as considered.
- The number of dom nodes cannot exceeds the given bound.