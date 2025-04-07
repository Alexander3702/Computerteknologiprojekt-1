#!/usr/bin/env python3
#
# Copyright 2018 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Jeonggeun Lim, Ryan Shim, Gilbert

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.qos import QoSProfile
from sensor_msgs.msg import LaserScan
import time


class Turtlebot3ObstacleDetection(Node):

    def __init__(self):
        super().__init__('turtlebot3_obstacle_detection')
        print('TurtleBot3 Obstacle Detection - Auto Move Enabled')
        print('----------------------------------------------')
        print('stop angle: -90 ~ 90 deg')
        print('stop distance: 0.25 m')
        print('----------------------------------------------')

        self.scan_ranges = []
        self.has_scan_received = False

        #initialising the collision count to 0 as standard. 
        self.collision_count = 0
        #implementing a collision state to only print a new collision, whenever the robot is within a new state
        self.in_collision_state = False
        #setting a collision range, to measure the distance from the sensor to where our robot would collide
        self.collision_range = 0.1

        #needs to be implemented next time!!!!!
        self.average_linear_speed = 0.0 
        

        self.stop_distance = 0.25
        self.tele_twist = Twist()
        self.tele_twist.linear.x = 0.2
        self.tele_twist.angular.z = 0.0

        qos = QoSProfile(depth=10)

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', qos)

        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            qos_profile=qos_profile_sensor_data)

        self.cmd_vel_raw_sub = self.create_subscription(
            Twist,
            'cmd_vel_raw',
            self.cmd_vel_raw_callback,
            qos_profile=qos_profile_sensor_data)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def scan_callback(self, msg):
        self.scan_ranges = msg.ranges
        self.has_scan_received = True

    def cmd_vel_raw_callback(self, msg):
        self.tele_twist = msg

    def timer_callback(self):
        if self.has_scan_received:
            self.detect_obstacle()

    def detect_obstacle(self):

        self.scan_ranges = [i if (i > 0 and i <= 3.5) else 3.5 for i in self.scan_ranges]

        middle = self.scan_ranges [342:360] + self.scan_ranges[0:18]
        left = self.scan_ranges[18:54]
        far_left = self.scan_ranges[54:90]
        #ff_left = self.scan_ranges[90:98]
        right = self.scan_ranges[306:342]
        far_right = self.scan_ranges[270:306]
        #ff_right = self.scan_ranges[262:270]

        middle_min = min(middle)
        left_min = min(left)
        far_left_min = min(far_left)
        right_min = min(right)
        far_right_min = min(far_right)
        #ff_right_min = min(ff_right)
        #ff_left_min = min(ff_left)



        twist = Twist()
        # Check each section and respond accordingly
        if middle_min < self.stop_distance:
            twist.linear.x = 0.0
            self.get_logger().info('Obstacle detected in front! Turning.', throttle_duration_sec=2)
        
            # Decide which way to turn based on side readings
            if left_min > right_min:
                twist.angular.z = 0.5  # Turn left if more space on the left
            else:
                twist.angular.z = -0.5  # Turn right if more space on the right
            
        elif left_min < self.stop_distance:
            twist.linear.x = 0.1  # Slow down
            twist.angular.z = -0.3  # Turn right away from left obstacle
            self.get_logger().info('Obstacle detected on left!', throttle_duration_sec=2)

        elif right_min < self.stop_distance:
            twist.linear.x = 0.1  # Slow down
            twist.angular.z = 0.3  # Turn left away from right obstacle
            self.get_logger().info('Obstacle detected on right!', throttle_duration_sec=2)
        
        elif far_left_min < self.stop_distance:
            twist.linear.x = 0.2  # Continue but slower
            twist.angular.z = -0.2  # Slight right turn
            self.get_logger().info('Obstacle detected on far left!', throttle_duration_sec=2)
        
        elif far_right_min < self.stop_distance:
            twist.linear.x = 0.2  # Continue but slower
            twist.angular.z = 0.2  # Slight left turn
            self.get_logger().info('Obstacle detected on far right!', throttle_duration_sec=2)
        
       # elif ff_left_min < self.stop_distance:
           # twist.linear.x = 0.1
            #twist.angular.z = -0.1
            #self.get_logger().info('Obstacle detected on far far left!', throttle_duration_sec = 2)
        
       # elif ff_right_min < self.stop_distance:
           # twist.linear.x = 0.1
           # twist.angular.z = 0.1
           # self.get_logger().info('Obstacle detected on far far right!', throttle_duration_sec = 2)
        else:
            # No obstacles detected, drive forward!
            if self.tele_twist is not None:
                twist = self.tele_twist
            else:
                # Default forward motion if no teleop commands
                twist.linear.x = 0.2
                twist.angular.z = 0.0
            self.get_logger().info('No obstacles, driving forward', throttle_duration_sec=5)
    
    
    # Check if any obstacle is within the stop distance
        collision_detected = (
            far_right_min < self.collision_range or 
            far_left_min < self.collision_range or 
            right_min < self.collision_range or 
            left_min < self.collision_range or 
            middle_min < self.collision_range
        )
    
    # Only increment count when transitioning from no collision to collision
        if collision_detected and not self.in_collision_state:
            self.collision_count += 1
            self.get_logger().info(f'New collision detected! Total: {self.collision_count}')
            self.in_collision_state = True
    
    # Reset state when all obstacles are cleared
        elif not collision_detected and self.in_collision_state:
            self.in_collision_state = False
            self.get_logger().info('Obstacle cleared')
            

        self.update_speed_stats(twist.linear.x)

        self.cmd_vel_pub.publish(twist)
    
    def update_speed_stats(self, current_speed):
        if current_speed != self.last_speed
            self.speed_sum += current_speed
            self.speed_index += 1
            self.last_speed = current_speed

    def detect_obstacle_collision(self):
        return self.collision_count


    


    def stop_robot(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)





        

def main(args=None):
    print("Test af main")
    rclpy.init(args=args)
    turtlebot3_obstacle_detection = Turtlebot3ObstacleDetection()
    
    #setting starttime and endtime to make the robot run for specific amount of time. 
    start_time = time.time()
    end_time = start_time + 30.0

    #running the robot for 30 seconds. We're updating the robot's position every 0.1 seconds.
    while time.time() < end_time:
        rclpy.spin_once(turtlebot3_obstacle_detection, timeout_sec = 0.1)

    turtlebot3_obstacle_detection.stop_robot()
    

    turtlebot3_obstacle_detection.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
