from mlx import Mlx

WIDTH = 400
HEIGHT = 300

mlx = Mlx()
ctx = mlx.mlx_init()
win = mlx.mlx_new_window(ctx, WIDTH, HEIGHT, "Pixel Test")

# Create image
img = mlx.mlx_new_image(ctx, WIDTH, HEIGHT)
data, bpp, size_line, endian = mlx.mlx_get_data_addr(img)

# 🔧 FIX 1: make data writable
data = bytearray(data)

print(f"bpp={bpp}, size_line={size_line}, endian={endian}")

BYTES_PER_PIXEL = bpp // 8

def put_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        pos = y * size_line + x * BYTES_PER_PIXEL

        # MLX uses BGR
        data[pos + 0] = color & 0xFF          # Blue
        data[pos + 1] = (color >> 8) & 0xFF   # Green
        data[pos + 2] = (color >> 16) & 0xFF  # Red

        if BYTES_PER_PIXEL == 4:
            data[pos + 3] = 0xFF              # Alpha

# ---- DRAWING ----

# Background
for y in range(HEIGHT):
    for x in range(WIDTH):
        put_pixel(x, y, 0x000044)

# Red rectangle
for y in range(50, 150):
    for x in range(50, 200):
        put_pixel(x, y, 0xFF0000)

# Green circle
cx, cy, r = 300, 150, 50
for y in range(cy - r, cy + r):
    for x in range(cx - r, cx + r):
        if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
            put_pixel(x, y, 0x00FF00)

# White border
for x in range(WIDTH):
    put_pixel(x, 0, 0xFFFFFF)
    put_pixel(x, HEIGHT - 1, 0xFFFFFF)

for y in range(HEIGHT):
    put_pixel(0, y, 0xFFFFFF)
    put_pixel(WIDTH - 1, y, 0xFFFFFF)

# ---- DISPLAY ----

mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)

# 🔧 FIX 3: correct expose hook
def on_expose():
    mlx.mlx_put_image_to_window(ctx, win, img, 0, 0)

# mlx.mlx_expose_hook(win, on_expose)

# Exit on ESC
def on_key(keycode):
    if keycode == 65307:
        mlx.mlx_loop_exit(ctx)

mlx.mlx_key_hook(win, on_key)

print("Running... Press ESC to exit")
mlx.mlx_loop(ctx)
