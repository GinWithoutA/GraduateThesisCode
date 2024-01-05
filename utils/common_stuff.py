'''
    通用模块
'''

import sys

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

# 导入自定义的包
import enums.platoon_flag as enum_pf

# 采样时间间隔
delta = 1

# 交叉口中心冲突区域的半径
central_radius = 13.6

# 控制输入的上下界
u_max = 2.0
u_min = -2.0

# 交叉口车辆速度的上下界
v_max = 15
v_min = 6

# 车辆位置的上下界，由于 Gurobi 变量的默认下界为 0，然而这 里的位置信息可以为负，所以也需要对位置进行设置
p_max = 2000
p_min = -2000

# 理想间距，10m
desire_space = 10

# 车辆排内部的理想间距，10m
desired_space_inside = 10

# 预测区间
predictive_horizon = 8

# 不同目标函数的权重
position_weight = 2
velocity_weight = 1
control_input_weight = 1

# 设置间距阈值，这里给它设置成 30m
space_threshold = 100

# desire speed of intersection
desire_velocity = 12

lane_ender = {'W0': [-13.6, -8], 'W1': [-13.6, -4.8], 'W2': [-13.6, -1.6],
              'N0': [-8, 13.6],  'N1': [-4.8, 13.6],  'N2': [-1.6, 13.6],
              'E0': [13.6, 8],   'E1': [13.6, 4.8],   'E2': [13.6, 1.6],
              'S0': [8, -13.6],  'S1': [4.8, -13.6],  'S2': [1.6, -13.6]}

# 车辆排及相关参数集合，[vehicle_ID, pre_platoon, optimal_control, last_vehicle_state, solve_time, road_ender_position]
platoon = {'0':  [['0', '1', '2', '3', '4'], -1, [], [], 0, lane_ender['E2']],                # platoon 1
           '1':  [['5', '6', '7'], -1, [], [], 0, lane_ender['W1']],                          # platoon 2
           '2':  [['8', '9'], -1, [], [], 0, lane_ender['N2']],                               # platoon 3
           '3':  [['10', '11', '12', '13', '14'], -1, [], [], 0, lane_ender['S0']],           # platoon 4     
           '4':  [['15', '16', '17', '18', '19'], -1, [], [], 0, lane_ender['N0']],           # platoon 5
           '5':  [['20', '21', '22'], -1, [], [], 0, lane_ender['E2']],                       # platoon 6
           '6':  [['23', '24', '25', '26'], -1, [], [], 0, lane_ender['S2']],                 # platoon 7
           '7':  [['27'], -1, [], [], 0, lane_ender['S1']],                                   # platoon 8
           '8':  [['28', '29', '30'], -1, [], [], 0, lane_ender['N1']],                       # platoon 9
           '9':  [['31', '32', '33'], -1, [], [], 0, lane_ender['W2']],                       # platoon 10
           '10': [['34', '35', '36', '37'], -1, [], [], 0, lane_ender['N0']],                 # platoon 11
           '11': [['38', '39', '40', '41', '42', '43'], -1, [], [], 0, lane_ender['E0']],     # platoon 12
           '12': [['44', '45', '46', '47', '48'], -1, [], [], 0, lane_ender['S0']],           # platoon 13
           '13': [['49', '50', '51', '52'], -1, [], [], 0, lane_ender['W0']],                 # platoon 14
           '14': [['53', '54', '55', '56', '57'], -1, [], [], 0, lane_ender['W2']],           # platoon 15
           '15': [['58', '59', '60', '61', '62', '63'], -1, [], [], 0, lane_ender['E0']],     # platoon 16
           '16': [['64', '65', '66', '67', '68', '69'], -1, [], [], 0, lane_ender['E1']],     # platoon 17
           '17': [['70', '71', '72'], -1, [], [], 0, lane_ender['N1']],                       # platoon 18
           '18': [['73', '74', '75', '76', '77'], -1, [], [], 0, lane_ender['S1']],           # platoon 19
           '19': [['78', '79'], -1, [], [], 0, lane_ender['S2']],                             # platoon 20
           '20': [['80', '81', '82', '83'], -1, [], [], 0, lane_ender['W0']],                 # platoon 21
           '21': [['84', '85', '86'], -1, [], [], 0, lane_ender['S0']],                       # platoon 22
           '22': [['87', '88', '89', '90'], -1, [], [], 0, lane_ender['N0']],                 # platoon 23
           '23': [['91', '92', '93', '94'], -1, [], [], 0, lane_ender['E1']],                 # platoon 24
           '24': [['95', '96', '97', '98'], -1, [], [], 0, lane_ender['E0']],                 # platoon 25
           '25': [['99', '100', '101', '102', '103', '104'], -1, [], [], 0, lane_ender['N2']],# platoon 26
           '26': [['105', '106', '107', '108'], -1, [], [], 0, lane_ender['S2']],             # platoon 27
           '27': [['109', '110', '111', '112', '113'], -1, [], [], 0, lane_ender['W1']],      # platoon 28
           '28': [['114', '115', '116', '117'], -1, [], [], 0, lane_ender['E0']],             # platoon 29
           '29': [['118', '119', '120', '121', '122'], -1, [], [], 0, lane_ender['N2']],      # platoon 30                       # platoon 31
}


