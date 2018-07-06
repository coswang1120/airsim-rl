
# ToDo: need to import MultirotorClient

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