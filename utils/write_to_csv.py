
# 将数据输出到 csv 的工具类
import csv
import os
import sys
import pathlib as pl

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

class write_util:
    
    # different name attributes, where na means name attribute
    na_distance_center = ['step', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11', '12']
    na_platoon_to_origin_forward = ['ego_pla']
    
    read_path = './output_data'
    
    
    def __init__(self):
        pass
    
    def csv_file_init(self, csv_name, csv_content):
        # 要保存的 csv 文件路径
        csv_path = pl.Path('./output_data/', csv_name)
        if csv_path.is_file():
            os.remove(csv_path)
        open_csv = open(csv_path, "w+", newline = '')
        try:
            writer = csv.writer(open_csv)
            writer.writerow(csv_content)
        finally:
            open_csv.close()
    
    def update_csv(self, info):
        open_csv_file = open(self.csv_path, "a+", newline='')
        try:
            writer = csv.writer(open_csv_file)
            writer.writerow(info)
        finally:
            open_csv_file.close()
            
    def distance_center_csv(self, platoon_distance):
        if self.csv_path.is_file():
            self.update_csv(platoon_distance)
        else:
            self.csv_file_init("distance_center")
    
    '''
        读取 csv 文件
    '''
    def read_csv(self, csv_name):
        content = []
        csv_path = pl.Path('./output_data/', csv_name)
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                content = line
        return list(map(float, content))