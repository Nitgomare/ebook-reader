import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from tf_transformations import euler_from_quaternion
import time
from datetime import datetime


class TFListener(Node):

    def __init__(self):
        super().__init__('tf2_listener')
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.timer = self.create_timer(1, self.get_transform)

    def get_transform(self):
        try:
            tf = self.buffer.lookup_transform(
                'map', 'base_footprint', rclpy.time.Time(seconds=0), rclpy.time.Duration(seconds=1))
            transform = tf.transform
            rotation_euler = euler_from_quaternion([
                transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w
            ])
            self.get_logger().info(
                f'平移:{transform.translation},旋转四元数:{transform.rotation}:旋转欧拉角:{rotation_euler}')
                
                    
            #将元组数据存储在文本文件中
            current_time = time.time()
            # 获取当前时间戳
            now = datetime.now()
            with open('data.txt', 'a') as file:
            # 将数据转换为字符串，并追加换行符
               line = "平移:"+ str(transform.translation) + "旋转四元数:" + str(transform.rotation) + "旋转欧拉角:" + str(rotation_euler) +  "/time:" + now.strftime("%H:%M:%S") + '\n'
            # 写入文件
               file.write(line)
            
            
        except Exception as e:
            self.get_logger().warn(f'不能够获取坐标变换，原因: {str(e)}')


def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
