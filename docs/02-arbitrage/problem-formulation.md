**Problem Statement:**

Given a graph where the vertices are connected by bidirectional edges. The task is to find a walk (of any length) that starts and ends at a specified vertex, such that the **product of the edge weights** along the walk is maximized.

The weights of the edges in opposite directions between any two vertices differ approximately by a factor of _k_ and _1/k_, respectively. Therefore, the problem essentially reduces to finding a cycle where the product of the edge weights is **greater than one**.
