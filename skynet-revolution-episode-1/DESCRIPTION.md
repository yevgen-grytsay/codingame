## Game Input
The program must first read the initialization data from standard input. Then, within an infinite loop, read the data from the standard input related to the current state of the Skynet agent and provide to the standard output the next instruction.

### Initialization input
**Line 1:** 3 integers N L E
- `N`, the total number of nodes in the level, including the gateways.
- `L`, the number of links in the level.
- `E`, the number of exit gateways in the level.

**Next L lines:** 2 integers per line (N1, N2), indicating a link between the nodes indexed N1 and N2 in the network.

**Next E lines:** 1 integer EI representing the index of a gateway node.

### Input for one game turn
Line 1: 1 integer SI, which is the index of the node on which the Skynet agent is positioned this turn.

### Output for one game turn
A single line comprised of two integers C1 and C2 separated by a space. C1 and C2 are the indices of the nodes you wish to sever the link between.

### Constraints
```
2 ≤ N ≤ 500
1 ≤ L ≤ 1000
1 ≤ E ≤ 20
0 ≤ N1, N2 < N
0 ≤ SI < N
0 ≤ C1, C2 < N
Response time per turn ≤ 150ms
```





```
12 23 1
0 2
0 1
0 8
1 2
2 3
3 4
4 5
5 6
6 11
11 10
10 9
9 8
8 1
1 7
2 7
3 7
4 7
5 7
6 7
11 7
10 7
9 7
8 7
7
```