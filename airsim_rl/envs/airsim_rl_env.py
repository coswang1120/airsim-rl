import gym
from gym import error, spaces, utils
from gym.utils import seeding


import logging
logger = logging.getLogger(__name__)

VEL_MAX = 10

# note: maybe we should use gym.GoalEnv instead?
class AirsimRLEnv(gym.Env):

	def __init__(self):

		mt_client = GreenMultirotorClient()


		"""
		observation_space: a depth image (30, 100)
		"""
		self.observation_space = spaces.Box(low=0, high=255, shape=(30, 100))

		"""
		action_space: (vel_x, vel_y)
		"""
		self.action_space = spaces.Tuple(spaces.Box(low=-VEL_MAX, high=VEL_MAX), spaces.Box(low=-VEL_MAX, high=VEL_MAX))


	# note: should I underscore the method name? What does it mean?
	def step(self, action):
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
		self._take_action(action)

		reward = self.compute_reward()
		ob = self.mt_client.get_state()
		#done = 



		pass

	def _take_action(self, action):
		assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

		self.mt_client.take_actiontake_action



	def compute_reward(self, achieved_goal, desired_goal, info):
		"""
		 Compute the step reward. This externalizes the reward function and makes
        it dependent on an a desired goal and the one that was achieved. If you wish to include
        additional rewards that are independent of the goal, you can include the necessary values
        to derive it in info and compute it accordingly.

        Args:
            achieved_goal (object): the goal that was achieved during execution
            desired_goal (object): the desired goal that we asked the agent to attempt to achieve
            info (dict): an info dictionary with additional information
            
        Returns:
            float: The reward that corresponds to the provided achieved goal w.r.t. to the desired
            goal. Note that the following should always hold true:
                ob, reward, done, info = env.step()

                assert reward == env.compute_reward(ob['achieved_goal'], ob['goal'], info)
        """
		pass

	def reset(self):
		"""Resets the state of the environment and returns an initial observation.
        Returns: observation (object): the initial observation of the
            space.
        """
		ob = self.mt_client.reset()

		return ob

	def render(self, mode, close):
		pass
