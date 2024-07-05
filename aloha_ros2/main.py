from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import (
    create_interbotix_global_node,
    robot_shutdown,
    robot_startup,
)
from interbotix_xs_msgs.msg import JointSingleCommand
from aloha_ros2.constants import MASTER2PUPPET_JOINT_FN, DT, START_ARM_POSE, MASTER_GRIPPER_JOINT_MID, PUPPET_GRIPPER_JOINT_CLOSE
from aloha_ros2.robot_utils import torque_on, torque_off, move_arms, move_grippers, get_arm_gripper_positions
import time



def prep_robots(master_bot: InterbotixManipulatorXS, puppet_bot: InterbotixManipulatorXS):
    puppet_bot.core.robot_reboot_motors("single","gripper",True)
    puppet_bot.core.robot_set_operating_modes("group", "arm", "position")
    puppet_bot.core.robot_set_operating_modes("single", "gripper", "current_based_position")
    master_bot.core.robot_set_operating_modes("group", "arm", "position")
    master_bot.core.robot_set_operating_modes("single", "gripper", "position")

    torque_on(puppet_bot)
    torque_on(master_bot)

    start_arm_qpos = START_ARM_POSE[:6]
    move_arms([master_bot, puppet_bot], [start_arm_qpos]*2, move_time=1)
    move_grippers([master_bot, puppet_bot], [MASTER_GRIPPER_JOINT_MID, PUPPET_GRIPPER_JOINT_CLOSE], move_time=0.5)
    
    
def press_to_start(master_bot):
    master_bot.core.robot_torque_enable("single", "gripper", False)
    print(f"Close the gripper to start")
    close_threshold = -0.3
    pressed = False
    while not pressed:
        gripper_pos = get_arm_gripper_positions(master_bot)
        if gripper_pos < close_threshold:
            pressed = True
        time.sleep(DT/10)
    torque_off(master_bot)
    print(f"Started!")

def teleop():
    global_node = create_interbotix_global_node()
    master_bot = InterbotixManipulatorXS(robot_model="wx250s", group_name="arm", gripper_name="gripper", node=global_node)
    puppet_bot = InterbotixManipulatorXS(robot_model="vx300s", group_name="arm", gripper_name="gripper", node=global_node)
    robot_startup(global_node)

    prep_robots(master_bot, puppet_bot)
    press_to_start(master_bot)


    ### Teleoperation loop
    gripper_command = JointSingleCommand(name='gripper')
    while True:
        # sync joint positions
        master_state_joints = master_bot.core.joint_states.position[:6]
        puppet_bot.arm.set_joint_positions(master_state_joints,blocking=False)
        # sync gripper positions
        master_gripper_joint = master_bot.core.joint_states.position[6]
        puppet_gripper_joint_target = MASTER2PUPPET_JOINT_FN(master_gripper_joint)
        gripper_command.cmd = puppet_gripper_joint_target
        puppet_bot.gripper.core.pub_single.publish(gripper_command)
        #sleep DT
        time.sleep(DT)

if __name__=='__main__':
    teleop()