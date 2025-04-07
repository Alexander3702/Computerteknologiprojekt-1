#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
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
# Authors: Ryan Shim, Gilbert

import rclpy
import time 
from turtlebot3_example.turtlebot3_obstacle_detection.turtlebot3_obstacle_detection \
    import Turtlebot3ObstacleDetection



def main(args=None):
    rclpy.init(args=args)
    turtlebot3_obstacle_detection = Turtlebot3ObstacleDetection()

     #setting starttime and endtime to make the robot run for specific amount of time. 
    start_time = time.time()
    end_time = start_time + 30.0

    #running the robot for 30 seconds. We're updating the robot's position every 0.1 seconds.
    while time.time() < end_time:
        rclpy.spin_once(turtlebot3_obstacle_detection, timeout_sec = 0.1)


   # Print final collision count if needed
    turtlebot3_obstacle_detection.get_logger().info(
        f'Total collisions detected: {turtlebot3_obstacle_detection.collision_count}'
    )

    turtlebot3_obstacle_detection.stop_robot()

    

    turtlebot3_obstacle_detection.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
