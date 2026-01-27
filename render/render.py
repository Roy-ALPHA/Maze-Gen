import time
import random
from maze.mazegen import MazeGenerator, InvalidDistinationFor42Path
from maze.pathfinder import pathfinder
from utils.errors import InvalidCoordinates

try:
    from mlx import Mlx
except ModuleNotFoundError:
    ModuleNotFoundError(
        "❌ Error: MiniLibX (mlx) module not found.\n"
        "👉 Make sure you:\n"
        "   - Built MiniLibX with `make`\n"
        "   - Installed the Python wheel (.whl)\n"
    )


def mlx_render(width, length, ENTRY, EXIT):
    width_pixel = width * 40
    length_pixel = length * 40
    if width_pixel > 1920 or length_pixel > 1000:
        raise InvalidCoordinates(
                "❌ Error: Window size exceeds screen resolution.\n"
                f"Requested: {width}x{length}\n"
                "Maximum allowed: 48x25\n"
                "👉 Please reduce WIDTH or HEIGHT to fit your screen."
        )
    mlx1 = Mlx()
    k = mlx1.mlx_init()

    win = mlx1.mlx_new_window(k, width_pixel, length_pixel, "YEB&YEN Maze_gen")
    maze = MazeGenerator(width, length)
    try:
        maze.creat_maze_bakctracker_algo()
    except InvalidDistinationFor42Path as e:
        print(e)
        maze.remove_walls()

    mz = maze.maze
    img = mlx1.mlx_new_image(k, width_pixel, length_pixel)
    result = mlx1.mlx_get_data_addr(img)
    data = result[0]
    size_line = result[2]

    def put_pixel(x, y, color):
        """Put a pixel at (x, y) with the given color in the image data"""
        if 0 <= x < width_pixel and 0 <= y < length_pixel:
            offset = y * size_line + x * 4
            if offset + 4 <= len(data):
                data[offset] = color & 0xFF
                data[offset + 1] = (color >> 8) & 0xFF
                data[offset + 2] = (color >> 16) & 0xFF
                data[offset + 3] = 0xFF

    bg_img, bg_width, bg_lenght = mlx1.mlx_xpm_file_to_image(k, "assets/maze_bg_40.xpm")
    pl_img, pl_width, pl_lenght = mlx1.mlx_xpm_file_to_image(k, "assets/player_idle1.xpm")

    def back_img():
        for y in range(0, length_pixel, bg_lenght):
            for x in range(0, width_pixel, bg_width):
                mlx1.mlx_put_image_to_window(k, win, bg_img, x, y)

    back_img()
    back_img()

    def player(x, y):
        mlx1.mlx_put_image_to_window(k, win, pl_img, x, y)

    colors = [
        0xFFFFFF,  # white
        0xFF0000,  # red
        0x00FF00,  # green
        0x0000FF,  # blue
        0xFFFF00,  # yellow
        0x00FFFF,  # cyan
        0xFF00FF,  # magenta
    ]
    wall_color = random.choice(colors)

    path_end_img, path_end_width, path_end_length = mlx1.mlx_xpm_file_to_image(k, "assets/path_end.xpm")
    path_start_img, path_start_width, path_start_length = mlx1.mlx_xpm_file_to_image(k, "assets/path_start.xpm")
    down_img, tmp1, tmp2 = mlx1.mlx_xpm_file_to_image(k, "assets/arrow_down.xpm")
    up_img, tmp1, tmp2 = mlx1.mlx_xpm_file_to_image(k, "assets/arrow_up.xpm")
    right_img, tmp1, tmp2 = mlx1.mlx_xpm_file_to_image(k, "assets/arrow_right.xpm")
    left_img, tmp1, tmp2 = mlx1.mlx_xpm_file_to_image(k, "assets/arrow_left.xpm")

    directions = [down_img, up_img, right_img, left_img]

    mlx1.mlx_put_image_to_window(k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
    mlx1.mlx_put_image_to_window(k, win, path_end_img, EXIT[0] * 40 + 10, EXIT[1] * 40 + 10)

    pl_x = ENTRY[0] * 40 + 10
    pl_y = ENTRY[1] * 40 + 10

    def draw_path():
        nonlocal pl_x, pl_y
        path = pathfinder(mz, (pl_x // 40, pl_y // 40), EXIT, width, length)
        direction_i = None
        CELL = 40
        i = 1
        for x, y in path:
            for nx, ny in path[i:]:
                if ny > y and nx == x:
                    direction_i = 0
                elif ny < y and nx == x:
                    direction_i = 1
                elif nx > x and ny == y:
                    direction_i = 2
                elif nx < x and ny == y:
                    direction_i = 3
                px = x * CELL + 10
                py = y * CELL + 10
                if (x, y) != ENTRY and (x, y) != EXIT and (x, y) != (pl_x // 40, pl_y // 40):
                    time.sleep(0.0001)
                    mlx1.mlx_put_image_to_window(k, win, directions[direction_i], px, py)
                i += 1
                break

    def draw_maze(maze, color, sleep):
        CELL = 40
        y_offset = 0
        for row in maze:
            x_offset = 0
            for cell in row:
                if cell.north:
                    for x in range(x_offset, x_offset + CELL):
                        put_pixel(x, y_offset, color)

                if cell.south:
                    for x in range(x_offset, x_offset + CELL):
                        put_pixel(x, y_offset + CELL - 1, color)
                if sleep is True:
                    time.sleep(0.0001)
                    mlx1.mlx_put_image_to_window(k, win, img, 0, 0)

                if cell.west:
                    for y in range(y_offset, y_offset + CELL):
                        put_pixel(x_offset, y, color)

                if cell.east:
                    for y in range(y_offset, y_offset + CELL):
                        put_pixel(x_offset + CELL - 1, y, color)
                x_offset += CELL
            y_offset += CELL

    draw_maze(mz, wall_color, True)

    def render():
        draw_maze(mz, wall_color, False)
        mlx1.mlx_put_image_to_window(k, win, img, 0, 0)
        player(pl_x, pl_y)

    render()

    prev_x = 0
    prev_y = 0

    def regenerate_maze():
        nonlocal mz
        maze = MazeGenerator(width, length)
        try:
            maze.creat_maze_bakctracker_algo()
        except InvalidDistinationFor42Path as e:
            print(e)
            maze.remove_walls()

        new_maze = maze.maze
        back_img()
        back_img()
        draw_maze(mz, 0x000000, True)
        draw_maze(new_maze, wall_color, True)
        mlx1.mlx_put_image_to_window(k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
        mlx1.mlx_put_image_to_window(k, win, path_end_img, EXIT[0] * 40 + 10, EXIT[1] * 40 + 10)
        mz = new_maze

    def on_key(keycode, param):
        nonlocal pl_x, pl_y, wall_color, prev_x, prev_y
        prev_x = pl_x
        prev_y = pl_y
        is_moved = False
        if keycode == 65307:
            mlx1.mlx_loop_exit(k)
        if keycode == 99:
            wall_color = random.choice(colors)
            draw_maze(mz, wall_color, True)
        if keycode == 65364 and mz[pl_y // 40][pl_x // 40].south is False:
            is_moved = True
            pl_y += 40
        elif keycode == 65362 and mz[pl_y // 40][pl_x // 40].north is False:
            is_moved = True
            pl_y -= 40
        elif keycode == 65363 and mz[pl_y // 40][pl_x // 40].east is False:
            is_moved = True
            pl_x += 40
        elif keycode == 65361 and mz[pl_y // 40][pl_x // 40].west is False:
            is_moved = True
            pl_x -= 40
        if is_moved is True:
            if (pl_x, pl_y) == (EXIT[0] * 40 + 10, EXIT[1] * 40 + 10):
                mlx1.mlx_loop_exit(k)
            mlx1.mlx_put_image_to_window(k, win, bg_img, prev_x - 10, prev_y - 10)
            mlx1.mlx_put_image_to_window(k, win, bg_img, pl_x - 10, pl_y - 10)
            mlx1.mlx_put_image_to_window(k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
        if keycode == 112:
            draw_path()
        if keycode == 103:
            regenerate_maze()
        render()

    mlx1.mlx_key_hook(win, on_key, None)
    mlx1.mlx_loop(k)
