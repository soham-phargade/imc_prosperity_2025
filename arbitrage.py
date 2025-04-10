import math

table = [[1,1.45,0.52,0.72],[0.7,1,0.31,0.48],[1.96,3.1,1,1.49],[1.34,1.98,0.64,1]]
names = {0: "Snowball", 1:"Pizza", 2:"Silicon", 3:"SeaShells"}

ln_table = [[None for _ in range(4)] for _ in range(4)]
for i in range(4):
    for j in range(4):
        ln_table[i][j] = -math.log(table[i][j])

def print_grid(grid):
    for row in grid:
        print(' '.join(map(str, row)))


# Use an algorithm to find the cycle with the shortest length from 3 to 3. 
# I will use brute force because n = 4

def find_most_negative_cycle(ln_table):
    n = 4
    best_cycle = []
    best_weight = math.inf

    def dfs(current, start, visited, path, total_weight):
        nonlocal best_weight, best_cycle
        if current == start and len(path) > 1:
            if total_weight < best_weight:
                best_weight = total_weight
                best_cycle = path.copy()
            return
        
        for neighbor in range(4):
            if neighbor == current:
                continue
            if neighbor == start or (neighbor not in visited and neighbor != path[0]):
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, start, visited, path, total_weight + ln_table[current][neighbor])
                path.pop()
                visited.remove(neighbor)
    
    visited = set([0])
    dfs(3, 3, visited, [0], 0)

    return best_cycle

def main():
    arr = find_most_negative_cycle(ln_table)
    for i in range(len(arr)):
        arr[i] = names[arr[i]]
    print(arr)

if __name__ == "__main__":
    main()

