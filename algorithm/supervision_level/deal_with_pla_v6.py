'''
    算法版本6：
        高流量算法
'''

import sys
import math
import time

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

# 导入自定义模块
from utils.common_stuff import platoon, platoon_flag, space_threshold, desire_velocity, desire_space
from utils.common_stuff import platoon_transmit_state, platoon_depart_pos, distance_to_junction_point
from utils.common_stuff import platoon_to_origin_forward, platoon_ego_pre_position_info
from algorithm.execution_level.optimize_solver_v2 import main_solver as solver_v2
import enums.platoon_flag as enum_pf
import utils.plot_state as plt

"""
    计算当前车辆到某一点的距离，默认的点为 [0, 0]

    Parameters:
        traci           - traci 接口
        vehicle         - 当前车辆 ID
        origin          - 目标点的坐标，默认为 [0, 0]
    
    Return:
        None
"""
def get_origin_distance(traci, vehicle, origin = [0, 0]):
    origin_x, origin_y = origin
    x, y = traci.vehicle.getPosition(vehicle)
    origin_distance = math.sqrt(math.pow(round(x, 2) - origin_x, 2) + math.pow(round(y, 2) - origin_y, 2))
    return round(origin_distance, 2)

"""
    根据路由 ID 获取前后车辆排到对应冲突点的初始距离

    Parameters:
        ego_pla         - 当前车辆排 ID
        ego_pla_route   - 当前车辆排的行驶方向
        pre_pla_route   - 前驱车辆排的的行驶方向
        type            - 表示是需要计算不同冲突点之间的距离（还未确定前驱排）还是需要存储某个确定冲突点的距离（确定前驱排）

    Return:
        list            - [ego_pla_distance, pre_pla_distance]
        None            - 当不存在冲突点时，返回 None
"""
def get_ego_pre_distance_to_conflict_point(ego_pla, ego_pla_route, pre_pla_route, type = -1):
    if (ego_pla_route + '_' + pre_pla_route) in distance_to_junction_point:
        if type == -1:
            platoon_ego_pre_position_info[ego_pla][0], platoon_ego_pre_position_info[ego_pla][1] = distance_to_junction_point[ego_pla_route + '_' + pre_pla_route]
        else:
            return distance_to_junction_point[ego_pla_route + '_' + pre_pla_route]
    elif (pre_pla_route + '_' + ego_pla_route) in distance_to_junction_point:
        if type == -1:
            platoon_ego_pre_position_info[ego_pla][0] = distance_to_junction_point[pre_pla_route + '_' + ego_pla_route][1]
            platoon_ego_pre_position_info[ego_pla][1] = distance_to_junction_point[pre_pla_route + '_' + ego_pla_route][0]
        else:
            return [distance_to_junction_point[pre_pla_route + '_' + ego_pla_route][1], distance_to_junction_point[pre_pla_route + '_' + ego_pla_route][0]]
    else:
        return None

"""
    计算当前状态车辆排到给定冲突点的距离
    Parameters:
        traci               - 当前车辆排的行驶方向
        ego_pla             - 当前车辆排 ID
        initial_distance    - 车辆排到给定冲突点的初始距离
    Return:
        None
"""
def get_current_distance_to_conflict_point(traci, initial_distance, ego_pla, vehicle, veh_index):
    driving_distance = traci.vehicle.getDistance(vehicle) + platoon_depart_pos[ego_pla][veh_index]
    return initial_distance - driving_distance

"""
    计算两个点之间的距离

    Parameters:
        beg_point       - 当前车辆排的行驶方向
        pre_pla_route   - 前驱车辆排的的行驶方向

    Return:
        None
"""
def point_to_point_distance(beg_point, end_point):
    beg_point_x, beg_point_y = beg_point
    end_point_x, end_point_y = end_point
    return round(math.sqrt(math.pow(beg_point_x - end_point_x, 2) + math.pow(beg_point_y - end_point_y, 2)), 2)
    

