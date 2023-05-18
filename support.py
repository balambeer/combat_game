import pygame as pg
import csv
from os import walk

def import_folder(path):
    img_list = []
    for _,_,img_files in walk(path):
        for img in img_files:
            image_surf = pg.image.load(path + "/" + img).convert_alpha()
            img_list.append(image_surf)
    return img_list

class CSVTable:
    def __init__(self, path):
        csv_table = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for (i, row) in enumerate(csv_reader):
                if i == 0:
                    header = row
                else:
                    csv_table.append(row)
                    
        self.header = header
        self.table = csv_table
        self.col_index = {}
        index = 0
        for col in self.header:
            self.col_index.update({col: index})
            index += 1
