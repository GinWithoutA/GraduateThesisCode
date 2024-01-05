import sys
import matplotlib.pyplot as plt

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

import utils.write_to_csv as write_to_csv
import utils.plot_state as u_plt

w_csv = write_to_csv.write_util()

def get_baseline_indicator(baseline_prefix):
    awt = w_csv.read_csv(baseline_prefix + 'AWT.csv')
    CO_emmision = w_csv.read_csv(baseline_prefix + 'CO_emmision.csv')
    CO2_emmision = w_csv.read_csv(baseline_prefix + 'CO2_emmision.csv')
    HC_emmision = w_csv.read_csv(baseline_prefix + 'HC_emmision.csv')
    NOx_emmision = w_csv.read_csv(baseline_prefix + 'NOx_emmision.csv')
    PMx_emmision = w_csv.read_csv(baseline_prefix + 'PMx_emmision.csv')
    fuel_consumption = w_csv.read_csv(baseline_prefix + 'fuel_consumption.csv')
    time_stamp = w_csv.read_csv(baseline_prefix + 'time_stamp.csv')
    return dictionary_construction(CO_emmision, CO2_emmision, HC_emmision, NOx_emmision, PMx_emmision, fuel_consumption, time_stamp, awt)

def get_main_indicator(main_prefix):
    awt = w_csv.read_csv(main_prefix + 'AWT.csv')
    CO_emmision = w_csv.read_csv(main_prefix + 'CO_emmision.csv')
    CO2_emmision = w_csv.read_csv(main_prefix + 'CO2_emmision.csv')
    HC_emmision = w_csv.read_csv(main_prefix + 'HC_emmision.csv')
    NOx_emmision = w_csv.read_csv(main_prefix + 'NOx_emmision.csv')
    PMx_emmision = w_csv.read_csv(main_prefix + 'PMx_emmision.csv')
    fuel_consumption = w_csv.read_csv(main_prefix + 'fuel_consumption.csv')
    time_stamp = w_csv.read_csv(main_prefix + 'time_stamp.csv')
    return dictionary_construction(CO_emmision, CO2_emmision, HC_emmision, NOx_emmision, PMx_emmision, fuel_consumption, time_stamp, awt)

def dictionary_construction(CO_emmision, CO2_emmision, HC_emmision, NOx_emmision, PMx_emmision, fuel_consumption, time_stamp, awt):
    return {
        'CO_emmision': CO_emmision,
        'CO2_emmision': CO2_emmision,
        'HC_emmision': HC_emmision,
        'NOx_emmision': NOx_emmision,
        'PMx_emmision': PMx_emmision,
        'fuel_consumption': fuel_consumption,
        'time_stamp': time_stamp,
        'awt': awt,
    }
    
def get_total_consumption(indicator):
    total_consumption = {}
    for key in indicator:
        if key == 'time_stamp':
            total_consumption[key] = indicator[key][-1]
            continue
        tmp = 0
        for item in indicator[key]:
            tmp += item
        total_consumption[key] = tmp
    return total_consumption