""" 
    platoon flag [is_in_cz_flag, lvp_leader_member_check_flag, pass_conflict_already_flag, ego_pre_same_lane_flag] 
        is_in_cz_flag                   - 判断车辆排是否还在 CZ 区域内，当领队车辆进入 CZ 区域或者队尾车辆还没有离开 CZ 区域时，都算该车辆排在 CZ 区域内
        lvp_leader_member_check_flag    - 判断该车辆排是否进行过 LVP Leader 以及 LVP Member 的初始化
        pass_conflict_already_flag      - 判断该车辆排是否通过冲突点，只有 LVP Member 的这项内容会不同
        ego_pre_same_lane_flag          - 判断前后驱是否是同一车道的车辆排
"""
platoon_flag = {'0':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '1':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '2':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '3':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '4':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '5':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '6':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '7':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '8':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '9':  [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '10': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '11': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '12': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '13': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '14': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '15': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '16': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '17': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '18': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '19': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '20': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '21': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '22': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '23': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '24': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '25': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '26': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '27': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '28': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '29': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],
                '30': [enum_pf.in_flag.OUT, enum_pf.l_m_check_flag.NOT_YET, enum_pf.pass_conflict_already_flag.NOT_YET, enum_pf.ego_pre_same_lane_flag.DIFFERENT],}

# 交叉口的 crossing 所有冲突点（总共64个）
junction_point = {'ES0_NS0': [-8, 8],      'ES0_NS1': [-4.8, 8],    'ES0_NS2': [-1.6, 8],    'ES0_NL2': [-0.8, 8],     'ES0_WL2': [0.8, 8],     'ES0_SS2': [1.6, 8],    'ES0_SS1': [4.8, 8],    'ES0_SS0': [8, 8],
                  'ES1_NS0': [-8, 4.8],    'ES1_NS1': [-4.8, 4.8],  'ES1_NS2': [-1.6, 4.8],  'ES1_NL2': [-0.65, 4.8],  'ES1_WL2': [0.65, 4.8],  'ES1_SS2': [1.6, 4.8],  'ES1_SS1': [4.8, 4.8],  'ES1_SS0': [8, 4.8],
                  'ES2_NS0': [-8, 1.6],    'ES2_NS1': [-4.8, 1.6],  'ES2_WL2': [-3.2, 1.6],  'ES2_NS2': [-1.6, 1.6],   'ES2_SS2': [1.6, 1.6],   'ES2_NL2': [3.2, 1.6],  'ES2_SS1': [4.8, 1.6],  'ES2_SS0': [8, 1.6],
                  'WS2_NS0': [-8, -1.6],   'WS2_NS1': [-4.8, -1.6], 'WS2_SL2': [-3.2, -1.6], 'WS2_NS2': [-1.6, -1.6],  'WS2_SS2': [1.6, -1.6],  'WS2_EL2': [3.2, -1.6], 'WS2_SS1': [4.8, -1.6], 'WS2_SS0': [8, -1.6],
                  'WS1_NS0': [-8, -4.8],   'WS1_NS1': [-4.8, -4.8], 'WS1_NS2': [-1.6, -4.8], 'WS1_SL2': [-0.65, -4.8], 'WS1_EL2': [0.65, -4.8], 'WS1_SS2': [1.6, -4.8], 'WS1_SS1': [4.8, -4.8], 'WS1_SS0': [8, -4.8],
                  'WS0_NS0': [-8, -8],     'WS0_NS1': [-4.8, -8],   'WS0_NS2': [-1.6, -8],   'WS0_EL2': [-0.8, -8],    'WS0_SL2': [0.8, -8],    'WS0_SS2': [1.6, -8],   'WS0_SS1': [4.8, -8],   'WS0_SS0': [8, -8],
                  'WL2_NL2': [0, 6],
                  'WL2_NS2': [-1.6, 3.2],  'NL2_SS2': [1.6, 3.2],
                  'SL2_NS1': [-8, 0.8],    'WL2_NS1': [-4.8, 0.6],   'NL2_SS1': [4.8, 0.6],  'EL2_SS0': [8, 0.8],
                  'WL2_SL2': [-6, 0],      'NL2_EL2': [6, 0],
                  'EL2_NS1': [-8, -0.8],   'SL2_NS1': [-4.8, -0.6],  'EL2_SS1': [4.8, -0.6], 'NL2_SS1': [8, -0.8],
                  'SL2_NS2': [-1.6, -3.2], 'EL2_SS2': [1.6, -3.2],
                  'SL2_EL2': [0, -6],
                  'ES0_NR0': [-13.6, 8], 'ES2_SL2': [-13.6, 1.6], 'WL2_SS2': [1.6, 13.6], 'ER0_SS0': [8, 13.6], 'NL2_WS2': [13.6, -1.6], 'WS0_SR0': [13.6, -8], 'EL2_NS2': [-1.6, -13.6], 'NS0_WR0': [-8, -13.6]}

