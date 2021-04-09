import time
from typing import Optional, Tuple

import numpy as np
import tensorflow as tf
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from skimage.filters import gaussian
from skimage.transform import resize


def make_saliency_map(input_img,
                      gradients,
                      convert_to_uint8: bool = True,
                      resize_dims: Optional[Tuple] = None):
    assert input_img.shape == gradients.shape
    gradients = tf.abs(gradients)
    # gradients = tf.nn.relu(gradients)
    gradients = tf.math.divide(tf.subtract(gradients,
                                           tf.reduce_min(gradients)),
                               tf.subtract(tf.reduce_max(gradients),
                                           tf.reduce_min(gradients)))

    t = tf.math.sqrt(tf.add(tf.math.reduce_std(gradients),
                            tf.reduce_mean(gradients)))
    gradients = tf.multiply(
        gradients,
        tf.cast(gradients > t, dtype=tf.float32)
    )
    gradients = gaussian(gradients, sigma=0.5 + t.numpy())

    saliency_map = tf.stack([gradients, input_img, input_img], axis=-1)

    if convert_to_uint8:
        saliency_map = tf.cast(tf.multiply(saliency_map, 255), dtype=tf.uint8)

    if resize_dims is not None:
        saliency_map = resize(saliency_map,
                              output_shape=[resize_dims[1], resize_dims[0], 3],
                              preserve_range=True)
    return saliency_map


def make_q_values_plot(q_values,
                       actions_names,
                       plt_objs,
                       resize_dims=None):
    fig, axis, canvas = tuple(map(plt_objs.get, ("fig", "axis", "canvas")))

    axis.clear()
    bar_list = axis.bar(x=actions_names, height=q_values)
    bar_list[np.argmax(q_values)].set_color("orange")

    canvas.draw()
    fig_width, fig_height = fig.get_size_inches() * fig.get_dpi()

    q_values_plot = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    q_values_plot = q_values_plot.reshape(int(fig_height), int(fig_width), 3)

    if resize_dims is not None:
        q_values_plot = resize(q_values_plot,
                               output_shape=[resize_dims[1], resize_dims[0], 3],
                               preserve_range=True)
    return q_values_plot


def visualize_policy(policy,
                     env,
                     num_episodes: int = 1,
                     fps: int = 60,
                     epsilon_greedy: float = 0):
    for episode in range(num_episodes):
        obs = env.reset().observation
        episode_reward = 0.0
        done = False

        while not done:
            # Rendering:
            env.render(mode="human")
            time.sleep(1 / fps)

            # Random action:
            if np.random.uniform(low=0, high=1) < epsilon_greedy:
                action = np.random.randint(low=0,
                                           high=env.action_spec().num_values)
            # Greedy policy:
            else:
                q_values = policy(tf.expand_dims(obs, axis=0))[0]
                action = tf.argmax(q_values).numpy()

            # Updating environment:
            timestep_obj = env.step(action)
            obs = timestep_obj.observation

            episode_reward += timestep_obj.reward
            done = timestep_obj.last()

        print(f"Episode reward: {episode_reward:.2f}")
