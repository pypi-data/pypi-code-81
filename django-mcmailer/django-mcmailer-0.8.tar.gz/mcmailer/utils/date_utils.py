def get_difference_between_dates(start, end, interval="all"):
    duration = end - start
    duration_in_s = duration.total_seconds()

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 86400)  # Seconds in a day = 86400

    def hours(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 3600)  # Seconds in an hour = 3600

    def minutes(seconds=None):
        return divmod(seconds if seconds != None else duration_in_s, 60)  # Seconds in a minute = 60

    def seconds(seconds=None):
        if seconds != None:
            return divmod(seconds, 1)
        return duration_in_s

    def total_duration():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "{} years, {} days, {} hours, {} minutes and {} seconds".format(
            int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0])
        )

    def all_without_seconds():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])

        return "{} years, {} days, {} hours and {} minutes".format(
            int(y[0]), int(d[0]), int(h[0]), int(m[0])
        )

    def year_days_hours():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
        h = hours(d[1])

        return "{} years, {} days and {} hours".format(int(y[0]), int(d[0]), int(h[0]))

    # Individual results
    results = {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'year_days_hours': year_days_hours(),
        'all_without_seconds': all_without_seconds(),
        'all': total_duration(),
    }

    return results[interval]