distance_to_junction_point = {  'ES0_NS0': [421.6, 405.6], 'ES0_NS1': [418.4, 405.6], 'ES0_NS2': [415.2, 405.6], 'ES0_NL2': [414.4, 405.7],  'ES0_WL2': [412.8, 418.81], 'ES0_SS2': [412, 421.6],   'ES0_SS1': [408.8, 421.6], 'ES0_SS0': [405.6, 421.6],
                                'ES1_NS0': [421.6, 408.8], 'ES1_NS1': [418.4, 408.8], 'ES1_NS2': [415.2, 408.8], 'ES1_NL2': [413, 409.2],    'ES1_WL2': [414.2, 415.31], 'ES1_SS2': [412, 418.4],   'ES1_SS1': [408.8, 418.4], 'ES1_SS0': [405.6, 418.4],
                                'ES2_NS0': [421.6, 412],   'ES2_NS1': [418.4, 412],   'ES2_NS2': [415.2, 412],   'ES2_WL2': [416.8, 411.1],  'ES2_NL2': [410.4, 413.41], 'ES2_SS2': [412, 415.2],   'ES2_SS1': [408.8, 415.2], 'ES2_SS0': [405.6, 415.2],
                                
                                'WS0_NS0': [405.6, 421.6], 'WS0_NS1': [408.8, 421.6], 'WS0_NS2': [412, 415.2],   'WS0_EL2': [412.8, 418.81], 'WS0_SL2': [414.4, 405.7],  'WS0_SS2': [415.2, 405.6], 'WS0_SS1': [418.4, 405.6], 'WS0_SS0': [421.6, 405.6],
                                'WS1_NS0': [405.6, 418.4], 'WS1_NS1': [408.8, 418.4], 'WS1_NS2': [412, 415.2],   'WS1_SL2': [413, 409.2],    'WS1_EL2': [414.2, 415.31], 'WS1_SS2': [415.2, 408.8], 'WS1_SS1': [418.4, 408.8], 'WS1_SS0': [421.6, 408.8],
                                'WS2_NS0': [405.6, 415.2], 'WS2_NS1': [408.8, 415.2], 'WS2_NS2': [412, 415.2],   'WS2_SL2': [410.4, 413.41], 'WS2_EL2': [416.8, 411.1],  'WS2_SS2': [415.2, 412],   'WS2_SS1': [418.4, 412],   'WS2_SS0': [421.6, 412],
                                
                                'WL2_NL2': [408.01, 416.5], 'NL2_SS2': [411.1, 416.8], 'WL2_NS2': [413.41, 410.4], 'EL2_SS2': [413.41, 410.4], 'SL2_NS2': [411.1, 416.8],
                                'WL2_SS2': [424.51, 427.2],  'NL2_WS2': [424.51, 427.2], 'SL2_ES2': [424.51, 427.2], 'EL2_NS2': [424.51, 427.2],
                                
                                'SL2_NS0': [418.81, 412.8],    'WL2_NS1': [409.2, 412.95],   'NL2_SS1': [415.31, 414.25],  'EL2_SS0': [405.7, 412.8],
                                
                                'WL2_SL2': [408, 416.51],      'NL2_EL2': [416.51, 408], 'SL2_EL2': [408, 416.51], 
                                'WL2_NS0': [405.7, 414.4],   'SL2_NS1': [415.31, 414.25],  'EL2_SS1': [609.2, 612.95], 'NL2_SS0': [418.81, 414.4],
                                
                                'ES0_NR0': [427, 409],  'ER0_SS0': [409, 427], '': [424.51, 427], 'WS0_SR0': [427, 409], '': [424.51, 427], 'NS0_WR0': [427, 409]}

