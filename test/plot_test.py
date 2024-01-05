from cProfile import label
import sys
import matplotlib.pyplot as plt

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

import utils.write_to_csv as write_to_csv

w_csv = write_to_csv.write_util()

if __name__ == "__main__":
    
    fig = plt.figure(figsize = (10, 10))
    canvas = fig.add_subplot(1, 1, 1)
    fuel_consumption_baseline = w_csv.read_csv('baseline/fuel_consumption.csv')
    fuel_consumption_main = w_csv.read_csv('main/fuel_consumption.csv')
    time_stamp_baseline = w_csv.read_csv('baseline/time_stamp.csv')
    time_stamp_main = w_csv.read_csv('main/time_stamp.csv')
    canvas.plot(time_stamp_baseline, fuel_consumption_baseline, 'c-', label = 'baseline', linewidth = 5.0)
    canvas.plot(time_stamp_main, fuel_consumption_main, 'g-', label = 'main', linewidth = 5.0)
    canvas.axvline(x = 63,ls = '-', c = 'red', linewidth = 2.5, label = 'all vehicles exist time')
    canvas.axvline(x = 80,ls = '-', c = 'red', linewidth = 2.5)
    
    canvas.set_xlabel('time_stamp', fontdict={"family": "Times New Roman", "size": 15})
    canvas.set_ylabel('fuel_consumption', fontdict={"family": "Times New Roman", "size": 15})
    
    canvas.annotate('all vehicles exit time', xy=(63, 30), xytext=(40, 31), arrowprops=dict(facecolor='green', shrink = 0.05),fontsize = 15, fontfamily = 'Times New Roman')
    canvas.annotate('all vehicles exit time', xy=(80, 140), xytext=(88, 141), arrowprops=dict(facecolor='cyan', shrink = 0.05),fontsize = 15, fontfamily = 'Times New Roman')
    fuel_main_total = 0
    fuel_baseline_total = 0
    
    for step in fuel_consumption_baseline:
        fuel_baseline_total += step
        
    for step in fuel_consumption_main:
        fuel_main_total += step
        
    print(fuel_main_total)
    print(fuel_baseline_total)
    
    plt.legend()
    plt.show()
    