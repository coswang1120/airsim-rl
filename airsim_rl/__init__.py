from gym.envs.registration import register

register(
	id='airsim-rl-v0',
	entry_point='airsim_rl.envs:AirsimRLEnv',
)