# distance_to_junction_point = {  'ES0_NS0': [621.6, 605.6], 'ES0_NS1': [618.4, 605.6], 'ES0_NS2': [615.2, 605.6], 'ES0_NL2': [614.4, 605.7],  'ES0_WL2': [612.8, 618.81], 'ES0_SS2': [612, 621.6],   'ES0_SS1': [608.8, 621.6], 'ES0_SS0': [605.6, 621.6],
#                                 'ES1_NS0': [621.6, 608.8], 'ES1_NS1': [618.4, 608.8], 'ES1_NS2': [615.2, 608.8], 'ES1_NL2': [613, 609.2],    'ES1_WL2': [614.2, 615.31], 'ES1_SS2': [612, 618.4],   'ES1_SS1': [608.8, 618.4], 'ES1_SS0': [605.6, 618.4],
#                                 'ES2_NS0': [621.6, 612],   'ES2_NS1': [618.4, 612],   'ES2_NS2': [615.2, 612],   'ES2_WL2': [616.8, 611.1],  'ES2_NL2': [610.4, 613.41], 'ES2_SS2': [612, 615.2],   'ES2_SS1': [608.8, 615.2], 'ES2_SS0': [605.6, 615.2],
                                
#                                 'WS0_NS0': [605.6, 621.6], 'WS0_NS1': [608.8, 621.6], 'WS0_NS2': [612, 615.2],   'WS0_EL2': [612.8, 618.81], 'WS0_SL2': [614.4, 605.7],  'WS0_SS2': [615.2, 605.6], 'WS0_SS1': [618.4, 605.6], 'WS0_SS0': [621.6, 605.6],
#                                 'WS1_NS0': [605.6, 618.4], 'WS1_NS1': [608.8, 618.4], 'WS1_NS2': [612, 615.2],   'WS1_SL2': [613, 609.2],    'WS1_EL2': [614.2, 615.31], 'WS1_SS2': [615.2, 608.8], 'WS1_SS1': [618.4, 608.8], 'WS1_SS0': [621.6, 608.8],
#                                 'WS2_NS0': [605.6, 615.2], 'WS2_NS1': [608.8, 615.2], 'WS2_NS2': [612, 615.2],   'WS2_SL2': [610.4, 613.41], 'WS2_EL2': [616.8, 611.1],  'WS2_SS2': [615.2, 612],   'WS2_SS1': [618.4, 612],   'WS2_SS0': [621.6, 612],
                                
#                                 'WL2_NL2': [608.01, 616.5], 'NL2_SS2': [611.1, 616.8], 'WL2_NS2': [613.41, 610.4], 'EL2_SS2': [613.41, 610.4], 'SL2_NS2': [611.1, 616.8],
#                                 'WL2_SS2': [624.51, 627.2],  'NL2_WS2': [624.51, 627.2], 'SL2_ES2': [624.51, 627.2], 'EL2_NS2': [624.51, 627.2],
                                
#                                 'SL2_NS0': [618.81, 612.8],    'WL2_NS1': [609.2, 612.95],   'NL2_SS1': [615.31, 614.25],  'EL2_SS0': [605.7, 612.8],
                                
#                                 'WL2_SL2': [608, 616.51],      'NL2_EL2': [616.51, 608], 'SL2_EL2': [608, 616.51], 
#                                 'WL2_NS0': [605.7, 614.4],   'SL2_NS1': [615.31, 614.25],  'EL2_SS1': [609.2, 612.95], 'NL2_SS0': [618.81, 614.4],
                                
#                                 'ES0_NR0': [627, 609], '': [], '': [624.51, 627], 'ER0_SS0': [609, 627], '': [624.51, 627], 'WS0_SR0': [627, 609], '': [624.51, 627], 'NS0_WR0': [627, 609]}

