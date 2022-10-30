import json
import time
from os.path import join


class Abc:
    def __init__(self):
        self.name = "arne"

    def __jsonrepr__(self):
        return self.__dict__


class Doc:
    def __init__(self):
        self.abc = Abc()

    def __jsonrepr__(self):
        return self.__dict__


def complexHandler(obj):
    print(type(obj))
    import numpy
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, numpy.int32):
        return int(obj)
    if hasattr(obj, '__jsonrepr__'):
        return obj.__jsonrepr__()
    else:
        raise TypeError(f"Object of type {type(obj)} is not serializable.")


def save_to_json(obj, file_directory):
    datetime_str = time.strftime("%Y%m%d-%H%M%S")
    obj_name = type(obj).__name__
    file_name = f"{datetime_str}_{obj_name}.json"
    filepath = join(file_directory, file_name)

    with open(filepath, 'w') as fp:
        json.dump(obj, fp, default=complexHandler, indent=4)