def show_indicator():
    
    CO_canvas, CO2_canvas, NOx_canvas, PMx_canvas = u_plt.single_plot_init(2, 2)
    canvas = u_plt.single_plot_init(2, 2)
    fuel_canvas = canvas[0]
    awt_canvas = canvas[1]
    baseline_high_traffic_8 = get_baseline_indicator('baseline_high_traffic_8/')
    baseline_high_traffic_12 = get_baseline_indicator('baseline_high_traffic_12/')
    baseline_low_traffic_8 = get_baseline_indicator('baseline_low_traffic_8/')
    baseline_low_traffic_12 = get_baseline_indicator('baseline_low_traffic_12/')
    high_traffic_8 = get_main_indicator('high_traffic_8/')
    high_traffic_12 = get_main_indicator('high_traffic_12/')
    low_traffic_8 = get_main_indicator('low_traffic_8/')
    low_traffic_12 = get_main_indicator('low_traffic_12/')
    
    baseline_total = get_total_consumption(baseline_high_traffic_8)
    main_total = get_total_consumption(high_traffic_8)
    
    CO_canvas.set_xlabel('time stamp (a)', fontdict={"family": "Times New Roman", "size": 15})
    CO_canvas.set_ylabel('CO_emission', fontdict={"family": "Times New Roman", "size": 15})
    
    CO2_canvas.set_xlabel('time stamp (b)', fontdict={"family": "Times New Roman", "size": 15})
    CO2_canvas.set_ylabel('CO2_emission', fontdict={"family": "Times New Roman", "size": 15})
    
    # HC_canvas.set_xlabel('time_stamp', fontdict={"family": "Times New Roman", "size": 15})
    # HC_canvas.set_ylabel('HC_emmision', fontdict={"family": "Times New Roman", "size": 15})
    
    NOx_canvas.set_xlabel('time stamp (c)', fontdict={"family": "Times New Roman", "size": 15})
    NOx_canvas.set_ylabel('NOx_emission', fontdict={"family": "Times New Roman", "size": 15})
    
    PMx_canvas.set_xlabel('time stamp (d)', fontdict={"family": "Times New Roman", "size": 15})
    PMx_canvas.set_ylabel('PMx_emission', fontdict={"family": "Times New Roman", "size": 15})
    
    fuel_canvas.set_xlabel('time_stamp', fontdict={"family": "Times New Roman", "size": 15})
    fuel_canvas.set_ylabel('fuel_consumption', fontdict={"family": "Times New Roman", "size": 15})
    
    awt_canvas.set_xlabel('time_stamp', fontdict={"family": "Times New Roman", "size": 15})
    awt_canvas.set_ylabel('Accumulated waiting time', fontdict={"family": "Times New Roman", "size": 15})
    
    awt_canvas.plot(baseline_high_traffic_8['time_stamp'], baseline_high_traffic_8['awt'], color='slateblue', linestyle='-', label = 'baseline_high_8', linewidth = 3.5)
    awt_canvas.plot(baseline_high_traffic_12['time_stamp'], baseline_high_traffic_12['awt'], color='blue', linestyle='-', label = 'baseline_high_12', linewidth = 3.5)
    awt_canvas.plot(baseline_low_traffic_8['time_stamp'], baseline_low_traffic_8['awt'], color='fuchsia', linestyle='-', label = 'baseline_low_8', linewidth = 3.5)
    awt_canvas.plot(baseline_low_traffic_12['time_stamp'], baseline_low_traffic_12['awt'], color='deeppink', linestyle='-', label = 'baseline_low_12', linewidth = 3.5)
    awt_canvas.plot(high_traffic_8['time_stamp'], high_traffic_8['awt'], color='black', linestyle='-', label = 'high_8', linewidth = 3.5)
    awt_canvas.plot(high_traffic_12['time_stamp'], high_traffic_12['awt'], color='darkgreen', linestyle='-', label = 'high_12', linewidth = 3.5)
    awt_canvas.plot(low_traffic_8['time_stamp'], low_traffic_8['awt'], color='dodgerblue', linestyle='-', label = 'low_8', linewidth = 3.5)
    awt_canvas.plot(low_traffic_12['time_stamp'], low_traffic_12['awt'], color='salmon', linestyle='-', label = 'low_12', linewidth = 3.5)
    awt_canvas.legend()
    
    CO_canvas.plot(baseline_high_traffic_8['time_stamp'], baseline_high_traffic_8['CO_emmision'], color='slateblue', linestyle='-', label = 'baseline_high_8', linewidth = 3.5)
    CO_canvas.plot(baseline_high_traffic_12['time_stamp'], baseline_high_traffic_12['CO_emmision'], color='blue', linestyle='-', label = 'baseline_high_12', linewidth = 3.5)
    CO_canvas.plot(baseline_low_traffic_8['time_stamp'], baseline_low_traffic_8['CO_emmision'], color='fuchsia', linestyle='-', label = 'baseline_low_8', linewidth = 3.5)
    CO_canvas.plot(baseline_low_traffic_12['time_stamp'], baseline_low_traffic_12['CO_emmision'], color='deeppink', linestyle='-', label = 'baseline_low_12', linewidth = 3.5)
    CO_canvas.plot(high_traffic_8['time_stamp'], high_traffic_8['CO_emmision'], color='black', linestyle='-', label = 'high_8', linewidth = 3.5)
    CO_canvas.plot(high_traffic_12['time_stamp'], high_traffic_12['CO_emmision'], color='darkgreen', linestyle='-', label = 'high_12', linewidth = 3.5)
    CO_canvas.plot(low_traffic_8['time_stamp'], low_traffic_8['CO_emmision'], color='dodgerblue', linestyle='-', label = 'low_8', linewidth = 3.5)
    CO_canvas.plot(low_traffic_12['time_stamp'], low_traffic_12['CO_emmision'], color='salmon', linestyle='-', label = 'low_12', linewidth = 3.5)
    CO_canvas.legend()
    
    CO2_canvas.plot(baseline_high_traffic_8['time_stamp'], baseline_high_traffic_8['CO2_emmision'], color='slateblue', linestyle='-', label = 'baseline_high_8', linewidth = 3.5)
    CO2_canvas.plot(baseline_high_traffic_12['time_stamp'], baseline_high_traffic_12['CO2_emmision'], color='blue', linestyle='-', label = 'baseline_high_12', linewidth = 3.5)
    CO2_canvas.plot(baseline_low_traffic_8['time_stamp'], baseline_low_traffic_8['CO2_emmision'], color='fuchsia', linestyle='-', label = 'baseline_low_8', linewidth = 3.5)
    CO2_canvas.plot(baseline_low_traffic_12['time_stamp'], baseline_low_traffic_12['CO2_emmision'], color='deeppink', linestyle='-', label = 'baseline_low_12', linewidth = 3.5)
    CO2_canvas.plot(high_traffic_8['time_stamp'], high_traffic_8['CO2_emmision'], color='black', linestyle='-', label = 'high_8', linewidth = 3.5)
    CO2_canvas.plot(high_traffic_12['time_stamp'], high_traffic_12['CO2_emmision'], color='darkgreen', linestyle='-', label = 'high_12', linewidth = 3.5)
    CO2_canvas.plot(low_traffic_8['time_stamp'], low_traffic_8['CO2_emmision'], color='dodgerblue', linestyle='-', label = 'low_8', linewidth = 3.5)
    CO2_canvas.plot(low_traffic_12['time_stamp'], low_traffic_12['CO2_emmision'], color='salmon', linestyle='-', label = 'low_12', linewidth = 3.5)
    CO2_canvas.legend()
    
    # HC_canvas.plot(baseline_indicator['time_stamp'], baseline_indicator['HC_emmision'], 'c-', label = 'baseline', linewidth = 3.5)
    # HC_canvas.plot(main_indicator['time_stamp'], main_indicator['HC_emmision'], 'g-', label = 'main', linewidth = 3.5)
    # HC_canvas.legend()
    
    NOx_canvas.plot(baseline_high_traffic_8['time_stamp'], baseline_high_traffic_8['NOx_emmision'], color='slateblue', linestyle='-', label = 'baseline_high_8', linewidth = 3.5)
    NOx_canvas.plot(baseline_high_traffic_12['time_stamp'], baseline_high_traffic_12['NOx_emmision'], color='blue', linestyle='-', label = 'baseline_high_12', linewidth = 3.5)
    NOx_canvas.plot(baseline_low_traffic_8['time_stamp'], baseline_low_traffic_8['NOx_emmision'], color='fuchsia', linestyle='-', label = 'baseline_low_8', linewidth = 3.5)
    NOx_canvas.plot(baseline_low_traffic_12['time_stamp'], baseline_low_traffic_12['NOx_emmision'], color='deeppink', linestyle='-', label = 'baseline_low_12', linewidth = 3.5)
    NOx_canvas.plot(high_traffic_8['time_stamp'], high_traffic_8['NOx_emmision'], color='black', linestyle='-', label = 'high_8', linewidth = 3.5)
    NOx_canvas.plot(high_traffic_12['time_stamp'], high_traffic_12['NOx_emmision'], color='darkgreen', linestyle='-', label = 'high_12', linewidth = 3.5)
    NOx_canvas.plot(low_traffic_8['time_stamp'], low_traffic_8['NOx_emmision'], color='dodgerblue', linestyle='-', label = 'low_8', linewidth = 3.5)
    NOx_canvas.plot(low_traffic_12['time_stamp'], low_traffic_12['NOx_emmision'], color='salmon', linestyle='-', label = 'low_12', linewidth = 3.5)
    NOx_canvas.legend()
    
    PMx_canvas.plot(baseline_high_traffic_8['time_stamp'], baseline_high_traffic_8['PMx_emmision'], color='slateblue', linestyle='-', label = 'baseline_high_8', linewidth = 3.5)
    PMx_canvas.plot(baseline_high_traffic_12['time_stamp'], baseline_high_traffic_12['PMx_emmision'], color='blue', linestyle='-', label = 'baseline_high_12', linewidth = 3.5)
    PMx_canvas.plot(baseline_low_traffic_8['time_stamp'], baseline_low_traffic_8['PMx_emmision'], color='fuchsia', linestyle='-', label = 'baseline_low_8', linewidth = 3.5)
    PMx_canvas.plot(baseline_low_traffic_12['time_stamp'], baseline_low_traffic_12['PMx_emmision'], color='deeppink', linestyle='-', label = 'baseline_low_12', linewidth = 3.5)
    PMx_canvas.plot(high_traffic_8['time_stamp'], high_traffic_8['PMx_emmision'], color='black', linestyle='-', label = 'high_8', linewidth = 3.5)
    PMx_canvas.plot(high_traffic_12['time_stamp'], high_traffic_12['PMx_emmision'], color='darkgreen', linestyle='-', label = 'high_12', linewidth = 3.5)
    PMx_canvas.plot(low_traffic_8['time_stamp'], low_traffic_8['PMx_emmision'], color='dodgerblue', linestyle='-', label = 'low_8', linewidth = 3.5)
    PMx_canvas.plot(low_traffic_12['time_stamp'], low_traffic_12['PMx_emmision'], color='salmon', linestyle='-', label = 'low_12', linewidth = 3.5)
    PMx_canvas.legend()
    
    fuel_canvas.plot(baseline_high_traffic_8['time_stamp'], baseline_high_traffic_8['fuel_consumption'], color='slateblue', linestyle='-', label = 'baseline_high_8', linewidth = 3.5)
    fuel_canvas.plot(baseline_high_traffic_12['time_stamp'], baseline_high_traffic_12['fuel_consumption'], color='blue', linestyle='-', label = 'baseline_high_12', linewidth = 3.5)
    fuel_canvas.plot(baseline_low_traffic_8['time_stamp'], baseline_low_traffic_8['fuel_consumption'], color='fuchsia', linestyle='-', label = 'baseline_low_8', linewidth = 3.5)
    fuel_canvas.plot(baseline_low_traffic_12['time_stamp'], baseline_low_traffic_12['fuel_consumption'], color='deeppink', linestyle='-', label = 'baseline_low_12', linewidth = 3.5)
    fuel_canvas.plot(high_traffic_8['time_stamp'], high_traffic_8['fuel_consumption'], color='black', linestyle='-', label = 'high_8', linewidth = 3.5)
    fuel_canvas.plot(high_traffic_12['time_stamp'], high_traffic_12['fuel_consumption'], color='darkgreen', linestyle='-', label = 'high_12', linewidth = 3.5)
    fuel_canvas.plot(low_traffic_8['time_stamp'], low_traffic_8['fuel_consumption'], color='dodgerblue', linestyle='-', label = 'low_8', linewidth = 3.5)
    fuel_canvas.plot(low_traffic_12['time_stamp'], low_traffic_12['fuel_consumption'], color='salmon', linestyle='-', label = 'low_12', linewidth = 3.5)
    fuel_canvas.legend()
    
    # print(main_total)
    # print(baseline_total)
    
    plt.show()
    
    # CO: 31.1%, CO2: 18.61%, HC: 25.32%, NOx: 13.25%, PMx:6.43%, fuel: 18.63%
    

    

