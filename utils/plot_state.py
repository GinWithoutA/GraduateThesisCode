
import sys
import matplotlib.pyplot as plt

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

import utils.write_to_csv as write_to_csv

# 初始化
w_csv = write_to_csv.write_util()

# 画图的格式
fig_type = '3d'

platoon_CO2_emissions = []

platoon_CO_emissions = []

platoon_HC_emissions = []

platoon_PMx_emissions = []

platoon_NOx_emissions = []

platoon_fuel_consumption = []

platoon_noise_emissions = []

platoon_AWT = []

platoon_time_stamp_linear = []

# 车辆排的车辆 ID 集合
platoon = [['0', '1', '2', '3', '4'],               # platoon 1
           ['5', '6', '7'],                         # platoon 2
           ['8', '9'],                              # platoon 3
           ['10', '11', '12', '13', '14'],          # platoon 4     
           ['15', '16', '17', '18', '19'],          # platoon 5
           ['20', '21', '22'],                      # platoon 6
           ['23', '24', '25', '26'],                # platoon 7
           ['27'],                                  # platoon 8
           ['28', '29', '30'],                      # platoon 9
           ['31', '32', '33'],                      # platoon 10
           ['34', '35', '36', '37'],                # platoon 11
           ['38', '39', '40', '41', '42', '43'],    # platoon 12
           ['44', '45', '46', '47', '48'],          # platoon 13
           ['49', '50', '51', '52'],                # platoon 14
           ['53', '54', '55', '56', '57'],          # platoon 15
           ['58', '59', '60', '61', '62', '63'],    # platoon 16
           ['64', '65', '66', '67', '68', '69'],    # platoon 17
           ['70', '71', '72'],
           ['73', '74', '75', '76', '77'],
           ['78', '79'],
           ['80', '81', '82', '83'],
           ['84', '85', '86'],
           ['87', '88', '89', '90'],
           ['91', '92', '93', '94'],
           ['95', '96', '97', '98'],
           ['99', '100', '101', '102', '103', '104'],
           ['105', '106', '107', '108'],
           ['109', '110', '111', '112', '113'],
           ['114', '115', '116', '117'],
           ['118', '119', '120', '121', '122'],]                     # platoon 18


platoon_position_x = [  [[], [], [], [], []],          # platoon 1
                        [[], [], []],                  # platoon 2
                        [[], []],                      # platoon 3
                        [[], [], [], [], []],          # platoon 4     
                        [[], [], [], [], []],          # platoon 5
                        [[], [], []],                  # platoon 6
                        [[], [], [], []],              # platoon 7
                        [[]],                          # platoon 8
                        [[], [], []],                  # platoon 9
                        [[], [], []],                  # platoon 10
                        [[], [], [], []],              # platoon 11
                        [[], [], [], [], [], []],      # platoon 12
                        [[], [], [], [], []],          # platoon 13
                        [[], [], [], []],              # platoon 14
                        [[], [], [], [], []],          # platoon 15
                        [[], [], [], [], [], []],      # platoon 16
                        [[], [], [], [], [], []],      # platoon 17
                        [[], [], []],                 # platoon 18
                        [[], [], [], [], []],
                        [[], []],
                        [[], [], [], []],
                        [[], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],]

platoon_position_y = [  [[], [], [], [], []],          # platoon 1
                        [[], [], []],                  # platoon 2
                        [[], []],                      # platoon 3
                        [[], [], [], [], []],          # platoon 4     
                        [[], [], [], [], []],          # platoon 5
                        [[], [], []],                  # platoon 6
                        [[], [], [], []],              # platoon 7
                        [[]],                          # platoon 8
                        [[], [], []],                  # platoon 9
                        [[], [], []],                  # platoon 10
                        [[], [], [], []],              # platoon 11
                        [[], [], [], [], [], []],      # platoon 12
                        [[], [], [], [], []],          # platoon 13
                        [[], [], [], []],              # platoon 14
                        [[], [], [], [], []],          # platoon 15
                        [[], [], [], [], [], []],      # platoon 16
                        [[], [], [], [], [], []],      # platoon 17
                        [[], [], []],                 # platoon 18
                        [[], [], [], [], []],
                        [[], []],
                        [[], [], [], []],
                        [[], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],]

