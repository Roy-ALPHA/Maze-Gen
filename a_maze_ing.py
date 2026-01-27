import sys
from configs.config_parser import parser
from render.render import mlx_render
from utils.errors import InvalidCoordinates

if len(sys.argv) < 2:
    print("Error: configuration file argument missing")
    sys.exit(1)

file = sys.argv[1]
configs = parser(file)
try:
    mlx_render(
        configs.get("WIDTH"),
        configs.get("HEIGHT"),
        configs.get("ENTRY"),
        configs.get("EXIT"))
except (ModuleNotFoundError, InvalidCoordinates) as e:
    print(e)
    exit()
