# -*- encoding:utf-8 -*-

small_label_color = {
    "background": {"color": (0, 0, 0), "cls": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "cls_num": 0},
    "road": {"color": (128, 0, 0), "cls": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "cls_num": 1},
    "residence": {"color": (0, 255, 0), "cls": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "cls_num": 2},
    "industry": {"color": (128, 128, 0), "cls": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], "cls_num": 3},
    "greenland": {"color": (0, 0, 128), "cls": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], "cls_num": 4},
    "uncompleted": {"color": (128, 0, 128), "cls": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], "cls_num": 5},
    "forest": {"color": (0, 128, 128), "cls": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], "cls_num": 6},
    "playground": {"color": (128, 128, 128), "cls": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], "cls_num": 7},
    "waterbody": {"color": (64, 0, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], "cls_num": 8},
    "village": {"color": (192, 0, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], "cls_num": 9},
    "service": {"color": (64, 128, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], "cls_num": 10},
    "farmland": {"color": (128, 64, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], "cls_num": 11},
    "other": {"color": (64, 128, 128), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], "cls_num": 12}
}


small_cls_color = {
    0: {"color": (0, 0, 0), "cls": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "label": "background"},
    1: {"color": (128, 0, 0), "cls": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "label": "road"},
    2: {"color": (0, 255, 0), "cls": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "label": "residence"},
    3: {"color": (128, 128, 0), "cls": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], "label": "industry"},
    4: {"color": (0, 0, 128), "cls": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], "label": "greenland"},
    5: {"color": (128, 0, 128), "cls": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], "label": "uncompleted"},
    6: {"color": (0, 128, 128), "cls": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], "label": "forest"},
    7: {"color": (128, 128, 128), "cls": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], "label": "playground"},
    8: {"color": (64, 0, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], "label": "waterbody"},
    9: {"color": (192, 0, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], "label": "village"},
    10: {"color": (64, 128, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], "label": "service"},
    11: {"color": (128, 64, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], "label": "farmland"},
    12: {"color": (64, 128, 128), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], "label": "other"}
}

big_cls_color = {
    "1": {"color": (128, 0, 0), "cls": [0, 1, 0, 0, 0, 0, 0, 0, 0], "label": "residential_area"},
    "2": {"color": (0, 255, 0), "cls": [0, 0, 1, 0, 0, 0, 0, 0, 0], "label": "industry_area"},
    "3": {"color": (128, 128, 0), "cls": [0, 0, 0, 1, 0, 0, 0, 0, 0], "label": "server_area"},
    "4": {"color": (0, 0, 128), "cls": [0, 0, 0, 0, 1, 0, 0, 0, 0], "label": "village_area"},
    "5": {"color": (128, 0, 128), "cls": [0, 0, 0, 0, 0, 1, 0, 0, 0], "label": "forest_area"},
    "6": {"color": (0, 128, 128), "cls": [0, 0, 0, 0, 0, 0, 1, 0, 0], "label": "farmland_area"},
    "7": {"color": (128, 128, 128), "cls": [0, 0, 0, 0, 0, 0, 0, 1, 0], "label": "uncompleted_area"},
    "8": {"color": (64, 0, 0), "cls": [0, 0, 0, 0, 0, 0, 0, 0, 1], "label": "mainroad"}
}

big_color_cls = {
    (0, 0, 0): {"cls_num": 0, "cls": [1, 0, 0, 0, 0, 0, 0, 0, 0], "label": "back_ground"},
    (128, 0, 0): {"cls_num": 1, "cls": [0, 1, 0, 0, 0, 0, 0, 0, 0], "label": "residential_area"},
    (0, 255, 0): {"cls_num": 2, "cls": [0, 0, 1, 0, 0, 0, 0, 0, 0], "label": "industry_area"},
    (128, 128, 0): {"cls_num": 3, "cls": [0, 0, 0, 1, 0, 0, 0, 0, 0], "label": "server_area"},
    (0, 0, 128): {"cls_num": 4, "cls": [0, 0, 0, 0, 1, 0, 0, 0, 0], "label": "village_area"},
    (128, 0, 128): {"cls_num": 5, "cls": [0, 0, 0, 0, 0, 1, 0, 0, 0], "label": "forest_area"},
    (0, 128, 128): {"cls_num": 6, "cls": [0, 0, 0, 0, 0, 0, 1, 0, 0], "label": "farmland_area"},
    (128, 128, 128): {"cls_num": 7, "cls": [0, 0, 0, 0, 0, 0, 0, 1, 0], "label": "uncompleted_area"},
    (64, 0, 0): {"cls_num": 8, "cls": [0, 0, 0, 0, 0, 0, 0, 0, 1], "label": "mainroad"}
}

small_color_cls = {
    (0, 0, 0): {"cls_num": 0, "cls": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "label": "background"},
    (128, 0, 0): {"cls_num": 1, "cls": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "label": "road"},
    (0, 255, 0): {"cls_num": 2, "cls": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "label": "residence"},
    (128, 128, 0): {"cls_num": 3, "cls": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], "label": "industry"},
    (0, 0, 128): {"cls_num": 4, "cls": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], "label": "greenland"},
    (128, 0, 128): {"cls_num": 5, "cls": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], "label": "uncompleteland"},
    (0, 128, 128): {"cls_num": 6, "cls": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], "label": "forest"},
    (128, 128, 128): {"cls_num": 7, "cls": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], "label": "playground"},
    (64, 0, 0): {"cls_num": 8, "cls": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], "label": "water"},
    (192, 0, 0): {"cls_num": 9, "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], "label": "village"},
    (64, 128, 0): {"cls_num": 10, "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], "label": "service"},
    (128, 64, 0): {"cls_num": 11, "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], "label": "farmland"},
    (64, 128, 128): {"cls_num": 12, "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], "label":"others"},
    (192, 128, 0):{"cls_num": 13, "cls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], "label":"others"}
}

if __name__ == "__main__":
    pass