platoon_acceleration = [[[], [], [], [], []],          # platoon 1
                        [[], [], []],                  # platoon 2
                        [[], []],                      # platoon 3
                        [[], [], [], [], []],          # platoon 4     
                        [[], [], [], [], []],          # platoon 5
                        [[], [], []],                  # platoon 6
                        [[], [], [], []],              # platoon 7
                        [[]],                          # platoon 8
                        [[], [], []],                  # platoon 9
                        [[], [], []],                  # platoon 10
                        [[], [], [], []],              # platoon 11
                        [[], [], [], [], [], []],      # platoon 12
                        [[], [], [], [], []],          # platoon 13
                        [[], [], [], []],              # platoon 14
                        [[], [], [], [], []],          # platoon 15
                        [[], [], [], [], [], []],      # platoon 16
                        [[], [], [], [], [], []],      # platoon 17
                        [[], [], []],                 # platoon 18
                        [[], [], [], [], []],
                        [[], []],
                        [[], [], [], []],
                        [[], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],]

platoon_electricity_consumption = [ [[], [], [], [], []],          # platoon 1
                                    [[], [], []],                  # platoon 2
                                    [[], []],                      # platoon 3
                                    [[], [], [], [], []],          # platoon 4     
                                    [[], [], [], [], []],          # platoon 5
                                    [[], [], []],                  # platoon 6
                                    [[], [], [], []],              # platoon 7
                                    [[]],                          # platoon 8
                                    [[], [], []],                  # platoon 9
                                    [[], [], []],                  # platoon 10
                                    [[], [], [], []],              # platoon 11
                                    [[], [], [], [], [], []],      # platoon 12
                                    [[], [], [], [], []],          # platoon 13
                                    [[], [], [], []],              # platoon 14
                                    [[], [], [], [], []],          # platoon 15
                                    [[], [], [], [], [], []],      # platoon 16
                                    [[], [], [], [], [], []],      # platoon 17
                                    [[], [], []],                 # platoon 18
                                    [[], [], [], [], []],
                                    [[], []],
                                    [[], [], [], []],
                                    [[], [], []],
                                    [[], [], [], []],
                                    [[], [], [], []],
                                    [[], [], [], []],
                                    [[], [], [], [], [], []],
                                    [[], [], [], []],
                                    [[], [], [], [], []],
                                    [[], [], [], []],
                                    [[], [], [], [], []],]

platoon_waiting_time = [[[], [], [], [], []],          # platoon 1
                        [[], [], []],                  # platoon 2
                        [[], []],                      # platoon 3
                        [[], [], [], [], []],          # platoon 4     
                        [[], [], [], [], []],          # platoon 5
                        [[], [], []],                  # platoon 6
                        [[], [], [], []],              # platoon 7
                        [[]],                          # platoon 8
                        [[], [], []],                  # platoon 9
                        [[], [], []],                  # platoon 10
                        [[], [], [], []],              # platoon 11
                        [[], [], [], [], [], []],      # platoon 12
                        [[], [], [], [], []],          # platoon 13
                        [[], [], [], []],              # platoon 14
                        [[], [], [], [], []],          # platoon 15
                        [[], [], [], [], [], []],      # platoon 16
                        [[], [], [], [], [], []],      # platoon 17
                        [[], [], []],                  # platoon 18
                        [[], [], [], [], []],
                        [[], []],
                        [[], [], [], []],
                        [[], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],]

platoon_time_loss = [[[], [], [], [], []],          # platoon 1
                    [[], [], []],                  # platoon 2
                    [[], []],                      # platoon 3
                    [[], [], [], [], []],          # platoon 4     
                    [[], [], [], [], []],          # platoon 5
                    [[], [], []],                  # platoon 6
                    [[], [], [], []],              # platoon 7
                    [[]],                          # platoon 8
                    [[], [], []],                  # platoon 9
                    [[], [], []],                  # platoon 10
                    [[], [], [], []],              # platoon 11
                    [[], [], [], [], [], []],      # platoon 12
                    [[], [], [], [], []],          # platoon 13
                    [[], [], [], []],              # platoon 14
                    [[], [], [], [], []],          # platoon 15
                    [[], [], [], [], [], []],      # platoon 16
                    [[], [], [], [], [], []],      # platoon 17
                    [[], [], []],                 # platoon 18
                    [[], [], [], [], []],
                    [[], []],
                    [[], [], [], []],
                    [[], [], []],
                    [[], [], [], []],
                    [[], [], [], []],
                    [[], [], [], []],
                    [[], [], [], [], [], []],
                    [[], [], [], []],
                    [[], [], [], [], []],
                    [[], [], [], []],
                    [[], [], [], [], []],]

