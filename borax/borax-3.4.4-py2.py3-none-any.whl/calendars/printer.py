# coding=utf-8
import calendar
from borax.calendars import LunarDate

__all__ = ['LCalendarPrinter']


class LCalendarPrinter(calendar.TextCalendar):
    def formatday(self, day, weekday, width):
        """
        Returns a formatted day.
        """
        if day == 0:
            s = ''
        else:
            s = '%2i' % day  # right-align single-digit days
        return s.center(width)

    def formatweek(self, theweek, width):
        """
        Returns a single week in a string (no newline).
        """
        return ' '.join(self.formatday(d, wd, width) for (d, wd) in theweek)

    def format_lunar_week(self, theyear, themonth, theweek, width):
        def _fmt_lunar_day(_day, _weekday, _with):
            if _day == 0:
                s = ''
            else:
                ld = LunarDate.from_solar_date(theyear, themonth, _day)
                s = ld.cn_day_calendar
            return s.center(width)

        return ' '.join(_fmt_lunar_day(d, wd, width) for (d, wd) in theweek)

    def formatmonth(self, theyear, themonth, w=0, l=0):
        """
        Return a month's calendar string (multi-line).
        """
        w = max(2, w)  # 2 -> 4
        en_w = w * 2
        l = max(1, l)
        s = self.formatmonthname(theyear, themonth, 7 * (w + 1) - 1)
        s = s.rstrip()
        s += '\n' * l
        s += self.formatweekheader(w).rstrip()
        s += '\n' * l
        for week in self.monthdays2calendar(theyear, themonth):
            s += self.formatweek(week, en_w).rstrip()
            s += '\n' * l
            s += self.format_lunar_week(theyear, themonth, week, w).rstrip()
            s += '\n' * l
        return s

    def formatyear(self, theyear, w=2, l=1, c=6, m=3):
        """
        Returns a year's calendar as a multi-line string.
        """
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append
        a(repr(theyear).center(colwidth * m + c * (m - 1)).rstrip())
        a('\n' * l)
        header = self.formatweekheader(w)
        for (i, row) in enumerate(self.yeardays2calendar(theyear, m)):
            # months in this row
            months = range(m * i + 1, min(m * (i + 1) + 1, 13))
            a('\n' * l)
            names = (self.formatmonthname(theyear, k, colwidth, False)
                     for k in months)
            a(calendar.formatstring(names, colwidth, c).rstrip())
            a('\n' * l)
            headers = (header for k in months)
            a(calendar.formatstring(headers, colwidth, c).rstrip())
            a('\n' * l)
            # max number of weeks for this row
            height = max(len(cal) for cal in row)
            for j in range(height):
                weeks = []
                for cal in row:
                    if j >= len(cal):
                        weeks.append('')
                    else:
                        weeks.append(self.formatweek(cal[j], w))
                a(calendar.formatstring(weeks, colwidth, c).rstrip())
                a('\n' * l)
        return ''.join(v)
