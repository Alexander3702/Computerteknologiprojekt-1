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
import smbus
from gpiozero import LED


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

        #implementing the average linear speed
        self.average_linear_speed = 0.0 
        self.speed_sum = 0.0
        self.speed_index = 0
        self.last_speed = 0.0

        self.stop_distance = 0.25
        self.tele_twist = Twist()
        self.tele_twist.linear.x = 0.21
        self.tele_twist.angular.z = 0.0
        self.led = LED(18)

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

        # Color detection and victim pickup parameters
        self.bus = smbus.SMBus(1)
        #configuring color sensors
        self.bus.write_byte_data(0x44, 0x01, 0x05)
        #Victims picked up in a single run
        self.victims_picked = 0
        #Pickup index to keep track of the amount of victimreadings
        self.pickup_index = 0
        #Pickup state to make sure, we don't pickup the same victim twice
        self.in_pickup_state = False
        #counting cosecutive non-victim readings
        self.non_red_consecutive_count = 0
        # resetiing the pickup state after this amount of non-victim readings
        self.reset_threshold = 10

    

    def scan_callback(self, msg):
        self.scan_ranges = msg.ranges
        self.has_scan_received = True

    def cmd_vel_raw_callback(self, msg):
        self.tele_twist = msg

    def timer_callback(self):
        twist = Twist()
        if not self.has_scan_received:
            # Move forward if no scan data yet
            twist.linear.x = 0.2
            twist.angular.z = 0.0
            self.cmd_vel_pub.publish(twist)
            self.get_logger().info('Moving forward while waiting for scan data')
        else:
            self.detect_obstacle()

    def detect_obstacle(self):

        self.scan_ranges = [i if (i > 0 and i <= 3.5) else 3.5 for i in self.scan_ranges]

        middle = self.scan_ranges [342:360] + self.scan_ranges[0:18]
        left = self.scan_ranges[18:42]
        far_left = self.scan_ranges[42:66]
        farfar_left = self.scan_ranges[66:90]
        right = self.scan_ranges[318:342]
        far_right = self.scan_ranges[294:318]
        farfar_right = self.scan_ranges[270:294]
        

        middle_min = min(middle)
        left_min = min(left)
        far_left_min = min(far_left)
        farfar_left_min = min(farfar_left)
        right_min = min(right)
        far_right_min = min(far_right)
        farfar_right_min = min(farfar_right)

        
        twist = Twist()
        
        # Check each section and respond accordingly
        if middle_min < self.stop_distance:
            left_space = min(left_min, far_left_min, farfar_left_min)
            right_space = min(right_min, far_right_min, farfar_right_min)
            twist.linear.x = 0.0
            # Check which side has more space by comparing all sections
            if left_space > right_space:
                twist.angular.z = 1.5
            else:
                twist.angular.z = -1.5
            self.get_logger().info('Obstacle detected in front! Turning.', throttle_duration_sec=2)
    
        elif left_min < self.stop_distance:
            # Check if far_left and farfar_left offer a path
            if far_left_min > self.stop_distance and farfar_left_min > self.stop_distance:
                twist.linear.x = 0.10
                twist.angular.z = -0.2  # Gentler turn
            else:
                twist.linear.x = 0.10
                twist.angular.z = -0.3  # Sharper turn
            self.get_logger().info('Obstacle detected on left!', throttle_duration_sec=2)

        elif right_min < self.stop_distance:
            # Check if far_right and farfar_right offer a path
            if far_right_min > self.stop_distance and farfar_right_min > self.stop_distance:
                twist.linear.x = 0.10
                twist.angular.z = 0.2  # Gentler turn
            else:
                twist.linear.x = 0.10
                twist.angular.z = 0.3  # Sharper turn
            self.get_logger().info('Obstacle detected on right!', throttle_duration_sec=2)
        
        else:
            twist.linear.x = 0.2
            twist.angular.z = 0.0
            self.get_logger().info('No obstacles, driving forward', throttle_duration_sec=5)
    
    
        # Check if any obstacle is within the stop distance
        collision_detected = (
            far_right_min < self.collision_range or 
            far_left_min < self.collision_range or 
            right_min < self.collision_range or 
            left_min < self.collision_range or 
            farfar_right_min < self.collision_range or
            farfar_left_min < self.collision_range or
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
            
        self.detect_average_linear_speed(twist.linear.x)
        # Publish the twist command
        self.cmd_vel_pub.publish(twist)
    
    def detect_average_linear_speed(self, current_speed):
        if current_speed != self.last_speed:
            self.speed_sum += current_speed
            self.speed_index += 1
            self.last_speed = current_speed

            if self.speed_index > 0:
                self.average_linear_speed = self.speed_sum / self.speed_index
                

    def get_average_linear_speed(self):
        return self.average_linear_speed

    def detect_obstacle_collision(self):
        return self.collision_count



    def stop_robot(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)
        
        # Clean up I2C bus
        if hasattr(self, 'bus'):
            try:
                self.bus.close()
            except Exception as e:
                self.get_logger().error(f'Error closing I2C bus: {str(e)}')
                
        self.get_logger().info(f'Mission complete! Total victims rescued: {self.victims_picked}')

    def check_for_color(self):
    
        self.data = self.bus.read_i2c_block_data(0x44, 0x09, 6)
        self.red = (self.data[3] + self.data[2] / 256) * 1.3
        self.blue = (self.data[5] + self.data[4] / 256) * 2
        self.green = (self.data[1] + self.data[0] / 256) 

        # Define minimum threshold for color detection
        threshold = 75
    
        # Detect if we have a strong color reading
        is_red = self.red > threshold and self.red > self.green and self.red > self.blue
        is_green = self.green > threshold and self.green > self.red and self.green > self.blue
        is_blue = self.blue > threshold and self.blue > self.red and self.blue > self.green
    
        if is_green or is_blue:
            # Reset on green or blue
            self.pickup_index = 0
            self.in_pickup_state = False
            self.non_red_consecutive_count = 0
        
        elif is_red:
            # Red detected
            self.non_red_consecutive_count = 0
            if self.pickup_index >= 4 and not self.in_pickup_state:
                self.in_pickup_state = True
                # make it blink n times in the background of the program by setting the background true. 
                self.led.blink(on_time = 2, off_time = 0, n = 1, background = True)
                self.victims_picked += 1
                self.get_logger().info(f'Picked up victim. Total victims picked {self.victims_picked}')
            elif self.pickup_index >= 4 and self.in_pickup_state:
                self.get_logger().info('Victim already picked up')
            else:
                self.pickup_index += 1
        else:
             # No strong color detected - increment counter
            self.non_red_consecutive_count += 1
        
        # Reset pickup state after seeing no colors for a while
        if self.non_red_consecutive_count >= self.reset_threshold and self.in_pickup_state:
            self.get_logger().info('Resetting pickup state due to no colors detected')
            self.in_pickup_state = False
            self.pickup_index = 0
        
        print("rgb (%d, %d, %d)" % (self.red, self.green, self.blue))
            
