import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import socket
import struct

class JointStateSender(Node):
    def __init__(self):
        super().__init__('joint_state_sender')
        # 创建订阅者，订阅 /wx250s/joint_states 主题
        self.subscription = self.create_subscription(
            JointState,
            '/wx250s/joint_states',
            self.listener_callback,
            10
        )
        self.subscription  # 防止未使用的变量警告
        # 初始化socket并连接到接收端
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('robot-helper', 8888))
        self.get_logger().info("Connected to robot-helper")

    def listener_callback(self, msg: JointState):
        # 打包消息以便通过socket发送
        data = self.pack_joint_state(msg)
        try:
            # 发送数据
            self.client_socket.sendall(data)
        except Exception as e:
            self.get_logger().error(f"Socket send error: {e}")

    def pack_joint_state(self, msg: JointState):
        positions = msg.position[:9]
        # '!'表示网络字节序，'6d'表示6个double
        packed_data = struct.pack('!9d', *positions)
        return packed_data

def main(args=None):
    rclpy.init(args=args)
    joint_state_sender = JointStateSender()
    rclpy.spin(joint_state_sender)
    # 关闭socket连接
    joint_state_sender.client_socket.close()
    joint_state_sender.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