platoon_time_stamp = [  [[], [], [], [], []],          # platoon 1
                        [[], [], []],                  # platoon 2
                        [[], []],                      # platoon 3
                        [[], [], [], [], []],          # platoon 4     
                        [[], [], [], [], []],          # platoon 5
                        [[], [], []],                  # platoon 6
                        [[], [], [], []],              # platoon 7
                        [[]],                          # platoon 8
                        [[], [], []],                  # platoon 9
                        [[], [], []],                  # platoon 10
                        [[], [], [], []],              # platoon 11
                        [[], [], [], [], [], []],      # platoon 12
                        [[], [], [], [], []],          # platoon 13
                        [[], [], [], []],              # platoon 14
                        [[], [], [], [], []],          # platoon 15
                        [[], [], [], [], [], []],      # platoon 16
                        [[], [], [], [], [], []],      # platoon 17
                        [[], [], []],                 # platoon 18
                        [[], [], [], [], []],
                        [[], []],
                        [[], [], [], []],
                        [[], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],
                        [[], [], [], []],
                        [[], [], [], [], []],]

platoon_velocity = {'0': [[], []],
                    '1': [[], []], 
                    '2': [[], []],
                    '3': [[], []],
                    '4': [[], []],
                    '5': [[], []],
                    '6': [[], []],
                    '7': [[], []],
                    '8': [[], []],
                    '9': [[], []],
                    '10': [[], []],
                    '11': [[], []],
                    '12': [[], []],
                    '13': [[], []],
                    '14': [[], []],
                    '15': [[], []],
                    '16': [[], []],
                    '17': [[], []],
                    '18': [[], []],
                    '19': [[], []],
                    '20': [[], []],
                    '21': [[], []],
                    '22': [[], []],
                    '23': [[], []],
                    '24': [[], []],
                    '25': [[], []],
                    '26': [[], []],
                    '27': [[], []],
                    '28': [[], []],
                    '29': [[], []],
                    '30': [[], []],
                    '31': [[], []],
                    '32': [[], []],
                    '33': [[], []],
                    '34': [[], []],
                    '35': [[], []],
                    '36': [[], []],
                    '37': [[], []],
                    '38': [[], []],
                    '39': [[], []],
                    '40': [[], []],
                    '41': [[], []],
                    '42': [[], []],
                    '43': [[], []],
                    '44': [[], []],
                    '45': [[], []],
                    '46': [[], []],
                    '47': [[], []],
                    '48': [[], []],
                    '49': [[], []],
                    '50': [[], []],
                    '51': [[], []],
                    '52': [[], []],
                    '53': [[], []],
                    '54': [[], []],
                    '55': [[], []],
                    '56': [[], []],
                    '57': [[], []],
                    '58': [[], []],
                    '59': [[], []],
                    '60': [[], []],
                    '61': [[], []],
                    '62': [[], []],
                    '63': [[], []],
                    '64': [[], []],
                    '65': [[], []],
                    '66': [[], []],
                    '67': [[], []],
                    '68': [[], []],
                    '69': [[], []],
                    '70': [[], []],
                    '71': [[], []],
                    '72': [[], []],
                    '73': [[], []],
                    '74': [[], []],
                    '75': [[], []],
                    '76': [[], []],
                    '77': [[], []],
                    '78': [[], []],
                    '79': [[], []],
                    '80': [[], []],
                    '81': [[], []],
                    '82': [[], []],
                    '83': [[], []],
                    '84': [[], []],
                    '85': [[], []],
                    '86': [[], []],
                    '87': [[], []],
                    '88': [[], []],
                    '89': [[], []],
                    '90': [[], []],
                    '91': [[], []],
                    '92': [[], []],
                    '93': [[], []],
                    '94': [[], []],
                    '95': [[], []],
                    '96': [[], []],
                    '97': [[], []],
                    '98': [[], []],
                    '99': [[], []],
                    '100': [[], []],
                    '101': [[], []],
                    '102': [[], []],
                    '103': [[], []],
                    '104': [[], []],
                    '105': [[], []],
                    '106': [[], []],
                    '107': [[], []],
                    '108': [[], []],
                    '109': [[], []],
                    '110': [[], []],
                    '111': [[], []],
                    '112': [[], []],
                    '113': [[], []],
                    '114': [[], []],
                    '115': [[], []],
                    '116': [[], []],
                    '117': [[], []],
                    '118': [[], []],
                    '119': [[], []],
                    '120': [[], []],
                    '121': [[], []],
                    '122': [[], []],
                    '123': [[], []],
                    '124': [[], []],
                    '125': [[], []],
                    '126': [[], []],
                    '127': [[], []],
                    '128': [[], []],
                    '129': [[], []],
                    '130': [[], []]}

