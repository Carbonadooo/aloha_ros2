import rclpy
from interbotix_common_modules.common_robot.robot import (
    robot_shutdown,
    robot_startup,
)
from sensor_msgs.msg import JointState
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_xs_msgs.msg import JointSingleCommand
from aloha_ros2.constants import MASTER2PUPPET_JOINT_FN

class FollowerArm(InterbotixManipulatorXS):
    def __init__(self):
        InterbotixManipulatorXS.__init__(
            self,
            robot_model="vx300s",
            group_name="arm", 
            gripper_name="gripper", 
        )
        self.node = self.core.get_node()
        self.node.create_subscription(
            JointState,
            "/wx250s/joint_states",
            self.leader_state_callback,
            10,
        )
        self.gripper_command = JointSingleCommand(name='gripper')

    def leader_state_callback(self, msg: JointState):
        positions = msg.position[:6]
        self.arm.set_joint_positions(positions, blocking=False)
        follower_gripper_joint_target = MASTER2PUPPET_JOINT_FN(msg.position[6])
        self.gripper_command.cmd = follower_gripper_joint_target
        self.gripper.core.pub_single.publish(self.gripper_command)

def main(args=None):
    rclpy.init(args=args)
    bot = FollowerArm()
    robot_startup(bot.node)
    rclpy.spin(bot.node)
    print("Shutting down")
    robot_shutdown(bot.node)


if __name__ == '__main__':
    main()
