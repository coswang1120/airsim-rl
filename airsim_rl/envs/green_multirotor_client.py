import setup_path 
import airsim
from airsim import MultirotorClient
import sys

import numpy as np
import os
import tempfile
import pprint


import time
import math
import cv2
from pylab import array, arange, uint8 
from PIL import Image
import eventlet
from eventlet import Timeout
import multiprocessing as mp
# ToDo: need to import MultirotorClient


NUM_SENSOR_STATES = 9
VEL_X, VEL_Y, VEL_Z, ACC_X, ACC_Y, ACC_Z, ROLL, PITCH, YAW = range(NUM_SENSOR_STATES)
STATE_STRINGS = {
	VEL_X: "Vel_X",
	VEL_Y: "Vel_Y",
	VEL_Z: "Vel_Z",
	ACC_X: "Acc_X",
	ACC_Y: "Acc_Y",
	ACC_Z: "Acc_Z",
	ROLL: "Roll",
	PITCH: "Pitch",
	YAW: "Yaw"
}

class GreenMultirotorClient(MultirotorClient):

	def __init__(self):
		self.img1 = None
		self.img2 = None
        MultirotorClient.__init__(self)
        MultirotorClient.confirmConnection(self)
        self.enableApiControl(True)
        self.armDisarm(True)

	def _take_off(self):
		self.takeoffAsync(timeout_sec = 4).join()
        self.moveToPositionAsync(0,0,-1.3,2).join()
        self.hoverAsync().join()

	def _take_action(self, action):
		"""
		Returns: collision true/false
		"""
		vel_x = action[0]
		vel_y = action[1]
		yaw = action[2]
		self.moveByVelocityAsync((vel_x), (vel_y), 0, 0.01,drivetrain = airsim.DrivetrainType.MaxDegreeOfFreedom, yaw_mode=airsim.YawMode(True, yaw)).join()
		self.hoverAsync().join()
		return self.simGetCollisionInfo().has_collided

	def _get_state(self):
		"""
		Returns:
			observation: agent's observation of the current environment (depth image)
		"""
		pass

	def _reset(self):
		self.armDisarm(False)
		self.reset()
		self.enableApiControl(False)
		self.armDisarm(True)
		self.enableApiControl(True)
		self._take_off()
		return self._get_state()

	def _get_sensor_info(self):
		"""
		Returns:
			sensor info: dictionary which contains sensor information (refer to STATE_STRING for key names)
		"""
		state = {
			STATE_STRINGS[VEL_X]: 
		}
		return state

	def _get_position(self):
		state = self.getMultirotorState()
		pos_x = state.kinematics_estimated.position.x_val
		pos_y = state.kinematics_estimated.position.y_val
		position = (pos_x, pos_y)
		return position