# platoon - [[solve_time], [step]]
platoon_solve_time = [  [[], []],   # platoon 0
                        [[], []],   # platoon 1
                        [[], []],   # platoon 2
                        [[], []],   # platoon 3
                        [[], []],   # platoon 4
                        [[], []],   # platoon 5
                        [[], []],   # platoon 6
                        [[], []],   # platoon 7
                        [[], []],   # platoon 8
                        [[], []],   # platoon 9
                        [[], []],   # platoon 10
                        [[], []],   # platoon 11
                        [[], []],   # platoon 12
                        [[], []],   # platoon 13
                        [[], []],   # platoon 14
                        [[], []],   # platoon 15
                        [[], []],   # platoon 16
                        [[], []],   # platoon 17
                        [[], []],   # platoon 18
                        [[], []],   # platoon 19
                        [[], []],   # platoon 20
                        [[], []],   # platoon 21
                        [[], []],   # platoon 22
                        [[], []],   # platoon 23
                        [[], []],   # platoon 24
                        [[], []],   # platoon 25
                        [[], []],   # platoon 26
                        [[], []],   # platoon 27
                        [[], []],   # platoon 28
                        [[], []],   # platoon 29
                        [[], []],   # platoon 30
                        ]

platoon_spacing_error = [  [[], []],   # platoon 0
                        [[], []],   # platoon 1
                        [[], []],   # platoon 2
                        [[], []],   # platoon 3
                        [[], []],   # platoon 4
                        [[], []],   # platoon 5
                        [[], []],   # platoon 6
                        [[], []],   # platoon 7
                        [[], []],   # platoon 8
                        [[], []],   # platoon 9
                        [[], []],   # platoon 10
                        [[], []],   # platoon 11
                        [[], []],   # platoon 12
                        [[], []],   # platoon 13
                        [[], []],   # platoon 14
                        [[], []],   # platoon 15
                        [[], []],   # platoon 16
                        [[], []],   # platoon 17
                        [[], []],   # platoon 18
                        [[], []],   # platoon 19
                        [[], []],   # platoon 20
                        [[], []],   # platoon 21
                        [[], []],   # platoon 22
                        [[], []],   # platoon 23
                        [[], []],   # platoon 24
                        [[], []],   # platoon 25
                        [[], []],   # platoon 26
                        [[], []],   # platoon 27
                        [[], []],   # platoon 28
                        [[], []],   # platoon 29
                        [[], []],   # platoon 30
                        ]
                  
plot_color = [  ["#DB7093", "#FF69B4", "#FF1493", "#C71585", "#FFC0CB"],               # platoon 1
                ["#8B008B", "#800080", "#BA55D3"],                                     # platoon 2
                ["#4B0082", "#8A2BE2"],                                                # platoon 3
                ["#0000FF", "#0000CD", "#191970", "#00008B", "#000080"],               # platoon 4     
                ["#778899", "#708090", "#1E90FF", "#4682B4", "#87CEFA"],               # platoon 5
                ["#ADD8E6", "#B0E0E6", "#5F9EA0"],                                     # platoon 6
                ["#D4F2E7", "#00CED1", "#2F4F4F", "#008B8B"],                          # platoon 7
                ["#40E0D0"],                                                           # platoon 8
                ["#7FFFAA", "#00FA9A", "#00FF7F"],                                     # platoon 9
                ["#228B22", "#008000", "#006400"],                                     # platoon 10
                ["#FFFF00", "#808000", "#BDB76B", "#FFFACD"],                          # platoon 11
                ["#F4A460", "#FF8C00", "#D2691E", "#8B4513", "#A0522D", "#FFA07A"],    # platoon 12
                ["#CD5C5C", "#FF0000", "#A52A2A", "#B22222", "#8B0000"],               # platoon 13
                ["#FF69B4", "#FF69B4", "#FF69B4", "#FF69B4"],                          # platoon 14
                ["#FF1493", "#FF1493", "#FF1493", "#FF1493", "#FF1493"],               # platoon 15
                ["#2F4F4F", "#2F4F4F", "#2F4F4F", "#2F4F4F", "#2F4F4F", "#2F4F4F"],    # platoon 16
                ["#008B8B", "#008B8B", "#008B8B", "#008B8B", "#008B8B", "#008B8B"],    # platoon 17
                ["#00FA9A", "#00FA9A", "#00FA9A"],                                    # platoon 18
                ["#87CEFA", "#87CEFA", "#87CEFA", "#87CEFA", "#87CEFA"],
                ["#8B0000", "#8B0000"],
                ["#DB7093", "#DB7093", "#DB7093", "#DB7093"],
                ["#C71585", "#C71585", "#C71585"],
                ["#FFC0CB", "#FFC0CB", "#FFC0CB", "#FFC0CB"],
                ["#8B008B", "#8B008B", "#8B008B", "#8B008B"],
                ["#800080", "#800080", "#800080", "#800080"],
                ["#BA55D3", "#BA55D3", "#BA55D3", "#BA55D3", "#BA55D3", "#BA55D3"],
                ["#4B0082", "#4B0082", "#4B0082", "#4B0082"],
                ["#8A2BE2", "#8A2BE2", "#8A2BE2", "#8A2BE2", "#8A2BE2"],
                ["#0000FF", "#0000FF", "#0000FF", "#0000FF"],
                ["#0000CD", "#0000CD", "#0000CD", "#0000CD", "#0000CD"],]

