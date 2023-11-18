import networkx as nx
import copy

def find_cycles_for(G: nx.Graph, n: int) -> int:
    result = 0
    queue = [set(G[n])]

    while queue:
        current = queue.pop()

        for n1 in current:
            for adj in G[n1]:
                if adj in current:
                    if adj == n:
                        result += 1
                else:
                    new = copy.copy(current)
                    new.add(adj)
                    queue.append(new)
    return result


def num_loops(G: nx.Graph) -> int:
    result = 0
    for n in G:
        result += find_cycles_for(G, n)
    return result
