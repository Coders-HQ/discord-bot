import json
from math import ceil
from static.paths import STATIC_DIR

class Resources:
    """Class to manage the resource list"""

    def __init__(self, path: str = STATIC_DIR / "resources.json"):
        with open(path) as file:
            self.data = json.load(file)

    def get_all_langs(self) -> list:
        """Get all languages"""
        return [k for k in self.data]

    def get_details(self, language: str) -> dict:
        """Returns the resources of the given language"""
        return self.data[language]

    def reload_resource(self, path: str=STATIC_DIR / "resources.json"):
        """Function to reload the existing resources"""
        with open(path) as file:
            self.data = json.load(file)

    def prepare_pagination(self, to_paginate: dict) -> list[list]:
        """To paginate the given dictionary to set of pages and contents"""
        total_items = len(to_paginate)
        r_count = ceil(total_items / 3)
        c_count = 3

        main = []
        for i in range(r_count):
            lst = []
            for j in range(c_count):
                d = {}
                idx_num = c_count * i + j
                if idx_num >= total_items:
                    break
                idx_txt = list(to_paginate.keys())[idx_num]
                d[idx_txt] = to_paginate[idx_txt]
                lst.append(d)
            main.append(lst)

        return main
