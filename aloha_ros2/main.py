from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_xs_msgs.msg import JointSingleCommand
from constants import MASTER2PUPPET_JOINT_FN, DT, START_ARM_POSE, MASTER_GRIPPER_JOINT_MID, PUPPET_GRIPPER_JOINT_CLOSE
import time


def prep_robots(master_bot, puppet_bot):
    pass
def press_to_start(master_bot):
    pass

def teleop():
    master_bot = InterbotixManipulatorXS(robot_model="wx250s", group_name="arm", gripper_name="gripper", robot_name='master')
    puppet_bot = InterbotixManipulatorXS(robot_model="vx300s", group_name="arm", gripper_name="gripper", robot_name='puppet')

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