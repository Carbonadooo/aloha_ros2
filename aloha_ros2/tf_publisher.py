import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_matrix, inverse_matrix
import os
import yaml
import numpy as np
from ament_index_python.packages import get_package_share_directory

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_publisher')
        self.tf_broadcaster = StaticTransformBroadcaster(self)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.package_share_directory = get_package_share_directory("robotic_arm")
        self.broadcast_c2g_tf()
        self.create_timer(5.0, self.broadcast_camera_tf)  # Timer to call broadcast_camera_tf every 5 seconds

    def broadcast_c2g_tf(self):
        tf_file_path = os.path.join(self.package_share_directory, "config", "transform_camera2gripper.yaml")
        with open(tf_file_path, "r") as file:
            c2g_file = yaml.safe_load(file)
        c2g_matrix = np.array(c2g_file["camera2gripper"])
        c2g_tf = TransformStamped()
        c2g_tf.header.stamp = self.get_clock().now().to_msg()
        c2g_tf.header.frame_id = "vx300s/ee_gripper_link"
        c2g_tf.child_frame_id = "camera_frame"
        c2g_tf.transform.translation.x = c2g_matrix[0][3]
        c2g_tf.transform.translation.y = c2g_matrix[1][3]
        c2g_tf.transform.translation.z = c2g_matrix[2][3]
        c2g_tf.transform.rotation.x, c2g_tf.transform.rotation.y, c2g_tf.transform.rotation.z, c2g_tf.transform.rotation.w = quaternion_from_matrix(c2g_matrix)
        self.tf_broadcaster.sendTransform(c2g_tf)
        self.get_logger().info("Broadcasted camera-to-gripper transform")

    def broadcast_camera_tf(self):
        try:
            tf = self.tf_buffer.lookup_transform(
                "D435i_color_optical_frame",
                "D435i_link",
                rclpy.time.Time()
            )
            tf.header.stamp = self.get_clock().now().to_msg()
            tf.header.frame_id = "camera_frame"
            self.tf_broadcaster.sendTransform(tf)
            # self.get_logger().info("Broadcasted camera transform")
        except Exception as e:
            self.get_logger().warn(f"Failed to broadcast camera transform: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = TFBroadcaster()
    try:
        rclpy.spin(node)  # No need for manual looping; timer handles periodic calls
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