'''
    初始化位置、速度、加速度、间距误差、速度误差画板。

    Parameters:
        None
   
    Return:
        plot_position_state     - 位置画板
        plot_velocity_state     - 速度画板
        plot_space_error_state  - 间距误差画板
'''
def plot_init():
    fig_position = plt.figure(figsize = (10, 10))
    fig_velocity = plt.figure(figsize = (10, 10))
    fig_solve_time = plt.figure(figsize = (10, 10))
    fig_acceleration = plt.figure(figsize = (10, 10))
    fig_spacing_error = plt.figure(figsize = (10, 10))
    position_canvas = fig_position.add_subplot(projection = fig_type)
    velocity_canvas = fig_velocity.add_subplot(projection = fig_type)
    solve_time_canvas = fig_solve_time.add_subplot(projection = fig_type)
    acceleration_canvas = fig_acceleration.add_subplot(projection = fig_type)
    spacing_error_canvas = fig_spacing_error.add_subplot(projection = fig_type)
    return position_canvas, velocity_canvas, solve_time_canvas, acceleration_canvas, spacing_error_canvas

'''

'''
def single_plot_init(row, column):
    fig = plt.figure(figsize = (10, 10))
    canvas = []
    for i in range(1, (row * column) + 1):
        canvas.append(fig.add_subplot(row, column, i))
    return canvas

'''
    初始化性能指标画板。

    Parameters:
        None
   
    Return:
        plot_position_state     - 位置画板
        plot_velocity_state     - 速度画板
        plot_space_error_state  - 间距误差画板
'''
def indicator_plot_init():
    fig_CO2 = plt.figure(figsize = (10, 10))
    fig_CO = plt.figure(figsize = (10, 10))
    fig_HC = plt.figure(figsize = (10, 10))
    fig_PMx = plt.figure(figsize = (10, 10))
    fig_NOx = plt.figure(figsize = (10, 10))
    fig_fuel = plt.figure(figsize = (10, 10))
    fig_noise = plt.figure(figsize = (10, 10))
    fig_electricity = plt.figure(figsize = (10, 10))
    fig_WT = plt.figure(figsize = (10, 10))
    fig_AWT = plt.figure(figsize = (10, 10))
    fig_TL = plt.figure(figsize = (10, 10))
    CO2_canvas = fig_CO2.add_subplot(projection = fig_type)
    CO_canvas = fig_CO.add_subplot(projection = fig_type)
    HC_canvas = fig_HC.add_subplot(projection = fig_type)
    PMx_canvas = fig_PMx.add_subplot(projection = fig_type)
    NOx_canvas = fig_NOx.add_subplot(projection = fig_type)
    fuel_canvas = fig_fuel.add_subplot(projection = fig_type)
    noise_canvas = fig_noise.add_subplot(projection = fig_type)
    electricity_canvas = fig_electricity.add_subplot(projection = fig_type)
    WT_canvas = fig_WT.add_subplot(projection = fig_type)
    AWT_canvas = fig_AWT.add_subplot(projection = fig_type)
    TL_canvas = fig_TL.add_subplot(projection = fig_type)
    return CO2_canvas, CO_canvas, HC_canvas, PMx_canvas, NOx_canvas, fuel_canvas, noise_canvas, electricity_canvas, WT_canvas, AWT_canvas, TL_canvas

