from mlx import Mlx


ptr = Mlx()
l = ptr.mlx_init()
win = ptr.mlx_new_window(l, 500, 500, "hello")
img = ptr.mlx_new_image(l, 200, 200)
res = ptr.mlx_get_data_addr(img)
print(len(res[0]))