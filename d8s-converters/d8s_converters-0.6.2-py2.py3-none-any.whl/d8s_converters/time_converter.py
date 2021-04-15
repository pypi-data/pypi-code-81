from .converter import convert

""" The code in this file was created from this code:
s = '''
def {{a}}_to_{{b}}({{a}}):
    return convert({{a}}, '{{a}}', '{{b}}')'''

# these time units (with 'second' added) were taken from:
# https://github.com/hgrecco/pint/blob/ffc05dcf92347b217e14adbf96c36160f6128627/pint/default_en.txt#L168
l = ['second',
'minute',
'hour',
'day',
'week',
'fortnight',
'year',
'month',
'century',
'millennium',]
l = pluralize(l)

funcs = []

for i in l:
    for j in l:
        if i == j:
            continue
        new_func = template_render(s, a=i, b=j)
        funcs.append(new_func)

for i in funcs:
    print(i)
    print('\n\n')

file_append('../democritus_core/time_converter.py', '\n\n\n'.join(funcs))
"""


def seconds_to_minutes(seconds):
    return convert(seconds, 'seconds', 'minutes')


def seconds_to_hours(seconds):
    return convert(seconds, 'seconds', 'hours')


def seconds_to_days(seconds):
    return convert(seconds, 'seconds', 'days')


def seconds_to_weeks(seconds):
    return convert(seconds, 'seconds', 'weeks')


def seconds_to_fortnights(seconds):
    return convert(seconds, 'seconds', 'fortnights')


def seconds_to_years(seconds):
    return convert(seconds, 'seconds', 'years')


def seconds_to_months(seconds):
    return convert(seconds, 'seconds', 'months')


def seconds_to_centuries(seconds):
    return convert(seconds, 'seconds', 'centuries')


def seconds_to_millenniums(seconds):
    return convert(seconds, 'seconds', 'millenniums')


def minutes_to_seconds(minutes):
    return convert(minutes, 'minutes', 'seconds')


def minutes_to_hours(minutes):
    return convert(minutes, 'minutes', 'hours')


def minutes_to_days(minutes):
    return convert(minutes, 'minutes', 'days')


def minutes_to_weeks(minutes):
    return convert(minutes, 'minutes', 'weeks')


def minutes_to_fortnights(minutes):
    return convert(minutes, 'minutes', 'fortnights')


def minutes_to_years(minutes):
    return convert(minutes, 'minutes', 'years')


def minutes_to_months(minutes):
    return convert(minutes, 'minutes', 'months')


def minutes_to_centuries(minutes):
    return convert(minutes, 'minutes', 'centuries')


def minutes_to_millenniums(minutes):
    return convert(minutes, 'minutes', 'millenniums')


def hours_to_seconds(hours):
    return convert(hours, 'hours', 'seconds')


def hours_to_minutes(hours):
    return convert(hours, 'hours', 'minutes')


def hours_to_days(hours):
    return convert(hours, 'hours', 'days')


def hours_to_weeks(hours):
    return convert(hours, 'hours', 'weeks')


def hours_to_fortnights(hours):
    return convert(hours, 'hours', 'fortnights')


def hours_to_years(hours):
    return convert(hours, 'hours', 'years')


def hours_to_months(hours):
    return convert(hours, 'hours', 'months')


def hours_to_centuries(hours):
    return convert(hours, 'hours', 'centuries')


def hours_to_millenniums(hours):
    return convert(hours, 'hours', 'millenniums')


def days_to_seconds(days):
    return convert(days, 'days', 'seconds')


def days_to_minutes(days):
    return convert(days, 'days', 'minutes')


def days_to_hours(days):
    return convert(days, 'days', 'hours')


def days_to_weeks(days):
    return convert(days, 'days', 'weeks')


def days_to_fortnights(days):
    return convert(days, 'days', 'fortnights')


def days_to_years(days):
    return convert(days, 'days', 'years')


def days_to_months(days):
    return convert(days, 'days', 'months')


def days_to_centuries(days):
    return convert(days, 'days', 'centuries')


def days_to_millenniums(days):
    return convert(days, 'days', 'millenniums')


def weeks_to_seconds(weeks):
    return convert(weeks, 'weeks', 'seconds')


def weeks_to_minutes(weeks):
    return convert(weeks, 'weeks', 'minutes')


def weeks_to_hours(weeks):
    return convert(weeks, 'weeks', 'hours')


def weeks_to_days(weeks):
    return convert(weeks, 'weeks', 'days')


