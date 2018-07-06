
# ToDo: need to import MultirotorClient


NUM_SENSOR_STATEs = 9
VEL_X, VEL_Y, VEL_Z, ACC_X, ACC_Y, ACC_Z, ROLL, PITCH, YAW = range(NUM_SENSOR_STATE)
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
		pass

	def take_action(self, action):
		"""
		Args:
			action: (vel_x, vel_y, yaw_rate)

		Returns:
			collided: True if collision occured

		"""
		pass

	def get_state(self):
		"""
		Returns:
			observation: agent's observation of the current environment (depth image)
		"""
		pass

	def get_sensor_info(self):
		"""
		Returns:
			sensor info: dictionary which contains sensor information (refer to STATE_STRING for key names)
		"""

	def reset(self):
		"""
		Resets the state of the environment and returns an initial observation.

		Returns:
			observation: the initial observation
		"""
		pass