'''
    初始化性能指标画板（2D）。

    Parameters:
        None
   
    Return:
        plot_position_state     - 位置画板
        plot_velocity_state     - 速度画板
        plot_space_error_state  - 间距误差画板
'''
def indicator_plot_2D_init():
    fig_1 = plt.figure(figsize = (10, 10))
    fig_2 = plt.figure(figsize = (10 , 10))
    fig_3 = plt.figure(figsize = (10, 10))
    CO2_canvas = fig_1.add_subplot(2, 2, 1)
    CO_canvas = fig_1.add_subplot(2, 2, 2)
    HC_canvas = fig_1.add_subplot(2, 2, 3)
    PMx_canvas = fig_1.add_subplot(2, 2, 4)
    NOx_canvas = fig_2.add_subplot(2, 2, 1)
    fuel_canvas = fig_2.add_subplot(2, 2, 2)
    noise_canvas = fig_2.add_subplot(2, 2, 3)
    # electricity_canvas = fig.add_subplot(2, 5, 8)
    WT_canvas = fig_2.add_subplot(2, 2, 4)
    AWT_canvas = fig_3.add_subplot(2, 2, 1)
    TL_canvas = fig_3.add_subplot(2, 2, 2)
    return CO2_canvas, CO_canvas, HC_canvas, PMx_canvas, NOx_canvas, fuel_canvas, noise_canvas, WT_canvas, AWT_canvas, TL_canvas



'''
    更新求解时间，由于只有在使用 GUROBI 的时候才需要更新，不想位置和速度需要一直更新，因此不能使用和位置以及速度相同的时间戳来表示

    Parameters:
        ego_pla_index   - 当前车辆排的下标
        solve_time      - 求解时间
        step            - 时间戳
   
    Return:
        None
'''
def update_solve_time(ego_pla, solve_time, step):
    ego_pla_index = int(ego_pla)
    platoon_solve_time[ego_pla_index][0].append(solve_time)
    platoon_solve_time[ego_pla_index][1].append(step)

"""
    更新求解时间，由于只有在使用 GUROBI 的时候才需要更新，不想位置和速度需要一直更新，因此不能使用和位置以及速度相同的时间戳来表示

    Parameters:
        ego_pla_index   - 当前车辆排的下标
        solve_time      - 求解时间
        step            - 时间戳
   
    Return:
"""
def udpate_spacing_error(ego_pla, spacing_error, step):
    ego_pla_index = int(ego_pla)
    platoon_spacing_error[ego_pla_index][0].append(spacing_error)
    platoon_spacing_error[ego_pla_index][1].append(step)

