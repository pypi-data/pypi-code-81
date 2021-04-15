import threading, time


from wrap_py import wrap_base

from thread_signals import LateStartThread, get_thread_broker, interface_patcher, get_func_patcher

on_app_task_added_or_callback_tasks_done = threading.Event()
on_app_task_added_or_callback_tasks_done.set()

on_callback_task_added = threading.Event()
on_callback_task_added.clear()

on_callback_tasks_done = threading.Event()
on_callback_tasks_done.set()

#starter of App thread.
#run in main thread
def get_app_starter(callback_thread_id):

    # run in App thread
    def on_every_app_tick():

        time_limit_ms = 100
        # time_limit_ms = 1000000000
        time_start = time.time()

        app_broker = get_thread_broker()
        callback_broker = get_thread_broker(callback_thread_id)

        if not app_broker.empty():
            app_broker.run_all_tasks()

        while not on_callback_tasks_done.is_set():

            #update frame if running too long
            time_passed = (time.time() - time_start)*1000
            time_left = time_limit_ms - time_passed
            if time_left<0:
                wrap_base.app.do_frame(False)
                time_start = time.time()

            # wait for all callbacks done or new task added to app
            # but not longer then time limit passed
            res = on_app_task_added_or_callback_tasks_done.wait(time_left/1000)

            # on timeout
            if not res:
                continue
            else:
                # bug fixed. We only should clear event if it happened.
                # it is possible that both timeout and event happened.
                # Then we only should process either event or timeout. Not both.
                on_app_task_added_or_callback_tasks_done.clear()

            #run all tasks if exists
            if not app_broker.empty():
                app_broker.run_all_tasks()




    # run in App thread
    def app_starter():
        wrap_base.app.start(on_tick=on_every_app_tick)

    return app_starter

#starter of Callback thread
def callback_starter():
    broker = get_thread_broker()

    while True:

        #release thread until app frame done
        # after_frame_phase_event.wait()

        on_callback_task_added.wait()
        on_callback_task_added.clear()

        on_callback_tasks_done.clear()

        #run all tasks once. No more task expected until next frame finished
        broker.run_all_tasks(True)



def start_app_thread(interfaces_list, call_timeout=None):


    #start callback thread
    cb_thread = LateStartThread(target=callback_starter, name="Callback thread", daemon=True)
    get_thread_broker(cb_thread.ident, [on_callback_task_added], [on_app_task_added_or_callback_tasks_done, on_callback_tasks_done])
    cb_thread.start()

    #make callback patcher
    callback_patcher = get_func_patcher(cb_thread.ident, call_timeout, False)


    #make thread
    app_thread = LateStartThread(target=get_app_starter(cb_thread.ident), name="App thread")
    get_thread_broker(app_thread.ident, [on_app_task_added_or_callback_tasks_done])

    #patch interaces
    res = []
    for i in interfaces_list:
        new = interface_patcher(i, app_thread.ident, call_timeout)
        res.append(new)

    # start app work
    app_thread.start()

    return {
        "patched_interfaces": res,
        "callback_func_patcher" : callback_patcher
    }


def event_handler_hook(orig_func):
    return orig_func

