import time
import os
from swissarmykit.lib.core import Singleton

@Singleton
class Timer:

    def __init__(self, total=0, file_name='timer_', check_point=None):
        self.log = None
        try:
            if 'swissarmykit_conf' in globals():
                from swissarmykit.utils.loggerutils import LoggerUtils
                self.log = LoggerUtils.instance(file_name)  # type: LoggerUtils
        except ImportError:
            pass

        self.t0 = time.time()
        self.cache = None
        self.prev_t0 = self.t0
        self.title = None
        self.total_task = total
        self.remain_task = total
        self.percentage = ''

        self.msg = ''
        self._id = 'pid_timer ' + str(os.getpid())
        self.check_point = check_point if check_point else 1000

    def reset(self, total=0):
        self.t0 = time.time()
        self.total_task = total
        self.remain_task = total

    def check(self, item=None, idx=None):
        self.remain_task -= 1
        # print('.', end='', flush=True)

        if self.remain_task % self.check_point == 0:
            t1 = time.time()
            time_spent = (t1 - self.t0) / 60

            extra_msg = ''
            if item:
                extra_msg = ' - (id: %s url: %s)' % (str(item.id), item.url)
            if idx:
                extra_msg += ' Idx: %d' % idx

            if self.total_task:
                done_task = self.total_task - self.remain_task
                time_eta = self.remain_task * time_spent / (done_task + 1) # Avoid divide by 0

                self.percentage = round(done_task * 100 / self.total_task)
                self.msg = "     {:4d}% tasks - eta: {} - et: {} - remain: {}  {}".format(
                    self.percentage, self.convert_mm_2_hh_mm(time_eta), self.convert_mm_2_hh_mm(time_spent), self.remain_task, extra_msg)
            else:
                self.msg = "     et: {} - total: {} tasks. {}".format(self.convert_mm_2_hh_mm(time_spent), abs(self.remain_task), extra_msg)

            self._log_info(self.msg)

        if self.remain_task % 10000 and self.log and self.cache:
            self.get_cache().save_attr(self._id, attr={
                'value': {'percentage': self.percentage, 'message': self.msg, 'log_file': self.log.get_log_name(), 'tail': self.log.get_tail_log(),
                          'total_task': self.total_task, 'remain_task': self.remain_task}})

    def get_cache(self):
        if not self.cache:
            if 'app' in globals():
                self.cache = app.get_process_tmp()
            else:
                print('app not define in definitions_prod')
        return self.cache


    def done(self):
        self.spent()

    def start(self, title=None):
        self.title = title
        self.prev_t0 = time.time()

    def spent(self):
        t1 = time.time()
        time_spent = (t1 - self.prev_t0) / 60
        if self.title:
            self._log_info("- {}. et: {}m.".format(self.title, round(time_spent, 2)))
            self.title = None
        else:
            self._log_info("et: {}m.".format(round(time_spent, 2)))

    def convert_mm_2_hh_mm(self, minutes):
        return "%dh %02dm" % (round(minutes / 60), minutes % 60)

    def _log_info(self, message):
        if self.log:
            self.log.info(message)
        else:
            print(message)

if __name__ == '__main__':
    timer = Timer.instance()
    for i in range(2001):
        timer.check()
