try:
    import commentjson as json_
except ImportError:
    import json as json_


dumps = json_.dumps
loads = json_.loads
