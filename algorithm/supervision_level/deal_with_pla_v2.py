'''
    算法版本2：
        通过交叉口中心点映射后得到大致的进入交叉口中心区域的顺序，接着以该中心点为基准判断车辆排的驾驶模式，得到初始间距，并以此为基准
        分配驾驶方式，后续也以此为基准进行前后虚拟间距的计算
        由于此算法以交叉口中心点为基准进行驾驶模式的分配，多车道使得交叉口范围变大，会产生额外的间距误差，因此间距阈值需要设置得大一点
    （不太可行）
'''

import sys
import math

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

# 导入自定义模块
from utils.common_stuff import platoon, platoon_flag, junction_point, space_threshold, desire_velocity, platoon_transmit_state, platoon_depart_pos
import enums.platoon_flag as enum_pf
import algorithm.execution_level.optimize_solver_v1 as solver_v1

"""
    计算当前车辆到某一点的距离，默认的点为 [0, 0]

    Parameters:
        traci           - traci 接口
        vehicle         - 当前车辆 ID
        origin          - 目标点的坐标，默认为 [0, 0]
"""
def get_origin_distance(traci, vehicle, origin = [0, 0]):
    origin_x, origin_y = origin
    x, y = traci.vehicle.getPosition(vehicle)
    origin_distance = math.sqrt(math.pow(round(x, 2) - origin_x, 2) + math.pow(round(y, 2) - origin_y, 2))
    return round(origin_distance, 2)

"""
    根据行驶方向构建新的原点

    Parameters:
        ego_pla_route   - 当前车辆排的行驶方向
        pre_pla_route   - 前驱车辆排的的行驶方向
"""
def generate_origin(ego_pla_route, pre_pla_route):
    return junction_point[ego_pla_route + '_' + pre_pla_route] if (ego_pla_route + '_' + pre_pla_route) in junction_point else junction_point[pre_pla_route + '_' + ego_pla_route]

"""
    计算两个点之间的距离

    Parameters:
        beg_point       - 当前车辆排的行驶方向
        pre_pla_route   - 前驱车辆排的的行驶方向
"""
def point_to_point_distance(beg_point, end_point):
    beg_point_x, beg_point_y = beg_point
    end_point_x, end_point_y = end_point
    return round(math.sqrt(math.pow(beg_point_x - end_point_x, 2) + math.pow(beg_point_y - end_point_y, 2)), 2)

