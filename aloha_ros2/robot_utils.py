import numpy as np
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from constants import DT
import time

def get_arm_joint_positions(bot: InterbotixManipulatorXS):
    return bot.core.joint_states.position[:6]

def move_arms(bot_list, target_pose_list, mvoe_time=1):
    num_steps=int(mvoe_time/DT)
    curr_pose_list=[get_arm_joint_positions(bot) for bot in bot_list]
    traj_list=[np.linspace(curr_pose, target_pose, num_steps) for curr_pose, target_pose in zip(curr_pose_list, target_pose_list)]
    for t in range(num_steps):
        for bot_id, bot in enumerate(bot_list):
            bot.arm.set_joint_positions(traj_list[bot_id][t], blocking=False)
        time.sleep(DT)
def torque_off(bot: InterbotixManipulatorXS):
    bot.core.robot_torque_enable("group", "arm", False)
    bot.core.robot_torque_enable("single", "gripper", False)

def torque_on(bot: InterbotixManipulatorXS):
    bot.core.robot_torque_enable("group", "arm", True)
    bot.core.robot_torque_enable("single", "gripper", True)