def weeks_to_fortnights(weeks):
    return convert(weeks, 'weeks', 'fortnights')


def weeks_to_years(weeks):
    return convert(weeks, 'weeks', 'years')


def weeks_to_months(weeks):
    return convert(weeks, 'weeks', 'months')


def weeks_to_centuries(weeks):
    return convert(weeks, 'weeks', 'centuries')


def weeks_to_millenniums(weeks):
    return convert(weeks, 'weeks', 'millenniums')


def fortnights_to_seconds(fortnights):
    return convert(fortnights, 'fortnights', 'seconds')


def fortnights_to_minutes(fortnights):
    return convert(fortnights, 'fortnights', 'minutes')


def fortnights_to_hours(fortnights):
    return convert(fortnights, 'fortnights', 'hours')


def fortnights_to_days(fortnights):
    return convert(fortnights, 'fortnights', 'days')


def fortnights_to_weeks(fortnights):
    return convert(fortnights, 'fortnights', 'weeks')


def fortnights_to_years(fortnights):
    return convert(fortnights, 'fortnights', 'years')


def fortnights_to_months(fortnights):
    return convert(fortnights, 'fortnights', 'months')


def fortnights_to_centuries(fortnights):
    return convert(fortnights, 'fortnights', 'centuries')


def fortnights_to_millenniums(fortnights):
    return convert(fortnights, 'fortnights', 'millenniums')


def years_to_seconds(years):
    return convert(years, 'years', 'seconds')


def years_to_minutes(years):
    return convert(years, 'years', 'minutes')


def years_to_hours(years):
    return convert(years, 'years', 'hours')


def years_to_days(years):
    return convert(years, 'years', 'days')


def years_to_weeks(years):
    return convert(years, 'years', 'weeks')


def years_to_fortnights(years):
    return convert(years, 'years', 'fortnights')


def years_to_months(years):
    return convert(years, 'years', 'months')


def years_to_centuries(years):
    return convert(years, 'years', 'centuries')


def years_to_millenniums(years):
    return convert(years, 'years', 'millenniums')


def months_to_seconds(months):
    return convert(months, 'months', 'seconds')


def months_to_minutes(months):
    return convert(months, 'months', 'minutes')


def months_to_hours(months):
    return convert(months, 'months', 'hours')


def months_to_days(months):
    return convert(months, 'months', 'days')


def months_to_weeks(months):
    return convert(months, 'months', 'weeks')


def months_to_fortnights(months):
    return convert(months, 'months', 'fortnights')


def months_to_years(months):
    return convert(months, 'months', 'years')


def months_to_centuries(months):
    return convert(months, 'months', 'centuries')


def months_to_millenniums(months):
    return convert(months, 'months', 'millenniums')


def centuries_to_seconds(centuries):
    return convert(centuries, 'centuries', 'seconds')


def centuries_to_minutes(centuries):
    return convert(centuries, 'centuries', 'minutes')


def centuries_to_hours(centuries):
    return convert(centuries, 'centuries', 'hours')


def centuries_to_days(centuries):
    return convert(centuries, 'centuries', 'days')


def centuries_to_weeks(centuries):
    return convert(centuries, 'centuries', 'weeks')


def centuries_to_fortnights(centuries):
    return convert(centuries, 'centuries', 'fortnights')


def centuries_to_years(centuries):
    return convert(centuries, 'centuries', 'years')


def centuries_to_months(centuries):
    return convert(centuries, 'centuries', 'months')


def centuries_to_millenniums(centuries):
    return convert(centuries, 'centuries', 'millenniums')


def millenniums_to_seconds(millenniums):
    return convert(millenniums, 'millenniums', 'seconds')


def millenniums_to_minutes(millenniums):
    return convert(millenniums, 'millenniums', 'minutes')


def millenniums_to_hours(millenniums):
    return convert(millenniums, 'millenniums', 'hours')


def millenniums_to_days(millenniums):
    return convert(millenniums, 'millenniums', 'days')


def millenniums_to_weeks(millenniums):
    return convert(millenniums, 'millenniums', 'weeks')


def millenniums_to_fortnights(millenniums):
    return convert(millenniums, 'millenniums', 'fortnights')


def millenniums_to_years(millenniums):
    return convert(millenniums, 'millenniums', 'years')


def millenniums_to_months(millenniums):
    return convert(millenniums, 'millenniums', 'months')


def millenniums_to_centuries(millenniums):
    return convert(millenniums, 'millenniums', 'centuries')