"""
    处理所有状态信息的更新。

    Parameters:
        traci           - traci 接口
        all_vehicle_id  - 所有车辆的 ID
        step            - 当前时间步骤
        ego_pla_index   - 当前车辆排下标
   
    Return:
        None
"""
def update_state(traci, all_vehicle_id, step):
    fuel_consumption = 0
    NOx_emission = 0
    PMx_emission = 0
    HC_emission = 0
    CO_emmision = 0
    CO2_emmision = 0
    noise_emission = 0
    awt = 0
    veh_num = len(traci.vehicle.getIDList())
    for pla_index, ego_pla in enumerate(platoon):
        for veh_index, ego_veh in enumerate(ego_pla):
            if ego_veh in all_vehicle_id:
                x, y = traci.vehicle.getPosition(ego_veh)
                velocity = round(traci.vehicle.getSpeed(ego_veh), 2)
                acceleration = round(traci.vehicle.getAcceleration(ego_veh), 2)
                CO2_emmision += round(traci.vehicle.getCO2Emission(ego_veh) / 1000, 2)
                CO_emmision += round(traci.vehicle.getCOEmission(ego_veh) / 1000, 2)
                HC_emission += round(traci.vehicle.getHCEmission(ego_veh), 2)
                PMx_emission += round(traci.vehicle.getPMxEmission(ego_veh), 2)
                NOx_emission += round(traci.vehicle.getNOxEmission(ego_veh) / 1000, 2)
                fuel_consumption += round(traci.vehicle.getFuelConsumption(ego_veh) / 1000, 2)
                noise_emission += round(traci.vehicle.getNoiseEmission(ego_veh), 2)
                # electricity_consumption = round(traci.vehicle.getElectricityConsumption(ego_veh), 2)
                W_time = round(traci.vehicle.getWaitingTime(ego_veh), 2)
                awt += round(traci.vehicle.getAccumulatedWaitingTime(ego_veh), 2)
                time_loss = round(traci.vehicle.getTimeLoss(ego_veh))
                platoon_waiting_time[pla_index][veh_index].append(W_time)
                platoon_time_loss[pla_index][veh_index].append(time_loss)
                platoon_acceleration[pla_index][veh_index].append(acceleration)
                platoon_position_x[pla_index][veh_index].append(round(x, 2))
                platoon_position_y[pla_index][veh_index].append(round(y, 2))
                platoon_time_stamp[pla_index][veh_index].append(step)
                platoon_velocity[ego_veh][0].append(velocity)
                platoon_velocity[ego_veh][1].append(step)
             
    if veh_num > 0:
        platoon_AWT.append(awt)
        platoon_fuel_consumption.append(fuel_consumption)
        platoon_CO2_emissions.append(CO2_emmision)
        platoon_CO_emissions.append(CO_emmision)
        platoon_HC_emissions.append(HC_emission)
        platoon_PMx_emissions.append(PMx_emission)
        platoon_NOx_emissions.append(NOx_emission)
        platoon_noise_emissions.append(noise_emission) 
        platoon_time_stamp_linear.append(step)  
     
            

'''
    更新各自画布的初始状态（X，Y，Z）。

    Parameters:
        canvas    - 初始化的画布
        label     - 列表，分别为XYZ坐标轴的名字
   
    Return:
        None
'''
def initial_canvas(canvas, label):
    family = "Times New Roman"
    size = 15
    canvas.set_xlabel(label[0], fontdict={"family": family, "size": size})
    canvas.set_ylabel(label[1], fontdict={"family": family, "size": size})
    canvas.set_zlabel(label[2], fontdict={"family": family, "size": size})
    
'''
    更新各自画布的初始状态（X，Y）。

    Parameters:
        canvas    - 初始化的画布
        label     - 列表，分别为XY坐标轴的名字
   
    Return:
        None
'''
def initial_canvas_2D(canvas, label):
    family = "Times New Roman"
    size = 15
    canvas.set_xlabel(label[0], fontdict={"family": family, "size": size})
    canvas.set_ylabel(label[1], fontdict={"family": family, "size": size})

"""
    在对应的画布上显示对应的状态。

    Parameters:
        position_canvas     - 位置画布
        velocity_canvas     - 速度画布
        solve_time_canvas   - 求解时间画布
   
    Return:
        None
"""
def show_state(position_canvas, velocity_canvas, solve_time_canvas, acceleration_canvas, spacing_error_canvas):
    
    # 计算车辆的 ID
    veh_id = 0
    
    # 画车辆排的位置信息
    for pla_index, ego_pla in enumerate(platoon):
        for veh_index in range(len(ego_pla)):
            position_canvas.plot(platoon_position_x[pla_index][veh_index], platoon_position_y[pla_index][veh_index], platoon_time_stamp[pla_index][veh_index], color = plot_color[pla_index][veh_index])
            acceleration_canvas.plot(platoon_acceleration[pla_index][veh_index], platoon_time_stamp[pla_index][veh_index], veh_id)
            veh_id += 1
                      
    # 画车辆排的速度信息，velocity_state[key][0] = velocity, velocity_state[key][1] = step
    for key in platoon_velocity:
        velocity_canvas.plot(platoon_velocity[key][0], platoon_velocity[key][1], int(key))
    
    # 画车辆排的求解时间信息，platoon_solve_time_state[key][0] = solve_time, platoon_solve_time_state[key][1] = step
    for pla_index, pla in enumerate(platoon_solve_time):
        solve_time_canvas.plot(pla[0], pla[1], pla_index)
        print(pla[0], pla[1], pla_index)
        
    for pla_index, pla in enumerate(platoon_spacing_error):
        spacing_error_canvas.plot(pla[0], pla[1], pla_index)
        
    print('spacing_error:')
    print(platoon_spacing_error)
        
    
    initial_canvas(position_canvas, ["X_Position", "Y_Position", "Time_Stamp"])
    initial_canvas(velocity_canvas, ["Velocity", "Time_Stamp", "Vehicle_ID"])
    initial_canvas(solve_time_canvas, ["Solve_Time", "Time_Stamp", "Platoon_ID"])
    initial_canvas(acceleration_canvas, ["Vehicle_Acc", "Time_Stamp", "Vehicle_ID"])
    initial_canvas(spacing_error_canvas, ["Spacing_Error", "Time_Stamp", "Platoon_ID"])
    
