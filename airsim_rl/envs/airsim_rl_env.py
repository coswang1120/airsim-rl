import gym
from gym import error, spaces, utils
from gym.utils import seeding
from airsim_rl.envs.green_multirotor_client import *


import logging
logger = logging.getLogger(__name__)

VEL_MAX = 10
YAW_RATE_MAX = 10

# note: maybe we should use gym.GoalEnv instead?
class AirsimRLEnv(gym.Env):

	def __init__(self):

		self.mt_client = GreenMultirotorClient()

		self.goal_pos = (0, 0)
		self.cur_pos = (0, 0)
		self.reward_sum = 0
		self.collided = False

		"""
		observation_space: a depth image (30, 100)
		"""
		self.observation_space = spaces.Box(low=0, high=255, shape=(30, 100))

		"""
		action_space: (vel_x, vel_y)
		"""
		self.action_space = spaces.Tuple(spaces.Box(low=-VEL_MAX, high=VEL_MAX), spaces.Box(low=-VEL_MAX, high=VEL_MAX), spaces.Box(low=-VEL_MAX, high=VEL_MAX))


	# note: should I underscore the method name? What does it mean?
	def _step(self, action):
		"""
		 Run one timestep of the environment's dynamics. When end of
		episode is reached, you are responsible for calling `reset()`
		to reset this environment's state.
		Accepts an action and returns a tuple (observation, reward, done, info).

		Args:
			action (object): an action provided by the environment
		Returns:
			observation (object): agent's observation of the current environment
			reward (float) : amount of reward returned after previous action
			done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
			info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
		"""
		self.collided = self._take_action(action)

		self.cur_pos = self.mt_client._get_position()

		reward = self.compute_reward()

		reward_sum = reward_sum + reward

		if reward_sum < -100 or self.collided:
			done = True

		self.state = self.mt_client._get_state()
		info = mt_client._get_sensor_info()


		return self.state, reward, done, info

	def _take_action(self, action):
		assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

		self.mt_client._take_action(action)



	def compute_reward():

		r = -1

		if self.collided == True:
			r = r + -100.0
		elif self.get_distance_from_goal() < 3:
			r = r + 100.0

		return r

	def _reset(self):
		"""Resets the state of the environment and returns an initial observation.
		Returns: observation (object): the initial observation of the
			space.
		"""
		self.mt_client._reset()

		reward_sum = 0

		self.state = self.mt_client._get_state()
		self.collided = False
		self.cur_pos = (0, 0)

		return self.state

	def render(self, mode, close):
		pass

	def get_distance_from_goal():
		return np.sqrt(np.power((self.goal_pos[0]-self.cur_pos[0]),2) + np.power((self.goal_pos[1]-self.cur_pos[1]),2))
