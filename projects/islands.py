# count islands in a binary graph

def island_counter(matrix):
    island_count=0
    visited=[]
    for i in range(len(matrix)):
        visited.append([False]*len(matrix[0]))
    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            if not visited[y][x]:
                if matrix[y][x]==1:
                    visited=dft(x,y,matrix,visited)
                    island_count+=1
                else:
                    visited[y][x]=True

def dft(x,y,matrix,visited):
    s=Stack()
    s.push((x,y))
    while s.size()>0:
        v=s.pop()
        x=v[0]
        y=v[1]
        if not visited[y][x]:
            visited[y][x]=True
            for neighbor in get_neighbors((x,y),matrix):
                s.push(neighbor)
    return visited

islands = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]

