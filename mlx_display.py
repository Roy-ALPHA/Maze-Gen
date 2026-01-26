from mlx import Mlx

# init mlx
mlx1 = Mlx()
k = mlx1.mlx_init()
# create window
width = 400
length = 400
win = mlx1.mlx_new_window(k, width, length, "Pixel Test")
# Example maze (3x3)
maze = [
    [{'north':True, 'south':False, 'east':False, 'west':True},
     {'north':True, 'south':True, 'east':False, 'west':False},
     {'north':True, 'south':False, 'east':True, 'west':False}],
    
    [{'north':False, 'south':False, 'east':True, 'west':True},
     {'north':True, 'south':False, 'east':False, 'west':True},
     {'north':False, 'south':False, 'east':True, 'west':False}],
    
    [{'north':False, 'south':True, 'east':False, 'west':True},
     {'north':False, 'south':True, 'east':False, 'west':False},
     {'north':False, 'south':True, 'east':True, 'west':False}],
]
# Create an image
img = mlx1.mlx_new_image(k, width, length)
result = mlx1.mlx_get_data_addr(img)
data = result[0]        # memoryview
bpp = result[1]         # bits per pixel
size_line = result[2]   # bytes per line
fmt = result[3]         # format

print(f"bpp={bpp}, size_line={size_line}, fmt={fmt}")
print(f"data type: {type(data)}, len: {len(data)}")

# Function to put a pixel in the image
def put_pixel(x, y, color):
    """Put a pixel at (x, y) with the given color in the image data"""
    if 0 <= x < 400 and 0 <= y < 300:
        offset = y * size_line + x * 4
        if offset + 4 <= len(data):
            # BGRA format - individual byte writes
            data[offset] = color & 0xFF              # Blue
            data[offset + 1] = (color >> 8) & 0xFF   # Green
            data[offset + 2] = (color >> 16) & 0xFF  # Red
            data[offset + 3] = 0xFF                  # Alpha

# Fill entire image with blue first
print("Filling image...")
for y in range(length):
    for x in range(width):
        put_pixel(x, y, 0x000044)  # Dark blue background

# Draw red rectangle
# print("Drawing red rectangle...")

# Draw green circle
# print("Drawing green circle...")
# cx, cy, r = 300, 150, 50
# for y in range(cy - r, cy + r):
#     for x in range(cx - r, cx + r):
#         if (x - cx)**2 + (y - cy)**2 <= r**2:
#             put_pixel(x, y, 0x00FF00)

# # Draw white border
# print("Drawing white border...")
# for x in range(400):
#     put_pixel(x, 0, 0xFFFFFF)
#     put_pixel(x, 299, 0xFFFFFF)
# for y in range(300):
#     put_pixel(0, y, 0xFFFFFF)
#     put_pixel(399, y, 0xFFFFFF)
for y in range(400):
    if y > 40:
        put_pixel(y, 1, 0xFFFFFF)
        put_pixel(y, 0, 0xFFFFFF)

# def on_expose(param):
mlx1.mlx_put_image_to_window(k, win, img, 0, 0)

# mlx1.mlx_expose_hook(win, on_expose, None)

# Exit on ESC
def on_key(keycode, param):
    if keycode == 65307:
        mlx1.mlx_loop_exit(k)


mlx1.mlx_key_hook(win, on_key, None)

print("Starting loop - press ESC to exit")
mlx1.mlx_loop(k)
