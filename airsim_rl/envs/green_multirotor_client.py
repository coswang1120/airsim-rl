
# ToDo: need to import MultirotorClient

NUM_SENSOR_STATE = 9
VEL_X, VEL_Y, VEL_Z, ACC_X, ACC_Y, ACC_Z, ROLL, PITCH, YAW = range(NUM_SENSOR_STATE)

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
			observation: agent's observation of the current environment
						 [[vel_x, vel_y, vel_z, acc_x, acc_y, acc_z, roll, pitch, yaw], depth_image]
		"""
		pass

	def reset(self):
		"""
		Resets the state of the environment and returns an initial observation.

		Returns:
			observation: the initial observation
		"""
		pass