"""
    每个车辆排求解的主要函数。

    Parameters:
        traci           - traci 接口
        all_vehicle_id  - 交叉口所有车辆的 ID
        ego_pla         - 当前车辆排的 ID
        pre_pla         - 前驱车辆排的 ID
        step            - 当前步骤
"""
def main_solver(traci, all_vehicle_id, ego_pla, pre_pla, step):
    if platoon[ego_pla][0][0] in all_vehicle_id:
        # 为当前车辆排的每个车辆创建列表，[vehicle_id, virtual_position, vehicle_velocity, vehicle_length]
        ego_pla_state = []
        pla_leader = platoon[ego_pla][0][0]
        pla_ender = platoon[ego_pla][0][-1]
        edge_beg, edge_end = traci.vehicle.getRoute(pla_leader)
        ego_pla_route = traci.vehicle.getRouteID(pla_leader)
        ego_pla_leader_edge = traci.vehicle.getRoadID(pla_leader)
        ego_pla_ender_edge = traci.vehicle.getRoadID(pla_ender)  
        if platoon[ego_pla][5] == -1:
            platoon[ego_pla][5] = traci.lane.getShape(traci.vehicle.getLaneID(pla_leader))[1]
        if (ego_pla_leader_edge == edge_beg and get_origin_distance(traci, pla_leader, traci.lane.getShape(traci.vehicle.getLaneID(pla_leader))[1]) > 236.4) or (ego_pla_ender_edge == edge_end and get_origin_distance(traci, pla_ender, traci.lane.getShape(traci.vehicle.getLaneID(pla_ender))[0]) > 236.4):
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
                if pre_pla != -1:
                    # 如果初始传入判断的前驱排就为 -1，直接跳过进入下一步
                    # 判断间距差值和阈值的关系，从而进行 LVP Leader 和 Member 两种驾驶模式的分配，根据交叉口的中心点，从而判断分配哪一种驾驶模式
                    ego_pla_distance = get_origin_distance(traci, pla_leader, platoon[ego_pla][5])
                    pre_pla_distance = [get_origin_distance(traci, platoon[pre_pla][0][0], traci.lane.getShape(traci.vehicle.getLaneID(platoon[pre_pla][0][0]))[1]), get_origin_distance(traci, platoon[pre_pla][0][-1], traci.lane.getShape(traci.vehicle.getLaneID(platoon[pre_pla][0][-1]))[1])]
                    if (pre_pla_distance[0] <= ego_pla_distance <= pre_pla_distance[1]) or (ego_pla_distance <= pre_pla_distance[1] + space_threshold):
                        platoon[ego_pla][1] = pre_pla
            print('该车辆排为 %s' % platoon[ego_pla][1])
            if platoon[ego_pla][1] == -1:
                # 如果该车辆排是 LVP Leader，传的位置用已经行驶的距离来表示
                for index, vehicle in enumerate(platoon[ego_pla][0]):
                    ego_pla_state.append([vehicle, platoon_depart_pos[ego_pla][index] + round(traci.vehicle.getDistance(vehicle), 2), round(traci.vehicle.getSpeed(vehicle), 2), round(traci.vehicle.getLength(vehicle), 2)])
            else:
                # 如果该车辆排是 LVP Member，传的位置应该是以冲突点为中心点进行映射的距离差值
                conflict_origin = generate_origin(ego_pla_route, traci.vehicle.getRouteID(platoon[pre_pla][0][0]))
                for vehicle in platoon[ego_pla][0]:
                    # 根据是否通过冲突点来判断传入的参数的正负性
                    ego_pla_position = get_origin_distance(traci, vehicle, conflict_origin)
                    ego_pla_each_edge = traci.vehicle.getRoadID(vehicle)
                    if ego_pla_each_edge == edge_beg:
                        ego_pla_position *= -1
                    elif ego_pla_each_edge != edge_end:
                        edge_conflic_origin_distance = point_to_point_distance(traci.lane.getShape(traci.vehicle.getLaneID(pla_leader))[1], conflict_origin)
                        if get_origin_distance(traci, vehicle, platoon[ego_pla][5]) <= edge_conflic_origin_distance:
                            ego_pla_position *= -1
                    ego_pla_state.append([vehicle, ego_pla_position, round(traci.vehicle.getSpeed(vehicle), 2), round(traci.vehicle.getLength(vehicle), 2)])
                # 如果是 LVP Member 的话，还要用新的冲突点构建的坐标系再预测以此，这样才能传递正确的前驱状态变量
                
            print("---------------------------------- platoon %s optimize begin at step %d ----------------------------------" % (ego_pla, step))
            platoon[ego_pla][2], platoon[ego_pla][4] = solver_v1.main_solver(ego_pla, ego_pla_state, platoon_transmit_state[pre_pla][0], desire_velocity) if platoon[ego_pla][1] != -1 and platoon_flag[ego_pla][0] == enum_pf.in_flag.IN else solver_v1.main_solver(ego_pla, ego_pla_state, -1, desire_velocity)
            for index, vehicle in enumerate(platoon[ego_pla][0]):
                # 该版本 traci 的 setAcceleration 有问题，所以这里先不用加速度来对车辆进行控制
                # Changes the acceleration to the given value for the given amount of time in seconds (must be greater than zero).
                # traci.vehicle.setAcceleration(i, optimizeControlInput[0], 1)
                print("speed is ", traci.vehicle.getSpeed(vehicle))
                print("platoon %s vehicle %s slow down at step %s" % (ego_pla, index, step)) if platoon[ego_pla][2][index] < 0 else print("platoon %s vehicle %s speed up at step %s" % (ego_pla, index, step))
                traci.vehicle.setSpeed(vehicle, traci.vehicle.getSpeed(vehicle) + platoon[ego_pla][2][index])
            print("---------------------------------- platoon %s optimize end at step %d ----------------------------------" % (ego_pla, step))
            print("---------------------------------- platoon %s control end at step %d ----------------------------------" % (ego_pla, step)) 