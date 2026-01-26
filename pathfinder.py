from collections import deque

def init_path(maze):
    for row in maze:
        for cell in row:
            cell.BFSvisited = False
            cell.parent = None

def pathfinder(maze, ENTRY, EXIT, WIDTH, HEIGHT):
    init_path(maze)
    q = deque([ENTRY])
    x, y = ENTRY
    maze[y][x].BFSvisited = True
    while q:

        x, y = q.popleft()

        if (x, y) == EXIT:
            break

        directions = [
            (maze[y][x].north, x, y - 1),
            (maze[y][x].east, x + 1, y),
            (maze[y][x].south, x, y + 1),
            (maze[y][x].west, x - 1, y)
        ]

        for d, dx, dy in directions:
            if 0 <= dx < WIDTH and 0 <= dy < HEIGHT and d is False and maze[dy][dx].BFSvisited is False:
                maze[dy][dx].BFSvisited = True
                q.append((dx, dy))
                maze[dy][dx].parent = (x, y)

    path = []
    path.append((x, y))
    while True:
        cx, cy = maze[y][x].parent
        path.append((cx, cy))
        if (cx, cy) == ENTRY:
            break
        x = cx
        y = cy
    path.reverse()
    return path
