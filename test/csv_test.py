import sys
import os

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

import utils.write_to_csv as write_to_csv

w_csv = write_to_csv.write_util()

file_name_list = os.listdir('./output_data')

print(file_name_list)