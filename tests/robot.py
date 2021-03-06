# Copyright (c) 2021 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

"""Test script to run a simple stance command.
"""
from __future__ import print_function
import argparse
import sys
import traceback
import time

import bosdyn.client
import bosdyn.client.estop
import bosdyn.client.lease
import bosdyn.client.util

from bosdyn.client import frame_helpers
from bosdyn.client import math_helpers
from bosdyn.client import robot_command
from bosdyn.client.robot_command import RobotCommandClient, RobotCommandBuilder
from bosdyn.client.robot_state import RobotStateClient


def run(robot, x_offset, y_offset):
    """Testing API Stance
    This example will cause the robot to power on, stand and reposition its feet (Stance) at the
    location it's already standing at.
    * Use sw-estop running on tablet/python etc.
    * Have ~1m of free space all around the robot
    * Ctrl-C to exit and return lease.
    """

    robot.time_sync.wait_for_sync()

    # Acquire lease
    lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
    lease = lease_client.acquire()

    try:
        with bosdyn.client.lease.LeaseKeepAlive(lease_client):
            command_client = robot.ensure_client(RobotCommandClient.default_service_name)
            robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)
            state = robot_state_client.get_robot_state()

            # This example ues the current body position, but you can specify any position.
            # A common use is to specify it relative to something you know, like a fiducial.
            vo_T_body = frame_helpers.get_se2_a_tform_b(state.kinematic_state.transforms_snapshot,
                                                        frame_helpers.VISION_FRAME_NAME,
                                                        frame_helpers.GRAV_ALIGNED_BODY_FRAME_NAME)

            # Power On
            robot.power_on()
            assert robot.is_powered_on(), "Robot power on failed."

            # Stand
            robot_command.blocking_stand(command_client)

            #### Example stance offsets from body position. ####
            if not 0.2 <= abs(x_offset) <= 0.5:
                print("Invalid x-offset value. Please pass a value between 0.2 and 0.5")
                sys.exit(1)
            if not 0.1 <= abs(y_offset) <= 0.4:
                print("Invalid y-offset value. Please pass a value between 0.1 and 0.4")
                sys.exit(1)

            pos_fl_rt_vision = vo_T_body * math_helpers.SE2Pose(x_offset, y_offset, 0)
            pos_fr_rt_vision = vo_T_body * math_helpers.SE2Pose(x_offset, -y_offset, 0)
            pos_hl_rt_vision = vo_T_body * math_helpers.SE2Pose(-x_offset, y_offset, 0)
            pos_hr_rt_vision = vo_T_body * math_helpers.SE2Pose(-x_offset, -y_offset, 0)

            stance_cmd = RobotCommandBuilder.stance_command(
                frame_helpers.VISION_FRAME_NAME, pos_fl_rt_vision.position,
                pos_fr_rt_vision.position, pos_hl_rt_vision.position, pos_hr_rt_vision.position)

            print("After stance adjustment, press Ctrl-C to sit Spot and turn off motors.")

            while True:
                # Update end time
                stance_cmd.synchronized_command.mobility_command.stance_request.end_time.CopyFrom(
                    robot.time_sync.robot_timestamp_from_local_secs(time.time() + 5))

                # Send the command
                command_client.robot_command(stance_cmd)

                time.sleep(1)

    finally:
        lease_client.return_lease(lease)