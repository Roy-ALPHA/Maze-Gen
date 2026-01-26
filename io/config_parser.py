import sys
from utils import errors


def checker_convert(configs: dict):
    keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in keys:
        if key in configs:
            if key in ["WIDTH", "HEIGHT"]:
                try:
                    configs[key] = int(configs.get(key))
                except ValueError:
                    raise errors.ConfigsError(f"Error: invalid '{key}' value (expected a positive integer)")
                if configs[key] <= 0:
                    raise errors.ConfigsError(f"Error: '{key}' must be positive integer")
            elif key == "PERFECT":
                if configs["PERFECT"] == "True":
                    configs["PERFECT"] = True
                elif configs["PERFECT"] == "False":
                    configs["PERFECT"] = False
                else:
                    raise errors.ConfigsError(f'Error: \'{key}\' must be either "True" or "False" (case-sensitive)')
            elif key == "OUTPUT_FILE":
                if configs.get(key).endswith(".txt") is False:
                    raise errors.ConfigsError("Error: invalid configuration file format (expected a .txt file)")
            elif key in ["ENTRY", "EXIT"]:
                if "," in configs.get(key):
                    try:
                        x, y = configs.get(key).split(",")
                        x = int(x)
                        y = int(y)
                        if x < 0 or y < 0:
                            raise errors.ConfigsError(f"Error: '{key}' coordinates must be non-negative integers")
                        configs[key] = (x, y)
                    except ValueError:
                        raise errors.ConfigsError(f"Error: invalid '{key}' coordinates format (expected exactly two integers: x,y)")
                else:
                    raise errors.ConfigsError(f"Error: invalid '{key}' coordinates format (expected exactly two integers: x,y)")
        else:
            raise errors.ConfigsError(f"Error: missing mandatory configuration key: '{key}'")


def parsing(file_obj, file: str) -> dict:
    configs = {}
    try:
        for line in file_obj:
            line = line.rstrip("\n")
            if not line or line[0] == '#':
                continue
            if "=" not in line or line.count("=") != 1:
                raise errors.ConfigsError(f"Error: invalid configuration line '{line}' (expected KEY=VALUE)")
            key, value = line.split("=", 1)
            configs.update({key.strip(): value.strip()})
    except PermissionError:
        raise errors.ConfigsError(f"Error: Cannot read '{file}'. Permission denied.")
    checker_convert(configs)
    return configs


if len(sys.argv) < 2:
    print("Error: configuration file argument missing")
    sys.exit(1)

file = sys.argv[1]
try:
    with open(file, "r") as f:
        try:
            configs = parsing(f, file)
            if configs["ENTRY"] == configs["EXIT"]:
                raise errors.ConfigsError("Error: 'ENTRY' and 'EXIT' cannot be the same cell")
        except errors.ConfigsError as e:
            print(f"{e}")
            sys.exit(1)
except FileNotFoundError:
    print(
        f"Error: Configuration file '{file}' not found. "
        "Please check the file path."
    )
    sys.exit(1)
x_entry, y_entry = configs["ENTRY"]
x_exit, y_exit = configs["EXIT"]
if not (0 <= x_entry < configs["WIDTH"]) or not (0 <= y_entry < configs["HEIGHT"]):
    print("Error: 'ENTRY' coordinates out of maze bounds")
    sys.exit(1)
if not (0 <= x_exit < configs["WIDTH"]) or not (0 <= y_exit < configs["HEIGHT"]):
    print("Error: 'EXIT' coordinates out of maze bounds")
    sys.exit(1)
