
import gurobipy as gurobi
import math
import sys

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

from utils.common_stuff import delta, u_max, u_min, v_max, v_min, p_max, p_min, desire_space, desired_space_inside
from utils.common_stuff import predictive_horizon, position_weight, velocity_weight, control_input_weight, platoon_transmit_state

'''
    GUROBI 模型初始化
    
    Parameters:
        None
    Return:
        model - GUROBI 模型
'''
def gurobi_init():
    # 针对提出的交叉口创建 gurobi 模型
    model = gurobi.Model("optimal_control_input_solver")
    # 定义 gurobi 处理非凸二次规划的策略
    model.Params.NonConvex = 2
    return model

"""
    计算间距误差。

    Parameters:
        position                            - 预测的未来预测空间内的位置
        ego_pre_distance_to_conflict_point  - 当前车辆排以及前驱车辆排到当前冲突点的初始距离（道路起始点到冲突点的距离）
        pre_pla_state                       - 前驱车辆排的状态
"""     
def deal_with_spacing_error(position, pre_pla_state, ego_pre_distance_to_conflict_point):
    # 看一下间距误差
    if pre_pla_state != -1:
        print('当前前驱车辆排的状态是 %s' % pre_pla_state)
        for step in range(predictive_horizon):
            ego_position = round(position[0, step].X, 2)
            ego_distance = ego_position - ego_pre_distance_to_conflict_point[0]
            pre_distance = pre_pla_state[step][0] - ego_pre_distance_to_conflict_point[1]
            print([round(ego_position, 2), round(pre_pla_state[step][0], 2) , round(ego_distance, 2), round(pre_distance, 2), round(pre_distance - ego_distance + pre_pla_state[step][2] + desire_space, 2)])

"""
    计算当前车辆排下一步骤的预测状态。

    Parameters:
        position            - 预测的未来预测空间内的位置
        last_vehicle_index  - 最后一辆车的下标
        velocity            - 预测的未来预测空间内的速度
        ego_pla_state       - 当前车辆排的状态
    
    Return:
        additional_state    - 返回计算的额外状态
"""        
def deal_with_additional_state(position, velocity, last_vehicle_index, ego_pla_state):
    additional_state = []
    # 额外状态的计算
    # 接收的应该是上一个步骤预测的这个步骤的状态
    # 排除第一个状态，添加一个额外的新状态作为最优状态
    additional_position = round(position[last_vehicle_index, predictive_horizon - 1].X, 2) + round(velocity[last_vehicle_index, predictive_horizon - 1].X, 2) * delta
    additional_velocity = round(velocity[last_vehicle_index, predictive_horizon - 1].X, 2)
    for step in range(1, predictive_horizon):
        additional_state.append([round(position[last_vehicle_index, step].X, 2), round(velocity[last_vehicle_index, step].X, 2), ego_pla_state[-1][3]])
    # put additional state into 
    additional_state.append([additional_position, additional_velocity, ego_pla_state[-1][3]])
    return additional_state

"""
    处理最后一辆车的未来预测水平内的预测状态。

    Parameters:
        ego_pla             - 车辆数量
        position            - 预测的未来预测空间内的位置
        last_vehicle_index  - 最后一辆车的下标
        velocity            - 预测的未来预测空间内的速度
        additional_state    - 额外状态
        ego_pla_state       - 当前车辆排的状态
"""    
def deal_with_predictive_state(ego_pla, position, last_vehicle_index, velocity, additional_state, ego_pla_state):    
    # 首先判断是否存在值，若不存在，初始化传回的状态列表的值，若存在，则更新传回的状态的列表值
    if not len(platoon_transmit_state[ego_pla]):
        # 该车辆排的传回状态存储列表为空，则用当前状态进行初始化，不使用额外状态进行初始化，注意要存两个状态
        predictive_state = []
        for step in range(predictive_horizon):
            predictive_state.append([round(position[last_vehicle_index, step].X, 2), round(velocity[last_vehicle_index, step].X, 2), ego_pla_state[-1][3]])
        platoon_transmit_state[ego_pla].append(predictive_state)
        platoon_transmit_state[ego_pla].append(additional_state)
    else:
        # 该车辆排的传回状态存储列表不为空，首先对换两个状态的位置，接着后一个位置的状态用当前预测的下一步状态替代
        platoon_transmit_state[ego_pla][0] = platoon_transmit_state[ego_pla][1]
        platoon_transmit_state[ego_pla][1] = additional_state
   
"""
    处理最终的返回值，即最优控制输入。

    Parameters:
        vehicle_count   - 车辆数量
        control_input   - 预测的控制输入
   
    Return:
        optimal_return  - 每个车辆的最优控制输入
"""    
def deal_with_optimal_control(vehicle_count, control_input):
    print("---------------------------------- print optimal control input ----------------------------------" )
    optimal_return = []
    for index in range(vehicle_count):
        optimal_return.append(round(control_input[index, 0].X, 2))
    print("optimal control input is ", optimal_return)
    print("---------------------------------- print optimal control input ----------------------------------")
    return optimal_return