# platoon_depart_pos = {  '0' : [70, 56, 42, 25, 10],
#                         '1' : [39, 25, 10],
#                         '2' : [27, 10],
#                         '3' : [70, 56, 39, 24, 10],
#                         '4' : [70, 56, 42, 27, 10],
#                         '5' : [42, 27, 10],
#                         '6' : [58, 41, 27, 10],
#                         '7' : [10],
#                         '8' : [38, 24, 10],
#                         '9' : [41, 24, 10],
#                         '10': [55, 41, 27, 10],
#                         '11': [88, 74, 57, 39, 24, 10],
#                         '12': [74, 57, 40, 25, 10],
#                         '13': [56, 41, 24, 10],
#                         '14': [69, 54, 39, 25, 10],
#                         '15': [84, 70, 53, 38, 24, 10],
#                         '16': [90, 75, 58, 41, 27, 10],
#                         '17': [39, 24, 10],
#                         '18': [70, 56, 41, 24, 10],
#                         '19': [24, 10],
#                         '20': [58, 44, 27, 10],
#                         '21': [41, 27, 10],
#                         '22': [56, 39, 24, 10],
#                         '23': [54, 40, 25, 10],
#                         '24': [53, 38, 24, 10],
#                         '25': [85, 71, 56, 39, 25, 10],
#                         '26': [56, 41, 27, 10],
#                         '27': [72, 55, 40, 25, 10],
#                         '28': [57, 42, 25, 10],
#                         '29': [71, 54, 39, 25, 10],}

platoon_depart_pos = {  '0' : [70, 56, 42, 25, 10],
                        '1' : [70, 56, 41],
                        '2' : [67, 50],
                        '3' : [70, 56, 39, 24, 10],
                        '4' : [70, 56, 42, 27, 10],
                        '5' : [70, 55, 38],
                        '6' : [53, 36, 22, 5],
                        '7' : [65],
                        '8' : [65, 51, 37],
                        '9' : [59, 42, 28],
                        '10': [70, 56, 42, 25],
                        '11': [88, 74, 57, 39, 24, 10],
                        '12': [70, 53, 36, 21, 6],}

# 记录的是该车辆排路径起始点到某个冲突点的距离，[ego_pla, pre_pla]
platoon_ego_pre_position_info = {   '0' : [-1, -1],
                                    '1' : [-1, -1],
                                    '2' : [-1, -1],
                                    '3' : [-1, -1],
                                    '4' : [-1, -1],
                                    '5' : [-1, -1],
                                    '6' : [-1, -1],
                                    '7' : [-1, -1],
                                    '8' : [-1, -1],
                                    '9' : [-1, -1],
                                    '10': [-1, -1],
                                    '11': [-1, -1],
                                    '12': [-1, -1],
                                    '13': [-1, -1],
                                    '14': [-1, -1],
                                    '15': [-1, -1],
                                    '16': [-1, -1],
                                    '17': [-1, -1],
                                    '18': [-1, -1],
                                    '19': [-1, -1],
                                    '20': [-1, -1],
                                    '21': [-1, -1],
                                    '22': [-1, -1],
                                    '23': [-1, -1],
                                    '24': [-1, -1],
                                    '25': [-1, -1],
                                    '26': [-1, -1],
                                    '27': [-1, -1],
                                    '28': [-1, -1],
                                    '29': [-1, -1],
                                    '30': [-1, -1],
                                    '31': [-1, -1],}

platoon_transmit_state = {  '0' : [],
                            '1' : [],
                            '2' : [],
                            '3' : [],
                            '4' : [],
                            '5' : [],
                            '6' : [],
                            '7' : [],
                            '8' : [],
                            '9' : [],
                            '10': [],
                            '11': [],
                            '12': [],
                            '13': [],
                            '14': [],
                            '15': [],
                            '16': [],
                            '17': [],
                            '18': [],
                            '19': [],
                            '20': [],
                            '21': [],
                            '22': [],
                            '23': [],
                            '24': [],
                            '25': [],
                            '26': [],
                            '27': [],
                            '28': [],
                            '29': [],
                            '30': [],}

# 用来存储每个车辆排进入 CZ 区域的时候，所有前驱排的位置
platoon_to_origin_forward = {'0' : [],
                             '1' : [],
                             '2' : [],
                             '3' : [],
                             '4' : [],
                             '5' : [],
                             '6' : [],
                             '7' : [],
                             '8' : [],
                             '9' : [],
                             '10': [],
                             '11': [],
                             '12': [],
                             '13': [],
                             '14': [],
                             '15': [],
                             '16': [],
                             '17': [],
                             '18': [],
                             '19': [],
                             '20': [],
                             '21': [],
                             '22': [],
                             '23': [],
                             '24': [],
                             '25': [],
                             '26': [],
                             '27': [],
                             '28': [],
                             '29': [],
                             '30': [],
                             '31': [],
                             '32': [],
                             '33': [],
                             '34': [],}
                                            