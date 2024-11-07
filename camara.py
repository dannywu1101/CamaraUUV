#!/usr/bin/env python3
# by Danny Wu

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ZedVideoNode(Node):
    def __init__(self):
        super().__init__('zed_video_node')
        self.publisher_ = self.create_publisher(Image, 'zed_video', 10)
        self.bridge = CvBridge()

        # Ajusta el índice de la cámara si es necesario (0 es la cámara predeterminada)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        self.timer = self.create_timer(0.1, self.publish_frame)
        self.get_logger().info("Nodo de video de ZED iniciado")

    def publish_frame(self):
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher_.publish(msg)
            self.get_logger().info("Publicando frame de ZED")
        else:
            self.get_logger().warning("No se pudo capturar el frame de la cámara")

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ZedVideoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