'''
    在对应的画布上显示对应的状态（指标状态）

    Parameters:
        position_canvas     - 位置画布
        velocity_canvas     - 速度画布
        solve_time_canvas   - 求解时间画布
   
    Return:
        None
'''
def show_state_indicator(CO2_canvas, CO_canvas, HC_canvas, PMx_canvas, NOx_canvas, fuel_canvas, noise_canvas, WT_canvas, AWT_canvas, TL_canvas):
    
    # 画车辆排的性能指标信息
    for pla_index, ego_pla in enumerate(platoon):
        for veh_index in range(len(ego_pla)):
            WT_canvas.plot(platoon_time_stamp[pla_index][veh_index], platoon_waiting_time[pla_index][veh_index])
            TL_canvas.plot(platoon_time_stamp[pla_index][veh_index], platoon_time_loss[pla_index][veh_index])
    
    fuel_canvas.plot(platoon_time_stamp_linear, platoon_fuel_consumption)
    CO2_canvas.plot(platoon_time_stamp_linear, platoon_CO2_emissions)
    CO_canvas.plot(platoon_time_stamp_linear, platoon_CO_emissions)
    HC_canvas.plot(platoon_time_stamp_linear, platoon_HC_emissions)
    PMx_canvas.plot(platoon_time_stamp_linear, platoon_PMx_emissions)
    NOx_canvas.plot(platoon_time_stamp_linear, platoon_NOx_emissions)
    noise_canvas.plot(platoon_time_stamp_linear, platoon_noise_emissions)
    AWT_canvas.plot(platoon_time_stamp_linear, platoon_AWT)

    initial_canvas_2D(CO2_canvas, ["Time_Stamp", "CO2 (g/s)"])
    initial_canvas_2D(CO_canvas, ["Time_Stamp", "CO (g/s)"])
    initial_canvas_2D(HC_canvas, ["Time_Stamp", "HC (mg/s)"])
    initial_canvas_2D(PMx_canvas, ["Time_Stamp", "PMx (g/s)"])
    initial_canvas_2D(NOx_canvas, ["Time_Stamp", "NOx (g/s)"])
    initial_canvas_2D(fuel_canvas, ["Time_Stamp", "Feul (10^-3L)"])
    initial_canvas_2D(noise_canvas, ["Time_Stamp", "noise (dBA)"])
    initial_canvas_2D(WT_canvas, ["Time_Stamp", "Waitting Time (s)"])
    initial_canvas_2D(AWT_canvas, ["Time_Stamp", "Accumulated Waiting Time (s)"])
    initial_canvas_2D(TL_canvas, ["Time_Stamp", "Time Loss (s)"])
    
'''
    显示图片
'''
def show():
    plt.legend()
    plt.show()
  
'''
    将结果存入 csv 文件中
    
    Parameters:
        prefix - 文件的前缀，即文件存储的文件夹名称
   
    Return:
        None
    
'''  
def list_to_csv(prefix):
    w_csv.csv_file_init(prefix + 'AWT.csv', platoon_AWT)
    w_csv.csv_file_init(prefix + 'CO2_emmision.csv', platoon_CO2_emissions)
    w_csv.csv_file_init(prefix + 'CO_emmision.csv', platoon_CO_emissions)
    w_csv.csv_file_init(prefix + 'HC_emmision.csv', platoon_HC_emissions)
    w_csv.csv_file_init(prefix + 'PMx_emmision.csv', platoon_PMx_emissions)
    w_csv.csv_file_init(prefix + 'NOx_emmision.csv', platoon_NOx_emissions)
    w_csv.csv_file_init(prefix + 'fuel_consumption.csv', platoon_fuel_consumption)
    w_csv.csv_file_init(prefix + 'noise_emmision.csv', platoon_noise_emissions)
    w_csv.csv_file_init(prefix + 'time_stamp.csv', platoon_time_stamp_linear)
    
    
