import gurobipy as gurobi
import math
import time
import sys

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

from utils.common_stuff import delta, u_max, u_min, v_max, v_min, p_max, p_min, desire_space, desired_space_inside, predictive_horizon, position_weight, velocity_weight, control_input_weight, platoon_transmit_state

def gurobi_init():
    
    # 针对提出的交叉口创建 gurobi 模型
    model = gurobi.Model("optimal_control_input_solver")
    
    # 定义 gurobi 处理非凸二次规划的策略
    model.Params.NonConvex = 2
    
    return model

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
def main_solver(ego_pla, ego_pla_state, pre_pla_state, desire_velocity):
    
    start = time.time()
    
    # the index of last vehicle
    last_vehicle_index = ego_pla_state.index(ego_pla_state[-1])
    
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
    
    # put the predictive state of last vehicle
    predictive_state = []
    
    additional_state = []
    
    print(pre_pla_state)
    
    # 对未来 predictive_horizon 步长的时间进行状态预测，并更新成本函数
    for step in range(predictive_horizon):
        for index, vehicle in enumerate(ego_pla_state):
            u_cost_function += control_input[index, step] * control_input[index, step]
            # 首先是车辆状态的约束，根据当前车辆的状态，根据模型预测车辆下一个时刻的状态
            if step == 0:
                # 当前步骤为第一步时，下一步的速度应该为传进来的 state 加上预测值
                gurobi_model.addLConstr(position[index, step] == vehicle[1] + (delta * vehicle[2] + math.pow(delta, 2) * control_input[index, step] / 2.0), name = "position_vehicle_" + vehicle[0] + "_step_" + str(step))
                gurobi_model.addLConstr(velocity[index, step] == vehicle[2] + (delta * control_input[index, step]), name = "velocity_vehicle_" + vehicle[0] + "_step_" + str(step))
            else:
                # 当前步骤不为第一步时，下一步的速度应该为上一步预测的状态加上预测值
                gurobi_model.addLConstr(position[index, step] == position[index, step - 1] + (delta * velocity[index, step - 1] + math.pow(delta, 2) * control_input[index, step] / 2.0), name = "position_vehicle_" + vehicle[0] + "_step_" + str(step))
                gurobi_model.addLConstr(velocity[index, step] == velocity[index, step - 1] + delta * control_input[index, step], name = "velocity_vehicle_" + vehicle[0] + "_step_" + str(step))
            
            # 若当前车辆是该车辆排的领队车辆，则判断该车辆排是 LVP Member 还是 LVP Leader，驾驶模式的分配只分配给每个车辆排的领队车辆
            if index == 0:
                if isinstance(pre_pla_state, list):
                    # 当前是LVP member，传递的位置是以冲突点为中心点的位置
                    p_cost_function += (pre_pla_state[step][0] - position[index, step] - pre_pla_state[step][2] - desire_space) * (pre_pla_state[step][0] - position[index, step] - pre_pla_state[step][2] - desire_space)
                    v_cost_function += (pre_pla_state[step][1] - velocity[index, step]) * (pre_pla_state[step][1] - velocity[index, step])
                else:
                    # 当前是 LVP leader，传递的位置是以行驶的距离为主的，只要行驶的距离相同 则就能够保证他们的间距相同
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
    # Once an optimize call has returned, the Gurobi optimizer sets the Status attribute of the model to one of several possible values
    #     LOADED          1  Model is loaded, but no solution information is available
    #     OPTIMAL         2  Model was solved to optimality (subject to tolerances), and an optimal solution is available
    #     INFEASIBLE      3  Model was proven to be infeasible
    #     INF_OR_UNBD     4  Model was proven to be either infeasible or unbounded. To obtain a more definitive conclusion, set the DualReductions parameter to 0 and reoptimize
    #     UNBOUNDED       5  Model was proven to be unbounded. Important note: an unbounded status indicates the presence of an unbounded ray that allows the objective to improve without limit. It says nothing about whether the model has a feasible solution. If you require information on feasibility, you should set the objective to zero and reoptimize
    #     CUTOFF          6  Optimal objective for model was proven to be worse than the value specified in the Cutoff parameter. No solution information is available
    #     ITERATION_LIMIT 7  Optimization terminated because the total number of simplex iterations performed exceeded the value specified in the IterationLimit parameter, or because the total number of barrier iterations exceeded the value specified in the BarIterLimit parameter
    #     NODE_LIMIT      8  Optimization terminated because the total number of branch and-cut nodes explored exceeded the value specified in the NodeLimit parameter
    #     TIME_LIMIT      9  Optimization terminated because the time expended exceeded the value specified in the TimeLimit parameter
    #     SOLUTION_LIMIT  10 Optimization terminated because the number of solutions found reached the value specified in the SolutionLimit parameter
    #     INTERRUPTED     11 Optimization was terminated by the user
    #     NUMERIC         12 Optimization was terminated due to unrecoverable numerical difficulties
    #     SUBOPTIMAL      13 Unable to satisfy optimality tolerances; a sub-optimal solution is availab
    #     INPROGRESS      14 An asynchronous optimization call was made, but the associated optimization run is not yet complete
    #     USER_OBJ_LIMIT  15 User specified an objective limit (a bound on either the best objective or the best bound), and that limit has been reached
    
    # 程序代码段运行
    end = time.time()
    # print("---------------------------------- print gurobi solve time ----------------------------------" )
    # print("gurobi solve time is ", end - start)
    # print("---------------------------------- print gurobi solve time ----------------------------------" )
    
    if gurobi_model.status == gurobi.GRB.status.OPTIMAL:
        print("model objective ", gurobi_model.getObjective())
        
        # 额外状态的计算
        # 接收的应该是上一个步骤预测的这个步骤的状态
        # 排除第一个状态，添加一个额外的新状态作为最优状态
        additional_position = round(position[last_vehicle_index, predictive_horizon - 1].X, 2) + round(velocity[last_vehicle_index, predictive_horizon - 1].X, 2) * delta
        additional_velocity = round(velocity[last_vehicle_index, predictive_horizon - 1].X, 2)
        for step in range(1, predictive_horizon):
            additional_state.append([round(position[last_vehicle_index, step].X, 2), round(velocity[last_vehicle_index, step].X, 2), ego_pla_state[-1][3]])
            # if isinstance(state_of_pre_platoon, list):
            #     print("the space error with pre platoon is ", state_of_pre_platoon[step][0] - position[0, step].X + state_of_pre_platoon[step][2] + desire_space)
        # put additional state into 
        additional_state.append([additional_position, additional_velocity, ego_pla_state[last_vehicle_index][3]])
        
        # 首先判断是否存在值，若不存在，初始化传回的状态列表的值，若存在，则更新传回的状态的列表值
        if not len(platoon_transmit_state[ego_pla]):
            # 该车辆排的传回状态存储列表为空，则用当前状态进行初始化，不使用额外状态进行次年初，注意要存两个状态
            for step in range(predictive_horizon):
                predictive_state.append([round(position[last_vehicle_index, step].X, 2), round(velocity[last_vehicle_index, step].X, 2), ego_pla_state[-1][3]])
            platoon_transmit_state[ego_pla].append(predictive_state)
            platoon_transmit_state[ego_pla].append(additional_state)
        else:
            # 该车辆排的传回状态存储列表不为空，首先对换两个状态的位置，
            platoon_transmit_state[ego_pla][0] = platoon_transmit_state[ego_pla][1]
            platoon_transmit_state[ego_pla][1] = additional_state
        
        
        print("---------------------------------- print optimal control input ----------------------------------" )
        # 最终的返回值
        optimal_return = []
        for index in range(vehicle_count):
            optimal_return.append(round(control_input[index, 0].X, 2))
        print("optimal control input is ", optimal_return)
        print("---------------------------------- print optimal control input ----------------------------------")
        return optimal_return, end - start
    else:
        print("model status is ", gurobi_model.status, "model is unsolvable", sep = ' ')
        exit(-1)