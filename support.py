import pygame as pg
from os import walk

def import_folder(path):
    img_list = []
    for _,_,img_files in walk(path):
        for img in img_files:
            image_surf = pg.image.load(path + "/" + img).convert_alpha()
            img_list.append(image_surf)
    return img_list