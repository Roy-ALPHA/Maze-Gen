import time
import random
import sys
from maze.mazegen import (MazeGenerator, InvalidDistinationFor42Path,
                          InvalidEntryExitPoint)
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


def mlx_render(width, length, ENTRY, EXIT, out_file: str, is_perfect: bool,
               seed: bool):
    """
    Main rendering and maze generation function.

    - Generates a maze (perfect or imperfect)
    - Computes the solution path from ENTRY to EXIT
    - Converts the maze/path representation into a hexadecimal format
    - Writes the hexadecimal encoding to `out_file`
    - Initializes MiniLibX (MLX) for graphical rendering
    - Handles rendering, input events, and maze regeneration

    Args:
        width (int): Maze width in cells
        length (int): Maze height in cells
        ENTRY (tuple): Entry cell (x, y)
        EXIT (tuple): Exit cell (x, y)
        out_file (str): Output file path where the maze/path is
                        encoded and saved in hexadecimal format
        is_perfect (bool): Whether to generate a perfect maze
        seed (bool): Whether to use a fixed random seed
    """
    width_pixel = width * 40
    length_pixel = length * 40
    if width_pixel > 1920 or length_pixel > 1000:
        raise InvalidCoordinates(
                "❌ Error: Window size exceeds screen resolution.\n"
                f"Requested: {width}x{length}\n"
                "Maximum allowed: 48x25\n"
                "👉 Please reduce WIDTH or HEIGHT to fit your screen."
        )
    if width < 6 or length < 6:
        raise InvalidCoordinates(
            "❌ Error: Invalid coordinates.\n"
            "Minimum allowed: 6x6"
        )

    output_file = out_file
    maze = MazeGenerator(width, length, ENTRY, EXIT, out_file)
    try:
        if seed:
            random.seed(1)
        if not is_perfect:
            maze.creat_maze_prims_algo()
        else:
            maze.creat_maze_bakctracker_algo()
        maze.creat_output_file(pathfinder(maze.maze, ENTRY, EXIT, width,
                                          length))
    except InvalidEntryExitPoint as e:
        print(f"Error: {e}")
        sys.exit()

    except InvalidDistinationFor42Path as e:
        print(e)
        if not is_perfect:
            maze.remove_walls_prims_algo()
        else:
            maze.remove_walls_backtracker_algo()
        maze.creat_output_file(pathfinder(maze.maze, ENTRY, EXIT, width,
                                          length))

    mlx1 = Mlx()
    k = mlx1.mlx_init()
    win = mlx1.mlx_new_window(k, width_pixel, length_pixel, "YEB&YEN Maze_gen")
    mz = maze.maze
    img = mlx1.mlx_new_image(k, width_pixel, length_pixel)
    result = mlx1.mlx_get_data_addr(img)
    data = result[0]
    size_line = result[2]

    def put_pixel(x, y, color):
        """
        Draws a single pixel into the MLX image buffer.

        This function writes directly into the raw image memory (CPU RAM).
        The pixel format is assumed to be BGRA (4 bytes per pixel).

        Args:
            x (int): X coordinate in pixels
            y (int): Y coordinate in pixels
            color (int): Color in 0xRRGGBB format
        """
        if 0 <= x < width_pixel and 0 <= y < length_pixel:
            offset = y * size_line + x * 4
            if offset + 4 <= len(data):
                byte = color.to_bytes(3, 'little')
                data[offset] = byte[0]
                data[offset + 1] = byte[1]
                data[offset + 2] = byte[2]
                data[offset + 3] = 255

    bg_img, bg_width, bg_lenght = mlx1.mlx_xpm_file_to_image(
                                        k,
                                        "assets/maze_bg_40.xpm")
    pl_img, pl_width, pl_lenght = mlx1.mlx_xpm_file_to_image(
                                        k,
                                        "assets/player_idle1.xpm")

    def back_img():
        """
        Fills the entire window with the background image.

        The background image is tiled repeatedly to cover the whole window.
        """
        for y in range(0, length_pixel, bg_lenght):
            for x in range(0, width_pixel, bg_width):
                mlx1.mlx_put_image_to_window(k, win, bg_img, x, y)

    back_img()
    back_img()

    def player(x, y):
        """
        Draws the player sprite at the given pixel position.

        Args:
            x (int): X position in pixels
            y (int): Y position in pixels
        """
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

    path_end_img, path_end_width, path_end_length = mlx1.mlx_xpm_file_to_image(
        k, "assets/path_end.xpm")
    path_start_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/path_start.xpm")
    down_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/arrow_down.xpm")
    up_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/arrow_up.xpm")
    right_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/arrow_right.xpm")
    left_img, _, _ = mlx1.mlx_xpm_file_to_image(
        k, "assets/arrow_left.xpm")
    image_42, _, _, = mlx1.mlx_xpm_file_to_image(
        k, "assets/wall_1337_neon.xpm")

    def draw_42(mz):
        y_offset = 0
        for row in mz:
            x_offset = 0
            for cell in row:
                if cell.self._42_path is True:
                    mlx1.mlx_put_image_to_window(k, win, image_42, x_offset, y_offset)
                    x_offset += 40
            y_offset += 40

    directions = [down_img, up_img, right_img, left_img]

    mlx1.mlx_put_image_to_window(k,
                                 win,
                                 path_start_img,
                                 ENTRY[0] * 40 + 10,
                                 ENTRY[1] * 40 + 10)

    mlx1.mlx_put_image_to_window(k,
                                 win,
                                 path_end_img,
                                 EXIT[0] * 40 + 10,
                                 EXIT[1] * 40 + 10)

    pl_x = ENTRY[0] * 40 + 10
    pl_y = ENTRY[1] * 40 + 10

    def draw_path():
        """
        Computes and displays the solution path from the player's position
        to the exit.

        Uses arrow images to visually represent movement directions.
        """
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
                    mlx1.mlx_put_image_to_window(k,
                                                 win,
                                                 directions[direction_i],
                                                 px,
                                                 py)
                i += 1
                break

    def draw_maze(maze, color, sleep):
        """
        Draws the maze walls into the image buffer.

        Each cell wall (north, south, east, west) is drawn pixel-by-pixel.
        Optionally animates drawing by sleeping briefly between updates.

        Args:
            maze (list): 2D list of maze cells
            color (int): Wall color (0xRRGGBB)
            sleep (bool): Whether to animate drawing
        """
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
        """
        Renders the full frame:

        - Draws maze walls
        - Pushes the image buffer to the window
        - Draws the player sprite
        """
        draw_42(mz)
        draw_maze(mz, wall_color, False)
        mlx1.mlx_put_image_to_window(k, win, img, 0, 0)
        player(pl_x, pl_y)

    render()

    prev_x = 0
    prev_y = 0

    def regenerate_maze():
        """
        Regenerates the maze with the same parameters.

        - Resets player position
        - Recreates the maze structure
        - Redraws background, maze, entry, and exit
        """
        nonlocal pl_x, pl_y
        pl_x = ENTRY[0] * 40 + 10
        pl_y = ENTRY[1] * 40 + 10
        nonlocal mz
        maze = MazeGenerator(width, length, ENTRY, EXIT, output_file)
        if seed:
            random.seed(1)
        try:
            if not is_perfect:
                maze.creat_maze_prims_algo()
            else:
                maze.creat_maze_bakctracker_algo()
            maze.creat_output_file(pathfinder(maze.maze, ENTRY, EXIT, width,
                                              length))
        except InvalidDistinationFor42Path as e:
            print(e)
            if not is_perfect:
                maze.remove_walls_prims_algo()
            else:
                maze.remove_walls_backtracker_algo()
            maze.creat_output_file(pathfinder(maze.maze, ENTRY, EXIT, width,
                                              length))
        except InvalidEntryExitPoint as e:
            print(f"Error: {e}")
            sys.exit()

        new_maze = maze.maze
        back_img()
        back_img()
        draw_maze(mz, 0x000000, True)
        draw_maze(new_maze, wall_color, True)
        mlx1.mlx_put_image_to_window(
            k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
        mlx1.mlx_put_image_to_window(
            k, win, path_end_img, EXIT[0] * 40 + 10, EXIT[1] * 40 + 10)
        mz = new_maze

    def on_key(keycode, param):
        """
        Keyboard event handler.

        Handles:
        - Player movement
        - Color changes
        - Path visualization
        - Maze regeneration
        - Window exit

        Args:
            keycode (int): X11 keycode
            param: Unused parameter (required by MLX)
        """
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
            mlx1.mlx_put_image_to_window(
                k, win, bg_img, prev_x - 10, prev_y - 10)
            mlx1.mlx_put_image_to_window(k, win, bg_img, pl_x - 10, pl_y - 10)
            mlx1.mlx_put_image_to_window(
                k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)

        if keycode == 112:
            back_img()
            back_img()
            mlx1.mlx_put_image_to_window(
                k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
            mlx1.mlx_put_image_to_window(
                k, win, path_end_img, EXIT[0] * 40 + 10, EXIT[1] * 40 + 10)
            player(pl_x, pl_y)
            draw_path()

        if keycode == 103:
            regenerate_maze()

        if keycode == 104:
            back_img()
            back_img()
            mlx1.mlx_put_image_to_window(
                k, win, path_start_img, ENTRY[0] * 40 + 10, ENTRY[1] * 40 + 10)
            mlx1.mlx_put_image_to_window(
                k, win, path_end_img, EXIT[0] * 40 + 10, EXIT[1] * 40 + 10)
            player(pl_x, pl_y)

        render()

    mlx1.mlx_key_hook(win, on_key, None)
    mlx1.mlx_loop(k)