"""
    This is a function that uses gurobi to solve optimal control of platoon i.

    Parameters:
        state_of_platoon - list[
                                item: [vehicleID, vehiclePosition, vehicleVelocity, vehicleLength],
                                length: number of vehicle
                                ]
        state_of_pre_platoon - list[
                                    item: [vehiclePosition, vehicleVelocity, vehicleLength],
                                    length: size of predictive horizon
                                    description: 
                                    ]
                                int -1
        current_desire_velocity - float

    Returns:
        optimalResult - float
        state_of_last_vehicle - list[
                                    item: [vehiclePosition, vehicleVelocity, vehicleLength],
                                    length: size of predictive horizon
                                    description: 
                                    ]

    Raises:
        KeyError - raises an exception
"""
def main_solver(ego_pla, ego_pla_state, desire_velocity, pre_pla_state = -1, ego_pre_distance_to_conflict_point = -1, ego_pre_same_lane = 0):
    
    print(ego_pla)
    print(pre_pla_state)
    
    # the index of last vehicle
    last_vehicle_index = len(ego_pla_state) - 1
    
    # vehicle num of platoon
    vehicle_count = len(ego_pla_state)

    gurobi_model = gurobi_init()

    # 用 gurobi 定义变量
    control_input = gurobi_model.addVars(vehicle_count, predictive_horizon, lb = u_min, ub = u_max, name = "control_input")
    velocity = gurobi_model.addVars(vehicle_count, predictive_horizon, lb = v_min, ub = v_max, name = "velocity")
    position = gurobi_model.addVars(vehicle_count, predictive_horizon, lb = p_min, ub = p_max, name = "position")
    
    
    # 初始化成本函数，包括位置误差，速度误差，控制输入的误差
    p_cost_function = 0
    v_cost_function = 0
    u_cost_function = 0
    
    # 对未来 predictive_horizon 步长的时间进行状态预测，并更新成本函数
    for step in range(predictive_horizon):
        for index, vehicle in enumerate(ego_pla_state):
            u_cost_function += control_input[index, step] * control_input[index, step]
            # 首先是车辆状态的约束，根据当前车辆的状态，根据模型预测车辆下一个时刻的状态
            if step == 0:
                # 当前步骤为第一步时，下一步的速度应该为传进来的 state 加上预测值，位置预测的结果是行驶的距离
                gurobi_model.addLConstr(position[index, step] == vehicle[1] + (delta * vehicle[2] + math.pow(delta, 2) * control_input[index, step] / 2.0), name = "position_vehicle_" + vehicle[0] + "_step_" + str(step))
                gurobi_model.addLConstr(velocity[index, step] == vehicle[2] + (delta * control_input[index, step]), name = "velocity_vehicle_" + vehicle[0] + "_step_" + str(step))
            else:
                # 当前步骤不为第一步时，下一步的速度应该为上一步预测的状态加上预测值
                gurobi_model.addLConstr(position[index, step] == position[index, step - 1] + (delta * velocity[index, step - 1] + math.pow(delta, 2) * control_input[index, step] / 2.0), name = "position_vehicle_" + vehicle[0] + "_step_" + str(step))
                gurobi_model.addLConstr(velocity[index, step] == velocity[index, step - 1] + delta * control_input[index, step], name = "velocity_vehicle_" + vehicle[0] + "_step_" + str(step))
            
            # 若当前车辆是该车辆排的领队车辆，则判断该车辆排是 LVP Member 还是 LVP Leader，驾驶模式的分配只分配给每个车辆排的领队车辆
            if index == 0:
                if isinstance(pre_pla_state, list):
                    # 当前是LVP Member
                    v_cost_function += (pre_pla_state[step][1] - velocity[index, step]) * (pre_pla_state[step][1] - velocity[index, step])
                    if not ego_pre_same_lane:
                        # 当前排和前驱排完全不同，需要对状态进行处理，将距离变化为到冲突点的距离，利用生成的冲突点进行计算
                        ego_to_conflict_origin = position[index, step] - ego_pre_distance_to_conflict_point[0] 
                        pre_to_conflict_origin = pre_pla_state[step][0] - ego_pre_distance_to_conflict_point[1]
                        p_cost_function += (pre_to_conflict_origin - ego_to_conflict_origin - desire_space - pre_pla_state[step][2]) * (pre_to_conflict_origin - ego_to_conflict_origin - desire_space - pre_pla_state[step][2])
                    else:
                        # 当前排和前驱排处在同一条道路上，直接使用已经行驶的距离进行处理即可，不用进行变更
                        p_cost_function += (pre_pla_state[step][0] - position[index, step] - pre_pla_state[step][2] - desire_space) * (pre_pla_state[step][0] - position[index, step] - pre_pla_state[step][2] - desire_space)
                else:
                    # 当前是 LVP Leader
                    v_cost_function += (velocity[index, step] - desire_velocity) * (velocity[index, step] - desire_velocity)
                    if step == 0:
                        p_cost_function += (position[index, step] - vehicle[1] - delta * desire_velocity) * (position[index, step] - vehicle[1] - delta * desire_velocity)
                    else:
                        p_cost_function += (position[index, step] - position[index, step - 1] -  delta * desire_velocity) * (position[index, step] - position[index, step - 1] -  delta * desire_velocity)
            else:
                # 当前针对的是跟随车辆
                desire_prev_spacing = 0
                for i in range(0, index, 1):
                    desire_prev_spacing += ego_pla_state[i][3] + desired_space_inside
                p_cost_function += ((position[index - 1, step] - position[index, step] - ego_pla_state[index - 1][3] - desired_space_inside) * (position[index - 1, step] - position[index, step] - ego_pla_state[index - 1][3] - desired_space_inside) + (position[0, step] - position[index, step] - desire_prev_spacing) * (position[0, step] - position[index, step] - desire_prev_spacing))
                v_cost_function += ((velocity[index - 1, step] - velocity[index, step]) * (velocity[index - 1, step] - velocity[index, step]) + (velocity[0, step] - velocity[index, step]) * (velocity[0, step] - velocity[index, step]))
    # 求解车辆排最优化的值
    quadExpr = position_weight * p_cost_function + velocity_weight * v_cost_function + control_input_weight * u_cost_function
    gurobi_model.setObjective(quadExpr, gurobi.GRB.MINIMIZE)
    gurobi_model.optimize()
    ''' Once an optimize call has returned, the Gurobi optimizer sets the Status attribute of the model to one of several possible values
        LOADED          1  Model is loaded, but no solution information is available
        OPTIMAL         2  Model was solved to optimality (subject to tolerances), and an optimal solution is available
        INFEASIBLE      3  Model was proven to be infeasible
        INF_OR_UNBD     4  Model was proven to be either infeasible or unbounded. To obtain a more definitive conclusion, set the DualReductions parameter to 0 and reoptimize
        UNBOUNDED       5  Model was proven to be unbounded. Important note: an unbounded status indicates the presence of an unbounded ray that allows the objective to improve without limit. It says nothing about whether the model has a feasible solution. If you require information on feasibility, you should set the objective to zero and reoptimize
        CUTOFF          6  Optimal objective for model was proven to be worse than the value specified in the Cutoff parameter. No solution information is available
        ITERATION_LIMIT 7  Optimization terminated because the total number of simplex iterations performed exceeded the value specified in the IterationLimit parameter, or because the total number of barrier iterations exceeded the value specified in the BarIterLimit parameter
        NODE_LIMIT      8  Optimization terminated because the total number of branch and-cut nodes explored exceeded the value specified in the NodeLimit parameter
        TIME_LIMIT      9  Optimization terminated because the time expended exceeded the value specified in the TimeLimit parameter
        SOLUTION_LIMIT  10 Optimization terminated because the number of solutions found reached the value specified in the SolutionLimit parameter
        INTERRUPTED     11 Optimization was terminated by the user
        NUMERIC         12 Optimization was terminated due to unrecoverable numerical difficulties
        SUBOPTIMAL      13 Unable to satisfy optimality tolerances; a sub-optimal solution is availab
        INPROGRESS      14 An asynchronous optimization call was made, but the associated optimization run is not yet complete
        USER_OBJ_LIMIT  15 User specified an objective limit (a bound on either the best objective or the best bound), and that limit has been reached
    
    print("---------------------------------- print gurobi solve time ----------------------------------" )
    print("gurobi solve time is ", end - start)
    print("---------------------------------- print gurobi solve time ----------------------------------" ) '''
    # print("model objective is ", gurobi_model.getObjective())
    if gurobi_model.status == gurobi.GRB.status.OPTIMAL or gurobi_model.status == gurobi.GRB.status.SUBOPTIMAL:
        deal_with_spacing_error(position, pre_pla_state, ego_pre_distance_to_conflict_point)
        # 不管是何种状态，都需要进行额外状态的计算，接收的应该是上一个步骤预测的这个步骤的状态，排除第一个状态，添加一个额外的新状态作为最优状态
        additional_state = deal_with_additional_state(position, velocity, last_vehicle_index, ego_pla_state)
        deal_with_predictive_state(ego_pla, position, last_vehicle_index, velocity, additional_state, ego_pla_state)
        optimal_return =  deal_with_optimal_control(vehicle_count, control_input)
        return optimal_return
    else:
        print("model status is ", gurobi_model.status, "model is unsolvable", sep = ' ')
        exit(-1)