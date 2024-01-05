from enum import Enum

class in_flag(Enum):
    IN = 1
    OUT = 0

class l_m_check_flag(Enum):
    CHECKED = 1
    NOT_YET = 0
    
class road_ender_save_flag(Enum):
    SAVED = 1
    NOT_YET = 0
    
class pass_conflict_already_flag(Enum):
    PASSING = 1
    NOT_YET = 0
    
class ego_pre_same_lane_flag(Enum):
    SAME = 2
    HALF_SAME = 1
    DIFFERENT = 0