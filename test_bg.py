from mlx import Mlx
import time

mlx = Mlx()
mlx_ptr = mlx.mlx_init()

WIDTH = 400
HEIGHT = 300

win = mlx.mlx_new_window(mlx_ptr, WIDTH, HEIGHT, "Simple Animation")

# Create image buffer
img = mlx.mlx_new_image(mlx_ptr, WIDTH, HEIGHT)
data, bpp, size_line, fmt = mlx.mlx_get_data_addr(img)

# --------- STATE ----------
x = 0
y = 140
speed = 2
last_time = time.time()

# --------- DRAW PIXEL ----------
def put_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        offset = y * size_line + x * 4
        data[offset]     = color & 0xFF
        data[offset + 1] = (color >> 8) & 0xFF
        data[offset + 2] = (color >> 16) & 0xFF
        data[offset + 3] = 0xFF

# --------- CLEAR IMAGE ----------
def clear():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            put_pixel(x, y, 0x000000)

# --------- DRAW SQUARE ----------
def draw_square(px, py):
    for y in range(py, py + 20):
        for x in range(px, px + 20):
            put_pixel(x, y, 0xFF0000)

# --------- LOOP HOOK ----------
def loop(param):
    global x, last_time

    now = time.time()
    if now - last_time < 1 / 60:  # 60 FPS
        return
    last_time = now

    # clear()
    draw_square(x, y)
    mlx.mlx_put_image_to_window(mlx_ptr, win, img, 0, 0)

    x += speed
    if x > WIDTH:
        x = -20

# --------- EXIT ----------
def on_key(key, param):
    if key == 65307:  # ESC
        mlx.mlx_loop_exit(mlx_ptr)

mlx.mlx_key_hook(win, on_key, None)
mlx.mlx_loop_hook(mlx_ptr, loop, None)
mlx.mlx_loop(mlx_ptr)
