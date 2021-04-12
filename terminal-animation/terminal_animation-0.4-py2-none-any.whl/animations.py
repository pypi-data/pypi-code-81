# -*- coding: utf-8 -*-
#
# Terminal based wait animations
#
# ------------------------------------------------


# imports
# -------
import sys
import threading
import time
from functools import wraps
import itertools
import cursor
import chalk

default_animation = ['    ','.   ','..  ','... ','....']

# animation objects
# -----------------
class Wait(object):
    """
    Class for managing wait animations.

    Args:
        animation (list): String list of the animation steps.
        speed (float): Number of seconds each cycle of animation.       
        color (str): Color to use for animation.

    Examples:
        >>> animation = Wait()
        >>> animation.start()
        >>> long_running_function()
        >>> animation.stop()
    """

    def __init__(self, animation=default_animation, speed=0.2, color=None, newLine=False):
        if not isinstance(animation, list):
            print("in here")
            return
        self._animation = animation
        self._newLine = newLine

        assert len(self._animation) > 0, 'Incorrect animation specified!'

        self.speed = speed

        if color is not None:
            if not hasattr(chalk, color):
                raise AssertionError('Color {} not supported. Please specify primary color supported by pychalk.'.format(color))
            self.color = getattr(chalk, color)
        else:
            self.color = lambda x: x

    #here is the animation
    def _animate(self):
        self._done = False
        cursor.hide() 
        for c in itertools.cycle(self._animation):
            if self._done:
                break
           
            print(self.color(c),end="",flush=True)
            
            for _ in range(len(c)):
                sys.stdout.write("\b")
            time.sleep(0.3)
        return

    def start(self):
        """
        Start animation thread.
        """
        self.thread = threading.Thread(target=self._animate)
        self.daemon = True
        self.thread.start()
        return

    def stop(self):
        """
        Stop animation thread.
        """
        time.sleep(self.speed)
        self._done = True
        sys.stdout.write('\r\033[K')
        sys.stdout.flush()
        if self._newLine:
                sys.stdout.write('\n')
        return


# decorators
# ----------
def wait(animation=default_animation, speed=0.2, color=None, newLine=False):
    """
    Decorator for adding wait animation to long running
    functions.

    Args:
        animation (list): String list of the animation steps.
        speed (float): Number of seconds each cycle of animation.
        newLine (boolean): Create a new line after the animation ended.

    Examples:
        >>> @animation.wait(['.','..','...','....'])
        >>> def long_running_function():
        >>>     ... 5 seconds later ...
        >>>     return
    """
    def decorator(func):
        func.animation = animation
        func.speed = speed
        func.color = color
        func.newLine = newLine

        @wraps(func)
        def wrapper(*args, **kwargs):
            animation = func.animation
            wait = Wait(animation=animation, speed=func.speed, color=color, newLine=newLine)
            cursor.hide() 
            wait.start()
            try:
                ret = func(*args, **kwargs)
            finally:
                wait.stop()
                cursor.show()
            return ret
        return wrapper
    return decorator