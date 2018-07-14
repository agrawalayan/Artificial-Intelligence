def backtracing(graph, node_count, depth = 1):
    for key in graph:
        if node_count in graph[key]:
            if (key == 1):
                return depth
            else:
                node_count = int(key)
                depth = depth +1
                return backtracing(graph, node_count,depth)



graph = {1: [2,3,4], 2: [4,5], 3: [8,9], 4:[10,11], 5: [6,7]}
print backtracing(graph, 5)

