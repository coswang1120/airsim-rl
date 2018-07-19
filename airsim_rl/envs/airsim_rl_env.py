import gym
from gym import error, spaces, utils
from gym.utils import seeding
from airsim_rl.envs.green_multirotor_client import *

from math import radians, sin, cos
import logging
import numpy as np

logger = logging.getLogger(__name__)

VEL_MAX = 10.0
YAW_RATE_MAX = 10.0

# note: maybe we should use gym.GoalEnv instead?
class AirsimRLEnv(gym.Env):

	def __init__(self):

		self.mt_client = GreenMultirotorClient()

		self.goal_pos = (109.106, -30.296)
		self.cur_pos = (0, 0)
		self.reward_sum = 0
		self.collided = False

		self.distance_before = 0

		"""
		observation_space: a depth image (30, 100)
		"""
		self.observation_space = spaces.Box(low=0, high=255, shape=(30, 100))

		"""
		action_space: (vel_x, vel_y)
		"""
		# self.action_space = spaces.Tuple((spaces.Box(low=-VEL_MAX, high=VEL_MAX, shape=(1,)), spaces.Box(low=-VEL_MAX, high=VEL_MAX, shape=(1,)), spaces.Box(low=-VEL_MAX, high=VEL_MAX, shape=(1,))))
		self.action_space = spaces.Discrete(11)


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

		reward = self.compute_reward(self.cur_pos)

		self.reward_sum = self.reward_sum + reward

		if self.reward_sum < -100 or self.collided:
			done = True
		else:
			done = False

		self.state = self.mt_client._get_state()
		info = self.mt_client._get_sensor_info()


		print(self.reward_sum)

		return self.state, reward, done, info

	def _take_action(self, action):
		assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

		self.mt_client._take_action(ACTION_LOOKUP[action], "FO")



	def compute_reward(self, cur_pos):
		distance_now = np.sqrt(np.power((self.goal_pos[0]-cur_pos[0]),2) + np.power((self.goal_pos[1]-cur_pos[1]),2))
        
        

		r = -1

		if self.collided == True:
			r = r + -100.0
		elif self.get_distance_from_goal() < 3:
			r = r + 100.0

		r = r + self.distance_before - distance_now

		self.distance_before = distance_now
		
		return r

	def _reset(self):
		"""Resets the state of the environment and returns an initial observation.
		Returns: observation (object): the initial observation of the
			space.
		"""
		self.mt_client._reset()

		self.reward_sum = 0

		self.state = self.mt_client._get_state()
		self.collided = False
		self.cur_pos = (0, 0)

		return self.state

	def render(self, mode, close):
		pass

	def _seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]

	def get_distance_from_goal(self):
		return np.sqrt(np.power((self.goal_pos[0]-self.cur_pos[0]),2) + np.power((self.goal_pos[1]-self.cur_pos[1]),2))


ACTION_LOOKUP = {
	0: (cos(radians(15)), sin(radians(15))),
	1: (cos(radians(30)), sin(radians(30))),
	2: (cos(radians(45)), sin(radians(45))),
	3: (cos(radians(60)), sin(radians(60))),
	4: (cos(radians(75)), sin(radians(75))),
	5: (cos(radians(0)), sin(radians(0))),
	6: (cos(radians(-15)), sin(radians(-15))),
	7: (cos(radians(-30)), sin(radians(-30))),
	8: (cos(radians(-45)), sin(radians(-45))),
	9: (cos(radians(-60)), sin(radians(-60))),
	10: (cos(radians(-75)), sin(radians(-75)))
}