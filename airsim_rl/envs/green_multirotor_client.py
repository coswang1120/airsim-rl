import setup_path 
import airsim
from airsim import *
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

	def _take_action(self, action, mode):
		"""
		Args:
			action: (vx, vy, yaw_rate)
			mode: "FO" or "MD"
		Returns: collision true/false

		"""
		vel_x = action[0]
		vel_y = action[1]
		cur_pitch, cur_roll, cur_yaw  = airsim.to_eularian_angles(self.simGetVehiclePose().orientation)
		if mode == "FO":
			self.moveByVelocityAsync((vel_x)*math.cos(cur_yaw)-(vel_y)*math.sin(cur_yaw), (vel_x)*math.sin(cur_yaw)+(vel_y)*math.cos(cur_yaw), 0, 0.01,drivetrain = airsim.DrivetrainType.ForwardOnly, yaw_mode=airsim.YawMode(False)).join()
			self.hoverAsync().join()
		else:
			"""cur_yaw  should be replaced """
			self.moveByVelocityAsync((vel_x)*math.cos(cur_yaw)-(vel_y)*math.sin(cur_yaw), (vel_x)*math.sin(cur_yaw)+(vel_y)*math.cos(cur_yaw), 0, 0.01,drivetrain = airsim.DrivetrainType.MaxDegreeOfFreedom, yaw_mode=airsim.YawMode(True, cur_yaw)).join()
			self.hoverAsync().join()
		return self.simGetCollisionInfo().has_collided

	def _get_collision_info(self):
		return self.simGetCollisionInfo().has_collided

	def _get_state(self):
		"""
		Returns:
			observation: agent's observation of the current environment (depth image)
		"""
		responses = self.simGetImages([ImageRequest(0, ImageType.DepthPerspective, True, False)])
		img1d = np.array(responses[0].image_data_float, dtype=np.float)
		img1d = 255/np.maximum(np.ones(img1d.size), img1d)
		img2d = np.reshape(img1d, (responses[0].height, responses[0].width))
		
	   


		image = np.invert(np.array(Image.fromarray(img2d.astype(np.uint8), mode='L')))
		  
		factor = 10
		maxIntensity = 255.0 # depends on dtype of image data
		
		# Decrease intensity such that dark pixels become much darker, bright pixels become slightly dark 
		newImage1 = (maxIntensity)*(image/maxIntensity)**factor
		newImage1 = array(newImage1,dtype=uint8)
		
		
		small = cv2.resize(newImage1, (0,0), fx=0.39, fy=0.38)
		cut = small[20:40,:]
		img = Image.fromarray(cut,'L')
		# img.show()
		# print(image.shape, cut.shape)
		
		"""info_section = np.zeros((10,cut.shape[1]),dtype=np.uint8) + 255
		info_section[9,:] = 0
		
		line = np.int((((track - -180) * (100 - 0)) / (180 - -180)) + 0)
		
		if line != (0 or 100):
			info_section[:,line-1:line+2]  = 0
		elif line == 0:
			info_section[:,0:3]  = 0
		elif line == 100:
			info_section[:,info_section.shape[1]-3:info_section.shape[1]]  = 0
			
		total = np.concatenate((info_section, cut), axis=0)"""
		
		return cut

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
		state = self.simGetGroundTruthKinematics()
		pitch, roll, yaw  = airsim.to_eularian_angles(self.simGetVehiclePose().orientation)
		#yaw = math.degrees(yaw) 
		ret = {
			STATE_STRINGS[VEL_X]: state['linear_velocity']['x_val'],
			STATE_STRINGS[VEL_Y]: state['linear_velocity']['y_val'],
			STATE_STRINGS[VEL_Z]: state['linear_velocity']['z_val'],
			STATE_STRINGS[ACC_X]: state['linear_acceleration']['x_val'],
			STATE_STRINGS[ACC_Y]: state['linear_acceleration']['y_val'],
			STATE_STRINGS[ACC_Z]: state['linear_acceleration']['z_val'],
			STATE_STRINGS[ROLL]: roll,
			STATE_STRINGS[PITCH]: pitch,
			STATE_STRINGS[YAW]: yaw
		}
		return ret

	def _get_position(self):
		state = self.getMultirotorState()
		pos_x = state.kinematics_estimated.position.x_val
		pos_y = state.kinematics_estimated.position.y_val
		position = (pos_x, pos_y)
		return position
