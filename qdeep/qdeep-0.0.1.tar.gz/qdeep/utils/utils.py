""" Implementation of useful functionalities. """

import os
import re
from typing import Callable, Optional
from pathlib import Path

import numpy as np
import tensorflow as tf
import sonnet as snt


def format_eta(eta_secs: int) -> str:
    m, s = divmod(int(eta_secs), 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}"


def save_module(module: snt.Module, file_prefix: str):
    checkpoint = tf.train.Checkpoint(root=module)
    return checkpoint.write(file_prefix=file_prefix)


def restore_module(base_module: snt.Module, save_path: str):
    checkpoint = tf.train.Checkpoint(root=base_module)
    return checkpoint.read(save_path=save_path)


def find_best_policy(policies_folder: str,
                     make_env: Callable,
                     make_dqn: Callable,
                     clean_and_sort_files: bool = False,
                     new_files_prefix: Optional[str] = None,
                     keep_n_best: int = 5,
                     keep_policy_min_diff: float = 100):
    # Preparing ray:
    try:
        import ray
    except ModuleNotFoundError as ex:
        raise ModuleNotFoundError(
            "In order to use this function, you must have `ray` installed. You "
            "can install it with the command:\n\t\t$ pip install ray"
        ) from ex
    ray.init(ignore_reinit_error=True)

    @ray.remote
    def _eval_policy_ray(policy_path):
        env = make_env()
        policy = make_dqn(env.action_spec().num_values)
        restore_module(base_module=policy, save_path=policy_path)

        obs = env.reset().observation
        policy_reward = 0
        done = False
        while not done:
            q_values = policy(tf.expand_dims(obs, axis=0))[0]
            action = tf.argmax(q_values)

            timestep_obj = env.step(action)
            obs = timestep_obj.observation

            policy_reward += timestep_obj.reward
            done = timestep_obj.last()

        return policy_reward

    # Getting files names:
    files = []
    for i, fn in enumerate(sorted(Path(policies_folder).iterdir(),
                                  key=os.path.getmtime)):
        if i % 2 == 0:
            files.append(re.search("^[^.]*", str(fn))[0])

    # Searching:
    futures = [_eval_policy_ray.remote(fn) for fn in files]
    rewards = ray.get(futures)
    best_policy_path = files[np.argmax(rewards)]

    # Sorting
    policies_rewards = {fn: reward for fn, reward in zip(files, rewards)}
    policies_rewards = {k: v for k, v in sorted(policies_rewards.items(),
                                                key=lambda item: item[1])}

    # Cleaning and sorting files:
    if clean_and_sort_files:
        SUFFIX1 = ".index"
        SUFFIX2 = ".data-00000-of-00001"
        assert new_files_prefix is not None

        new_dict = {}
        last_reward = None
        for i, fn in enumerate(reversed(policies_rewards.keys())):
            reward = policies_rewards[fn]
            if (last_reward is None
                    or (last_reward - reward) >= keep_policy_min_diff
                        or i < keep_n_best):
                episode = re.search("(episode)[0-9]+", fn)
                episode = f"_ep{episode[0][7:]}" if episode is not None else ""

                new_fn = os.path.join(
                    policies_folder,
                    new_files_prefix + f"_r{int(reward)}" + episode)

                os.rename(fn + SUFFIX1, new_fn + SUFFIX1)
                os.rename(fn + SUFFIX2, new_fn + SUFFIX2)

                last_reward = reward
                new_dict[new_fn] = reward
            else:
                os.remove(fn + SUFFIX1)
                os.remove(fn + SUFFIX2)

        policies_rewards = {k: v for k, v in sorted(new_dict.items(),
                                                    key=lambda item: item[1])}
        best_policy_path = list(policies_rewards.keys())[-1]

    return best_policy_path, policies_rewards