"""
    计算前面所有车辆排到交叉口的距离，以及到冲突点的距离

    Parameters:
        traci     - traci 接口
        ego_pla   - 当前车辆排 ID
        
    Return:
        None
"""
def update_platoon_to_origin_forward(traci, ego_pla, ego_pla_route, all_vehicle_id, ego_distance):
    for item in platoon:
        # 若当前车辆排和目标车辆排相同，跳过
        if item == ego_pla: 
            continue
        leader = platoon[item][0][0]
        # 若当前车辆排的车辆不在场景中，跳过
        if leader not in all_vehicle_id:
            continue
        ender = platoon[item][0][-1] 
        edge_ender_x, edge_ender_y = platoon[item][5]
        item_route = traci.vehicle.getRouteID(leader)
        leader_origin = traci.vehicle.getDrivingDistance2D(leader, edge_ender_x, edge_ender_y)
        # 若当前距离更小，即比目标车辆排更晚到达交叉口，则跳过
        if ego_distance < leader_origin:
            continue
        ender_origin = traci.vehicle.getDrivingDistance2D(ender, edge_ender_x, edge_ender_y)
        ego_pre_conflict_distance = get_ego_pre_distance_to_conflict_point(ego_pla, ego_pla_route, item_route, 'call')
        if ego_pre_conflict_distance:
            ego_to_conflict = get_current_distance_to_conflict_point(traci, ego_pre_conflict_distance[0], ego_pla, platoon[ego_pla][0][0], 0)
            item_to_conflict = get_current_distance_to_conflict_point(traci, ego_pre_conflict_distance[1], item, platoon[item][0][0], 0)
            # 前驱领队到道路尽头的距离，前驱末尾到道路尽头的距离，当前车辆排到生成的冲突点的距离，前驱车辆排到生成的冲突点的距离
            platoon_to_origin_forward[ego_pla].append([item, ego_distance, leader_origin if leader_origin > 0 else -1, ender_origin if ender_origin else -1, ego_to_conflict, item_to_conflict])
    print('当前车辆排为 %s ，前面的所有车辆排的位置如下： %s ' % (ego_pla, platoon_to_origin_forward[ego_pla]))
   
'''
    更新当前的间距误差
    Parameters:
        traci           - traci 接口
        all_vehicle_id  - 交叉口所有车辆的 ID
        ego_pla         - 当前车辆排的 ID
        pre_pla         - 前驱车辆排的 ID
        step            - 当前步骤
    Return
        None
'''
def update_current_spacing_error(traci, ego_pla, pre_pla, step):
    ego_conflict = get_current_distance_to_conflict_point(traci, platoon_ego_pre_position_info[ego_pla][0], ego_pla, platoon[ego_pla][0][0], 0)
    pre_conflict = get_current_distance_to_conflict_point(traci, platoon_ego_pre_position_info[ego_pla][1], pre_pla, platoon[pre_pla][0][-1], -1)
    spacing_error = pre_conflict - ego_conflict + desire_space + traci.vehicle.getLength(platoon[pre_pla][0][-1])
    plt.udpate_spacing_error(ego_pla, spacing_error, step)

