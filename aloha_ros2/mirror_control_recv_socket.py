import rclpy
import socket
import struct
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

        self.gripper_command = JointSingleCommand(name='gripper')
        # 初始化socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))  # 绑定地址和端口
        self.server_socket.listen(1)
        self.node.create_timer(0.1, self.socket_receive_callback)  # 创建定时器来接收socket消息

    def socket_receive_callback(self):
        try:
            conn, addr = self.server_socket.accept()
            with conn:
                data = conn.recv(1024)  # 接收数据
                if data:
                    # 解析数据为JointState消息
                    msg = self.parse_joint_state(data)
                    self.leader_state_callback(msg)
        except Exception as e:
            self.node.get_logger().error(f"Socket error: {e}")

    def parse_joint_state(self, data):
        # 这里需要根据实际的socket数据格式进行解析
        # 假设数据格式为：name_count, name1, name2, ..., position_count, position1, position2, ...
        # 简单示例，需要根据实际情况修改
        msg = JointState()
        # 解析name
        name_count = struct.unpack('!I', data[:4])[0]
        data = data[4:]
        names = []
        for _ in range(name_count):
            name_length = struct.unpack('!I', data[:4])[0]
            data = data[4:]
            name = data[:name_length].decode('utf-8')
            data = data[name_length:]
            names.append(name)
        msg.name = names
        # 解析position
        position_count = struct.unpack('!I', data[:4])[0]
        data = data[4:]
        positions = []
        for _ in range(position_count):
            position = struct.unpack('!d', data[:8])[0]
            data = data[8:]
            positions.append(position)
        msg.position = positions
        # 假设velocity和effort为空
        msg.velocity = []
        msg.effort = []
        return msg

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
