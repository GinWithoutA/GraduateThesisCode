# 集中式执行时候的主要方法
import optparse
import os
import sys

# 我们需要从 $SUMO_HOME/tools 目录中引入 python 模块
# 或者直接指定 $SUMO_HOME/tools 目录的位置
# sys.path.append(os.path.join('E:', os.sep, 'SUMO', os.sep, 'sumo-1.13.0', os.sep, 'tools'))
if 'SUMO_HOME' in os.environ :
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    print(sys.path)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# 添加项目路径到 python 路径中
sys.path.append('D:\Coding Projects\GraduateProject\SUMO Project\simulation_for_my_literatual')

import utils.plot_state as plt
from algorithm.supervision_level.deal_with_pla_v2 import main_solver as solver_v2
from algorithm.supervision_level.deal_with_pla_v4 import main_solver as solver_v4
from algorithm.supervision_level.deal_with_pla_v5 import main_solver as solver_v5

# 引入 sumo 相关的工具
from sumolib import checkBinary
import traci

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    # sumo -c demo.sumocfg --fcd-output fcd.xml
    traci.start([sumoBinary, "-c", "data/sumo_experiment/intersection.sumocfg"])
    
    # 初始化画布，位置画布，速度画布，求解时间画布
    position_canvas, velocity_canvas, solve_time_canvas, acceleration_canvas, spacing_error_canvas = plt.plot_init()  
    CO2_canvas, CO_canvas, HC_canvas, PMx_canvas, NOx_canvas, fuel_canvas, noise_canvas, WT_canvas, AWT_canvas, TL_canvas = plt.indicator_plot_2D_init()

    # the unit of step is sec
    for step in range(171):
        
        # 获取所有车辆的 ID
        all_vehicle_id = traci.vehicle.getIDList()
        
        plt.update_state(traci, all_vehicle_id, step)
        
        
        # 首先判断谁先到达交叉口，首先以交叉口中心点，然后再通过冲突点进行间距的计算
        # deal with platoon 0
        
        
        # 推进仿真
        traci.simulationStep()
        
        # 每一步仿真的间隔，这里设置为 1s 
        # time.sleep(0.1)
    
    traci.close()

    plt.show_state(position_canvas, velocity_canvas, solve_time_canvas, acceleration_canvas, spacing_error_canvas)
    plt.show_state_indicator(CO2_canvas, CO_canvas, HC_canvas, PMx_canvas, NOx_canvas, fuel_canvas, noise_canvas, WT_canvas, AWT_canvas, TL_canvas)
    plt.list_to_csv('baseline/')
    plt.show()