if __name__ == "__main__":
    
    # fig = plt.figure(figsize = (10, 10))
    # canvas = fig.add_subplot(1, 1, 1)
    # canvas.plot(time_stamp_baseline, fuel_consumption_baseline, 'c-', label = 'baseline', linewidth = 5.0)
    # canvas.plot(time_stamp_main, fuel_consumption_main, 'g-', label = 'main', linewidth = 5.0)
    # canvas.axvline(x = 63,ls = '-', c = 'red', linewidth = 2.5, label = 'all vehicles exist time')
    # canvas.axvline(x = 80,ls = '-', c = 'red', linewidth = 2.5)
    
    # canvas.set_xlabel('time_stamp', fontdict={"family": "Times New Roman", "size": 15})
    # canvas.set_ylabel('fuel_consumption', fontdict={"family": "Times New Roman", "size": 15})
    
    # canvas.annotate('all vehicles exit time', xy=(63, 30), xytext=(40, 31), arrowprops=dict(facecolor='green', shrink = 0.05),fontsize = 15, fontfamily = 'Times New Roman')
    # canvas.annotate('all vehicles exit time', xy=(80, 140), xytext=(88, 141), arrowprops=dict(facecolor='cyan', shrink = 0.05),fontsize = 15, fontfamily = 'Times New Roman')
    # fuel_main_total = 0
    # fuel_baseline_total = 0
    
    # for consumption in fuel_consumption_baseline:
    #     fuel_baseline_total += consumption
        
    # for consumption in fuel_consumption_main:
    #     fuel_main_total += consumption
        
    # print(fuel_main_total)
    # print(fuel_baseline_total)
    
    # plt.legend()
    # plt.show()
    
    show_indicator()