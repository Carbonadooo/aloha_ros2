import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import socket
import struct
import threading

class JointStateReceiver(Node):
    def __init__(self):
        super().__init__('joint_state_receiver')
        # 创建ROS2发布者
        self.publisher = self.create_publisher(JointState, '/external_joint_states', 10)
        
        # 初始化TCP服务器
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 8888))
        self.server_socket.listen(1)
        
        # 启动独立线程处理网络连接
        self.conn = None
        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.start()
        self.get_logger().info("Listening on leader arm socket")

    def _receive_loop(self):
        """独立线程处理网络连接"""
        try:
            self.conn, addr = self.server_socket.accept()
            self.get_logger().info(f"Connected by {addr}")
            
            while rclpy.ok():
                # 接收并解析数据
                data = self._receive_exact(72)
                positions = struct.unpack('!9d', data)
                
                # 转换为ROS2消息并发布
                msg = JointState()
                msg.position = list(positions)
                self.publisher.publish(msg)
                
        except Exception as e:
            self.get_logger().error(f"Connection error: {str(e)}")
        finally:
            if self.conn:
                self.conn.close()

    def _receive_exact(self, size: int) -> bytes:
        """确保接收指定长度的数据"""
        data = b''
        while len(data) < size and rclpy.ok():
            packet = self.conn.recv(size - len(data))
            if not packet:
                raise ConnectionError("Connection closed")
            data += packet
        return data

    def destroy_node(self):
        """重写销毁方法确保资源释放"""
        self.server_socket.close()
        if self.conn:
            self.conn.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    receiver = JointStateReceiver()
    rclpy.spin(receiver)
    receiver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()