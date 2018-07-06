
# ToDo: need to import MultirotorClient

NUM_SENSOR_STATE = 9
VEL_X, VEL_Y, VEL_Z, ACC_X, ACC_Y, ACC_Z, ROLL, PITCH, YAW = range(NUM_SENSOR_STATE)

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
		self.moveByVelocityAsync((vel_x), (vel_y), 0, 0.1,drivetrain = airsim.DrivetrainType.MaxDegreeOfFreedom, yaw_mode=airsim.YawMode(True, yaw)).join()
		self.hoverAsync().join()

	def _get_state(self):
		"""
		Returns:
			observation: agent's observation of the current environment
						 [[vel_x, vel_y, vel_z, acc_x, acc_y, acc_z, roll, pitch, yaw], depth_image]
		"""
		pass

	def _reset(self):
		self.armDisarm(False)
		self.reset()
		self.enableApiControl(False)
		self.armDisarm(True)
		self.enableApiControl(True)
		self.moveToPositionAsync(0,0,0)
		self.hoverAsync().join()