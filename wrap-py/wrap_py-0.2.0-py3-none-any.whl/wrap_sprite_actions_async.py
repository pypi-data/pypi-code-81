import time, threading
import wrap_py

sprite = wrap_py.sprite
event = wrap_py.event


def _reset_global_interfaces():
    global sprite, event
    sprite = wrap_py.sprite
    event = wrap_py.event


class wrap_sprite_actions_async():

    @staticmethod
    def _calc_values_by_percent(changing_kwargs: dict, percent):
        """
        updates changing_kwargs "val" key accordingly to percent

        :param changing_kwargs:
        :param percent:
        :return:
        """
        for arg_dict in changing_kwargs.values():
            arg_dict['val'] = arg_dict['start'] + (arg_dict['stop'] - arg_dict['start']) * percent

    @staticmethod
    def _get_changing_kwargs(changing_kwargs, key):
        """
        return flat dict {'param_name':param_value}

        :param changing_kwargs:
        :param use_stop_values:
        :return:
        """
        ch_kw = {name: int(d[key]) for (name, d) in changing_kwargs.items()}
        return ch_kw

    @staticmethod
    def _start_action(func, fixed_kwargs: dict, changing_kwargs: dict, time_ms: int, fps: int,
                            on_before_action=None, on_after_action=None,
                            on_finished=None,
                            wait_for_finish=False, timeout=None):
        """

        :param func:

        :param fixed_kwargs:
        :param changing_kwargs: { "argname1":{ start: int, stop: int} }
        :param time_ms:
        :param fps:
        :param on_before_action: func(**fixed_kwargs, **changing_kwargs_prepared)
        :param on_after_action: func(**fixed_kwargs, **changing_kwargs_prepared)
        :param on_finished: func(**fixed_kwargs, **changing_kwargs_prepared) - with last applied values
        :return:
        """

        def _make_call(func, fixed_kwargs, ch_kw):
            """Tries to make call. Returns True if calls could be continued. False otherwise"""
            # check we can do call
            if on_before_action is not None and not on_before_action(**fixed_kwargs, **ch_kw):
                return False

            # make call and save last real used values
            func(**fixed_kwargs, **ch_kw)
            # print(*ch_kw.values())

            # check if can continue
            if on_after_action is not None and not on_after_action(**fixed_kwargs, **ch_kw):
                return False

            return True

        def _finish_action(make_final_call):
            """Makes last call to func with stop values, if required.
            Stops notifications.
            Calls on_finish callback.
            """

            event.stop_listening(event_id)
            finished.set()

            if make_final_call:
                ch_kw = cls._get_changing_kwargs(changing_kwargs, "stop")
                _make_call(func, fixed_kwargs, ch_kw)

            if callable(on_finished):
                on_finished()

        def _action_callback(*args, **kwargs):
            nonlocal current_time

            if finished.is_set(): return

            # percent of time length passed
            current_time+=step_delay
            passed_percent = (current_time - start_time) / time_length

            # if all time passed - nothing to do here
            if passed_percent >= 1:
                _finish_action(True)
                return

            # update values
            cls._calc_values_by_percent(changing_kwargs, passed_percent)
            ch_kw = cls._get_changing_kwargs(changing_kwargs, "val")

            # make call
            can_continue = _make_call(func, fixed_kwargs, ch_kw)
            if not can_continue:
                _finish_action(False)

        start_time = time.time()
        time_length = time_ms / 1000
        end_time = start_time + time_length

        step_delay = 1 / fps
        current_time = start_time

        finished = threading.Event()

        event_id = event.register_event_handler(_action_callback, int(step_delay * 1000))

        if wait_for_finish:
            finished.wait(timeout)

    # @staticmethod
    # def _start_action(func, fixed_kwargs: dict, changing_kwargs: dict, time_ms: int, fps: int,
    #                   on_before_action=None, on_after_action=None, on_finished=None,
    #                   wait_for_finish=False, timeout=None):
    #
    #     # start in async mode and finish
    #     if not wait_for_finish:
    #         cls._start_action_async(func, fixed_kwargs, changing_kwargs, time_ms, fps,
    #                                 on_before_action, on_after_action, on_finished)
    #         return
    #
    #     # sync mode
    #
    #     def when_finished(*args, **kwargs):
    #         """Processes on_finish event.
    #             Calls original callback and unfroze this method from waiting.
    #         """
    #         if callable(on_finished):
    #             on_finished(*args, **kwargs)
    #
    #         ev.set()
    #
    #     ev = threading.Event()
    #
    #     cls._start_action_async(func, fixed_kwargs, changing_kwargs, time_ms, fps,
    #                             on_before_action, on_after_action, when_finished)
    #
    #     # wait for end of actions
    #     return ev.wait(timeout)

    @staticmethod
    def change_sprite_size(id, time_ms, width, height, on_before_action=None, on_after_action=None, on_finished=None,
                           wait_for_finish=False, timeout=None, fps=100):
        start_width, start_height = sprite.get_sprite_size(id)

        f = sprite.change_sprite_size
        fixkw = {"id": id}
        chkw = {
            "width": {"start": start_width, "stop": width},
            "height": {"start": start_height, "stop": height}
        }
        cls._start_action(f, fixkw, chkw, time_ms, fps,
                          on_before_action, on_after_action, on_finished,
                          wait_for_finish, timeout)

    @staticmethod
    def change_sprite_width(id, time_ms, width, on_before_action=None, on_after_action=None, on_finished=None,
                            wait_for_finish=False, timeout=None, fps=100):
        start_width = sprite.get_sprite_width(id)

        f = sprite.change_sprite_width
        fixkw = {"id": id}
        chkw = {
            "width": {"start": start_width, "stop": width}
        }
        cls._start_action(f, fixkw, chkw, time_ms, fps,
                          on_before_action, on_after_action, on_finished,
                          wait_for_finish, timeout)

    @staticmethod
    def change_sprite_height(id, time_ms, height, on_before_action=None, on_after_action=None, on_finished=None,
                             wait_for_finish=False, timeout=None, fps=100):
        start_height = sprite.get_sprite_height(id)

        f = sprite.change_sprite_height
        fixkw = {"id": id}
        chkw = {
            "height": {"start": start_height, "stop": height}
        }
        cls._start_action(
            f, fixkw, chkw, time_ms, fps,
            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def change_width_proportionally(id, time_ms, width, from_modified=False,
                                    on_before_action=None, on_after_action=None, on_finished=None,
                                    wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.change_width_proportionally,
            {"id": id,
             "from_modified": from_modified
             },

            {"width":
                 {"start": sprite.get_sprite_width(id), "stop": width}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def change_height_proportionally(id, time_ms, height, from_modified=False, on_before_action=None,
                                     on_after_action=None, on_finished=None,
                                     wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.change_height_proportionally,
            {"id": id,
             "from_modified": from_modified
             },

            {"height":
                 {"start": sprite.get_sprite_height(id), "stop": height}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def change_sprite_size_proc(id, time_ms, width, height, on_before_action=None, on_after_action=None,
                                on_finished=None,
                                wait_for_finish=False, timeout=None, fps=100):
        startw = sprite.get_sprite_width_proc(id)
        startw = startw if startw is not None else 100

        starth = sprite.get_sprite_height_proc(id)
        starth = starth if starth is not None else 100

        cls._start_action(
            sprite.change_sprite_size_proc,
            {"id": id},

            {"width":
                 {"start": startw, "stop": width},
             "height":
                 {"start": starth, "stop": height}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def change_sprite_width_proc(id, time_ms, width, on_before_action=None, on_after_action=None,
                                 on_finished=None,
                                 wait_for_finish=False, timeout=None, fps=100):
        startw = sprite.get_sprite_width_proc(id)
        startw = startw if startw is not None else 100

        cls._start_action(
            sprite.change_sprite_width_proc,
            {"id": id},

            {"width": {"start": startw, "stop": width}},
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def change_sprite_height_proc(id, time_ms, height, on_before_action=None, on_after_action=None,
                                  on_finished=None,
                                  wait_for_finish=False, timeout=None, fps=100):
        starth = sprite.get_sprite_height_proc(id)
        starth = starth if starth is not None else 100

        cls._start_action(
            sprite.change_sprite_height_proc,
            {"id": id},

            {"height":
                 {"start": starth, "stop": height}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def set_sprite_angle(id, time_ms, angle, on_before_action=None, on_after_action=None,
                         on_finished=None,
                         wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.set_sprite_angle,
            {"id": id},

            {"angle":
                 {"start": sprite.get_sprite_angle(id), "stop": angle}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def move_sprite_to(id, time_ms, x, y, on_before_action=None, on_after_action=None,
                       on_finished=None,
                       wait_for_finish=False, timeout=None, fps=100):
        start_x, start_y = sprite.get_sprite_pos(id)
        cls._start_action(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": x},
             "y": {"start": start_y, "stop": y}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def move_sprite_by(id, time_ms, dx, dy,
                       on_before_action=None, on_after_action=None, on_finished=None,
                       wait_for_finish=False, timeout=None, fps=100):
        start_x, start_y = sprite.get_sprite_pos(id)
        cls._start_action(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": start_x + dx},
             "y": {"start": start_y, "stop": start_y + dy}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def set_left_to(id, time_ms, left, on_before_action=None, on_after_action=None,
                    on_finished=None,
                    wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.set_left_to,
            {"id": id},

            {"left": {"start": sprite.get_left(id), "stop": left}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def set_right_to(id, time_ms, right, on_before_action=None, on_after_action=None,
                     on_finished=None,
                     wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.set_right_to,
            {"id": id},

            {"right": {"start": sprite.get_right(id), "stop": right}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def set_top_to(id, time_ms, top, on_before_action=None, on_after_action=None,
                   on_finished=None,
                   wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.set_top_to,
            {"id": id},

            {"top": {"start": sprite.get_top(id), "stop": top}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def set_bottom_to(id, time_ms, bottom, on_before_action=None, on_after_action=None,
                      on_finished=None,
                      wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.set_bottom_to,
            {"id": id},

            {"bottom": {"start": sprite.get_bottom(id), "stop": bottom}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def set_centerx_to(id, time_ms, centerx, on_before_action=None, on_after_action=None,
                       on_finished=None,
                       wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.set_centerx_to,
            {"id": id},

            {"centerx": {"start": sprite.get_centerx(id), "stop": centerx}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def set_centery_to(id, time_ms, centery, on_before_action=None, on_after_action=None,
                       on_finished=None,
                       wait_for_finish=False, timeout=None, fps=100):
        cls._start_action(
            sprite.set_centery_to,
            {"id": id},

            {"centery": {"start": sprite.get_centery(id), "stop": centery}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def move_sprite_at_angle(id, time_ms, angle, distance, on_before_action=None, on_after_action=None,
                             on_finished=None,
                             wait_for_finish=False, timeout=None, fps=100):
        start_x, start_y = sprite.get_sprite_pos(id)
        x, y = sprite.calc_point_by_angle_and_distance(id, angle, distance)
        cls._start_action(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": x},
             "y": {"start": start_y, "stop": y}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def move_sprite_to_angle(id, time_ms, distance, on_before_action=None, on_after_action=None,
                             on_finished=None,
                             wait_for_finish=False, timeout=None, fps=100):
        start_x, start_y = sprite.get_sprite_pos(id)
        angle = sprite.get_sprite_final_angle(id)
        x, y = sprite.calc_point_by_angle_and_distance(id, angle, distance)
        cls._start_action(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": x},
             "y": {"start": start_y, "stop": y}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def move_sprite_to_point(id, time_ms, x, y, distance, on_before_action=None, on_after_action=None,
                             on_finished=None,
                             wait_for_finish=False, timeout=None, fps=100):
        start_x, start_y = sprite.get_sprite_pos(id)
        angle = sprite.calc_angle_by_point(id, [x, y])
        if angle is None:
            return

        x, y = sprite.calc_point_by_angle_and_distance(id, angle, distance)
        cls._start_action(
            sprite.move_sprite_to,
            {"id": id},

            {"x": {"start": start_x, "stop": x},
             "y": {"start": start_y, "stop": y}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def rotate_to_angle(id, time_ms, angle_to_look_to, on_before_action=None, on_after_action=None,
                        on_finished=None,
                        wait_for_finish=False, timeout=None, fps=100):
        angle_modif = sprite.calc_angle_modification_by_angle(id, angle_to_look_to)

        cls._start_action(
            sprite.set_sprite_angle,
            {"id": id},

            {"angle":
                 {"start": sprite.get_sprite_angle(id), "stop": angle_modif}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def rotate_to_point(id, time_ms, x, y, on_before_action=None, on_after_action=None,
                        on_finished=None,
                        wait_for_finish=False, timeout=None, fps=100):
        angle_to_look_to = sprite.calc_angle_by_point(id, [x, y])
        if angle_to_look_to is None:
            return

        angle_modif = sprite.calc_angle_modification_by_angle(id, angle_to_look_to)

        cls._start_action(
            sprite.set_sprite_angle,
            {"id": id},

            {"angle":
                 {"start": sprite.get_sprite_angle(id), "stop": angle_modif}
             },
            time_ms, fps,

            on_before_action, on_after_action, on_finished,
            wait_for_finish, timeout)

    @staticmethod
    def wait(time_ms, fps=30):
        def a():return
        cls._start_action(a, {}, {}, time_ms, fps, wait_for_finish=True)


cls = wrap_sprite_actions_async