"""
    每个车辆排求解的主要函数。

    Parameters:
        traci           - traci 接口
        all_vehicle_id  - 交叉口所有车辆的 ID
        ego_pla         - 当前车辆排的 ID
        pre_pla         - 前驱车辆排的 ID
        step            - 当前步骤
    
    Return
        None
"""
def main_solver(traci, all_vehicle_id, ego_pla, pre_pla, step):
    if platoon[ego_pla][0][0] in all_vehicle_id:
        ego_pla_state = []
        pla_leader = platoon[ego_pla][0][0]
        pla_ender = platoon[ego_pla][0][-1]
        ego_pla_route = traci.vehicle.getRouteID(pla_leader)
        edge_beg, edge_end = traci.vehicle.getRoute(pla_leader)
        ego_pla_leader_edge = traci.vehicle.getRoadID(pla_leader)
        ego_pla_ender_edge = traci.vehicle.getRoadID(pla_ender)  
        if (ego_pla_leader_edge == edge_beg and get_origin_distance(traci, pla_leader, traci.lane.getShape(traci.vehicle.getLaneID(pla_leader))[1]) > 336.4) or (ego_pla_ender_edge == edge_end and get_origin_distance(traci, pla_ender, traci.lane.getShape(traci.vehicle.getLaneID(pla_ender))[0]) > 336.4):
            # 当车辆在交叉口控制范围之外时，控制车辆按照 12 的速度行驶
            platoon_flag[ego_pla][0] = enum_pf.in_flag.OUT
            for vehicle in platoon[ego_pla][0]:
                traci.vehicle.setSpeed(vehicle, 12)
        else:
            # 当车辆排的头部车辆进入 CZ 区域，或者尾部车辆还在 CZ 区域，用提出的算法进行控制，这里的 CZ 区域设置为 250m
            platoon_flag[ego_pla][0] = enum_pf.in_flag.IN
            print("---------------------------------- platoon %s control begin at step %d ----------------------------------" % (ego_pla, step))
            # 首先根据分配的前驱排判断驾驶模式，分别为 LVP Member 以及 LVP Leader，若 platoon[ego_pla][1] 为 -1 则为 LVP Leader， 若不为 -1 则是 LVP Member
            if platoon_flag[ego_pla][1] == enum_pf.l_m_check_flag.NOT_YET:
                # 修改判断 LVP Leader 和 Member 是否分配的标志位
                platoon_flag[ego_pla][1] = enum_pf.l_m_check_flag.CHECKED
                # 计算每个车辆排到交叉口中心以及各自冲突点的距离
                update_platoon_to_origin_forward(traci, ego_pla, ego_pla_route, all_vehicle_id, traci.vehicle.getDrivingDistance2D(pla_leader, platoon[ego_pla][5][0], platoon[ego_pla][5][1]))
                if pre_pla != -1:
                    # 如果初始传入判断的前驱排就为 -1，直接跳过进入下一步
                    # 判断间距差值和阈值的关系，从而进行 LVP Leader 和 Member 两种驾驶模式的分配，根据交叉口的中心点，从而判断分配哪一种驾驶模式
                    ego_pla_distance = get_origin_distance(traci, pla_leader, platoon[ego_pla][5])
                    pre_pla_distance = [get_origin_distance(traci, platoon[pre_pla][0][0], traci.lane.getShape(traci.vehicle.getLaneID(platoon[pre_pla][0][0]))[1]), get_origin_distance(traci, platoon[pre_pla][0][-1], traci.lane.getShape(traci.vehicle.getLaneID(platoon[pre_pla][0][-1]))[1])]
                    if (pre_pla_distance[0] <= ego_pla_distance <= pre_pla_distance[1]) or (ego_pla_distance <= pre_pla_distance[1] + space_threshold):
                        platoon[ego_pla][1] = pre_pla
            # 进入 CZ 控制
            if platoon[ego_pla][1] != -1:
                if platoon_ego_pre_position_info[ego_pla][0] == -1 or platoon_ego_pre_position_info[ego_pla][1] == -1:
                    if ego_pla_route == traci.vehicle.getRouteID(platoon[pre_pla][0][0]):
                        # 方向路径完全相同，这种情况一直维持 LVP Member 即可，不用计算到达冲突点的距离
                        platoon_flag[ego_pla][3] = enum_pf.ego_pre_same_lane_flag.SAME
                        platoon_ego_pre_position_info[ego_pla] = [0, 0]
                    elif edge_beg == traci.vehicle.getRoute(platoon[pre_pla][0][0])[0] and edge_end != traci.vehicle.getRoute(platoon[pre_pla][0][0])[1]:
                        # 只有车道相同，路由不同，当前驱排的最后一辆车离开车道时，后驱排转为 LVP Leader
                        platoon_flag[ego_pla][3] = enum_pf.ego_pre_same_lane_flag.HALF_SAME
                        platoon_ego_pre_position_info[ego_pla] = [0, 0]
                    else:
                        # 如果车辆路径完全不同，计算前后驱车辆到冲突点的初始距离
                        get_ego_pre_distance_to_conflict_point(ego_pla, ego_pla_route, traci.vehicle.getRouteID(platoon[pre_pla][0][0]))
                if platoon_flag[ego_pla][2] == enum_pf.pass_conflict_already_flag.NOT_YET:
                    # 只要模式没有转变为 leader，就进行判断
                    if platoon_flag[ego_pla][3] == enum_pf.ego_pre_same_lane_flag.DIFFERENT:
                        # Different: 路径不同且初始车道不同
                        ego_distance = get_current_distance_to_conflict_point(traci, platoon_ego_pre_position_info[ego_pla][0], ego_pla, platoon[ego_pla][0][0], 0)
                        if ego_distance < 0:
                            # 当车辆排到达冲突点之后，就可以改为 LVP Leader 行驶，如果不存在冲突点，即前驱车辆排就在当前道路上，则一直保持 LVP Member 行驶
                            platoon_flag[ego_pla][2] = enum_pf.pass_conflict_already_flag.PASSING
                        else:
                            update_current_spacing_error(traci, ego_pla, platoon[ego_pla][1], step)
                    elif platoon_flag[ego_pla][3] == enum_pf.ego_pre_same_lane_flag.HALF_SAME:
                        # Half_same: 路径只有一半相同，即初始相同，离开车道后不同
                        pre_driving = traci.vehicle.getDistance(platoon[pre_pla][0][-1]) + platoon_depart_pos[pre_pla][-1] 
                        if pre_driving > 600:
                            platoon_flag[ego_pla][2] = enum_pf.pass_conflict_already_flag.PASSING
                        else:
                            update_current_spacing_error(traci, ego_pla, platoon[ego_pla][1], step)
                    else:
                        # Same
                        update_current_spacing_error(traci, ego_pla, platoon[ego_pla][1], step)
            # 不管是 LVP Leader 还是 LVP Member 传递的位置信息都是行驶的距离加上出现的位置
            for index, vehicle in enumerate(platoon[ego_pla][0]):
                ego_pla_state.append([vehicle, platoon_depart_pos[ego_pla][index] + round(traci.vehicle.getDistance(vehicle), 2), round(traci.vehicle.getSpeed(vehicle), 2), round(traci.vehicle.getLength(vehicle), 2)])
            print('当前车辆排的状态是 %s' % ego_pla_state)
            print("---------------------------------- platoon %s optimize begin at step %d ----------------------------------" % (ego_pla, step))
            start_time = time.time()
            platoon[ego_pla][2] = solver_v2(ego_pla, ego_pla_state, desire_velocity, platoon_transmit_state[pre_pla][0], platoon_ego_pre_position_info[ego_pla], platoon[ego_pla][3]) if platoon[ego_pla][1] != -1 and platoon_flag[ego_pla][0] == enum_pf.in_flag.IN and platoon_flag[ego_pla][2] == enum_pf.pass_conflict_already_flag.NOT_YET else solver_v2(ego_pla, ego_pla_state, desire_velocity)
            end_time = time.time()
            plt.update_solve_time(ego_pla, round(end_time - start_time, 2), step)
            for index, vehicle in enumerate(platoon[ego_pla][0]):
                # 该版本 traci 的 setAcceleration 有问题，所以这里先不用加速度来对车辆进行控制
                # Changes the acceleration to the given value for the given amount of time in seconds (must be greater than zero).
                # traci.vehicle.setAcceleration(i, optimizeControlInput[0], 1)
                print("platoon %s vehicle %s's speed is %s" % (ego_pla, index, traci.vehicle.getSpeed(vehicle)))
                print("platoon %s vehicle %s slow down at step %s" % (ego_pla, index, step)) if platoon[ego_pla][2][index] < 0 else print("platoon %s vehicle %s speed up at step %s" % (ego_pla, index, step))
                traci.vehicle.setSpeed(vehicle, traci.vehicle.getSpeed(vehicle) + platoon[ego_pla][2][index])
            print("---------------------------------- platoon %s optimize end at step %d ----------------------------------" % (ego_pla, step))
            print("---------------------------------- platoon %s control end at step %d ----------------------------------" % (ego_pla, step)) 