def backtracing(graph,level_one_length =2, successors_count =12):
    for key in graph:
        if successors_count in graph[key]:
            if (2 <= key < 2+ level_one_length):
                return int(key)
            else:
                successors_count = int(key)
                return backtracing(graph,3,successors_count)
graph = {1: [2, 3, 4], 2: [5, 6], 3: [7, 8], 4: [9, 10], 5: [11, 12, 13]}
print backtracing(graph, 3, 12)
#print parent_key
