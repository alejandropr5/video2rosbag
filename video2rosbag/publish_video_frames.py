import rclpy 
from rclpy.node import Node 
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge, CvBridgeError 
import numpy as np
import time
import cv2 
import os
from ament_index_python.packages import get_package_share_directory

class ImagePublisher(Node):

    def __init__(self):
        super().__init__('image_publisher')
        
        self.image_pub = self.create_publisher(Image,'raw_video_frames',10)

        self.br = CvBridge()

    def publish_frames(self):
        vid_path = os.path.join(
            get_package_share_directory('video2rosbag'),
            'videos',
            'walker.mp4')
        cap = cv2.VideoCapture(vid_path)

        if not cap.isOpened():
            print("Cannot open video")
            exit()
        while True:
            # Capture frame-by-frame
            ret, current_frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Stream ended. Exiting ...")
                break
            
            im_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
            img_msg = self.br.cv2_to_imgmsg(im_rgb,'rgb8') 
            img_msg.header.stamp = self.get_clock().now().to_msg() 
            img_msg.header.frame_id = "video_frames" 

            self.image_pub.publish(img_msg) 

            time.sleep(0.005) 
        # When everything done, release the capture
        cap.release()

def main(args=None):
    rclpy.init(args=args)

    image_publisher = ImagePublisher()

    image_publisher.publish_frames()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()