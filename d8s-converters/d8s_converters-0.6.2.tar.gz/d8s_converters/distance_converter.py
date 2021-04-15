from .converter import convert

""" The code in this file was created from this code:
s = '''
def {{a}}_to_{{b}}({{a}}):
    return convert({{a}}, '{{a}}', '{{b}}')'''

# these time units (with 'meter' added) were taken from:
# https://github.com/hgrecco/pint/blob/ffc05dcf92347b217e14adbf96c36160f6128627/pint/default_en.txt
l = ['meter',
'centimeter',
'millimeter',
'kilometer',
'inch',
'hand',
'foot',
'yard',
'mile',
'light_year',
'astronomical_unit',
'parsec',
'nautical_mile',
'angstrom',
'micron',
'planck_length',]
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

file_append('../democritus_core/distance_converter.py', '\n\n\n'.join(funcs))
"""


def meters_to_centimeters(meters):
    return convert(meters, 'meters', 'centimeters')


def meters_to_millimeters(meters):
    return convert(meters, 'meters', 'millimeters')


def meters_to_kilometers(meters):
    return convert(meters, 'meters', 'kilometers')


def meters_to_inches(meters):
    return convert(meters, 'meters', 'inches')


def meters_to_hands(meters):
    return convert(meters, 'meters', 'hands')


def meters_to_feet(meters):
    return convert(meters, 'meters', 'feet')


def meters_to_yards(meters):
    return convert(meters, 'meters', 'yards')


def meters_to_miles(meters):
    return convert(meters, 'meters', 'miles')


def meters_to_light_years(meters):
    return convert(meters, 'meters', 'light_years')


def meters_to_astronomical_units(meters):
    return convert(meters, 'meters', 'astronomical_units')


def meters_to_parsecs(meters):
    return convert(meters, 'meters', 'parsecs')


def meters_to_nautical_miles(meters):
    return convert(meters, 'meters', 'nautical_miles')


def meters_to_angstroms(meters):
    return convert(meters, 'meters', 'angstroms')


def meters_to_microns(meters):
    return convert(meters, 'meters', 'microns')


def meters_to_planck_lengths(meters):
    return convert(meters, 'meters', 'planck_lengths')


def centimeters_to_meters(centimeters):
    return convert(centimeters, 'centimeters', 'meters')


def centimeters_to_millimeters(centimeters):
    return convert(centimeters, 'centimeters', 'millimeters')


def centimeters_to_kilometers(centimeters):
    return convert(centimeters, 'centimeters', 'kilometers')


def centimeters_to_inches(centimeters):
    return convert(centimeters, 'centimeters', 'inches')


def centimeters_to_hands(centimeters):
    return convert(centimeters, 'centimeters', 'hands')


def centimeters_to_feet(centimeters):
    return convert(centimeters, 'centimeters', 'feet')


def centimeters_to_yards(centimeters):
    return convert(centimeters, 'centimeters', 'yards')


def centimeters_to_miles(centimeters):
    return convert(centimeters, 'centimeters', 'miles')


def centimeters_to_light_years(centimeters):
    return convert(centimeters, 'centimeters', 'light_years')


def centimeters_to_astronomical_units(centimeters):
    return convert(centimeters, 'centimeters', 'astronomical_units')


def centimeters_to_parsecs(centimeters):
    return convert(centimeters, 'centimeters', 'parsecs')


def centimeters_to_nautical_miles(centimeters):
    return convert(centimeters, 'centimeters', 'nautical_miles')


def centimeters_to_angstroms(centimeters):
    return convert(centimeters, 'centimeters', 'angstroms')


def centimeters_to_microns(centimeters):
    return convert(centimeters, 'centimeters', 'microns')


def centimeters_to_planck_lengths(centimeters):
    return convert(centimeters, 'centimeters', 'planck_lengths')


def millimeters_to_meters(millimeters):
    return convert(millimeters, 'millimeters', 'meters')


def millimeters_to_centimeters(millimeters):
    return convert(millimeters, 'millimeters', 'centimeters')


def millimeters_to_kilometers(millimeters):
    return convert(millimeters, 'millimeters', 'kilometers')


def millimeters_to_inches(millimeters):
    return convert(millimeters, 'millimeters', 'inches')


def millimeters_to_hands(millimeters):
    return convert(millimeters, 'millimeters', 'hands')


def millimeters_to_feet(millimeters):
    return convert(millimeters, 'millimeters', 'feet')


def millimeters_to_yards(millimeters):
    return convert(millimeters, 'millimeters', 'yards')


def millimeters_to_miles(millimeters):
    return convert(millimeters, 'millimeters', 'miles')


def millimeters_to_light_years(millimeters):
    return convert(millimeters, 'millimeters', 'light_years')


def millimeters_to_astronomical_units(millimeters):
    return convert(millimeters, 'millimeters', 'astronomical_units')


def millimeters_to_parsecs(millimeters):
    return convert(millimeters, 'millimeters', 'parsecs')


def millimeters_to_nautical_miles(millimeters):
    return convert(millimeters, 'millimeters', 'nautical_miles')


def millimeters_to_angstroms(millimeters):
    return convert(millimeters, 'millimeters', 'angstroms')


def millimeters_to_microns(millimeters):
    return convert(millimeters, 'millimeters', 'microns')


def millimeters_to_planck_lengths(millimeters):
    return convert(millimeters, 'millimeters', 'planck_lengths')


def kilometers_to_meters(kilometers):
    return convert(kilometers, 'kilometers', 'meters')


def kilometers_to_centimeters(kilometers):
    return convert(kilometers, 'kilometers', 'centimeters')


def kilometers_to_millimeters(kilometers):
    return convert(kilometers, 'kilometers', 'millimeters')


def kilometers_to_inches(kilometers):
    return convert(kilometers, 'kilometers', 'inches')


def kilometers_to_hands(kilometers):
    return convert(kilometers, 'kilometers', 'hands')


def kilometers_to_feet(kilometers):
    return convert(kilometers, 'kilometers', 'feet')


def kilometers_to_yards(kilometers):
    return convert(kilometers, 'kilometers', 'yards')


def kilometers_to_miles(kilometers):
    return convert(kilometers, 'kilometers', 'miles')


def kilometers_to_light_years(kilometers):
    return convert(kilometers, 'kilometers', 'light_years')


def kilometers_to_astronomical_units(kilometers):
    return convert(kilometers, 'kilometers', 'astronomical_units')


def kilometers_to_parsecs(kilometers):
    return convert(kilometers, 'kilometers', 'parsecs')


def kilometers_to_nautical_miles(kilometers):
    return convert(kilometers, 'kilometers', 'nautical_miles')


def kilometers_to_angstroms(kilometers):
    return convert(kilometers, 'kilometers', 'angstroms')


def kilometers_to_microns(kilometers):
    return convert(kilometers, 'kilometers', 'microns')


def kilometers_to_planck_lengths(kilometers):
    return convert(kilometers, 'kilometers', 'planck_lengths')


def inches_to_meters(inches):
    return convert(inches, 'inches', 'meters')


def inches_to_centimeters(inches):
    return convert(inches, 'inches', 'centimeters')


def inches_to_millimeters(inches):
    return convert(inches, 'inches', 'millimeters')


def inches_to_kilometers(inches):
    return convert(inches, 'inches', 'kilometers')


def inches_to_hands(inches):
    return convert(inches, 'inches', 'hands')


def inches_to_feet(inches):
    return convert(inches, 'inches', 'feet')


def inches_to_yards(inches):
    return convert(inches, 'inches', 'yards')


def inches_to_miles(inches):
    return convert(inches, 'inches', 'miles')


def inches_to_light_years(inches):
    return convert(inches, 'inches', 'light_years')


def inches_to_astronomical_units(inches):
    return convert(inches, 'inches', 'astronomical_units')


def inches_to_parsecs(inches):
    return convert(inches, 'inches', 'parsecs')


def inches_to_nautical_miles(inches):
    return convert(inches, 'inches', 'nautical_miles')


def inches_to_angstroms(inches):
    return convert(inches, 'inches', 'angstroms')


def inches_to_microns(inches):
    return convert(inches, 'inches', 'microns')


def inches_to_planck_lengths(inches):
    return convert(inches, 'inches', 'planck_lengths')


def hands_to_meters(hands):
    return convert(hands, 'hands', 'meters')


def hands_to_centimeters(hands):
    return convert(hands, 'hands', 'centimeters')


def hands_to_millimeters(hands):
    return convert(hands, 'hands', 'millimeters')


def hands_to_kilometers(hands):
    return convert(hands, 'hands', 'kilometers')


def hands_to_inches(hands):
    return convert(hands, 'hands', 'inches')


def hands_to_feet(hands):
    return convert(hands, 'hands', 'feet')


def hands_to_yards(hands):
    return convert(hands, 'hands', 'yards')


def hands_to_miles(hands):
    return convert(hands, 'hands', 'miles')


def hands_to_light_years(hands):
    return convert(hands, 'hands', 'light_years')


def hands_to_astronomical_units(hands):
    return convert(hands, 'hands', 'astronomical_units')


def hands_to_parsecs(hands):
    return convert(hands, 'hands', 'parsecs')


def hands_to_nautical_miles(hands):
    return convert(hands, 'hands', 'nautical_miles')


def hands_to_angstroms(hands):
    return convert(hands, 'hands', 'angstroms')


def hands_to_microns(hands):
    return convert(hands, 'hands', 'microns')


def hands_to_planck_lengths(hands):
    return convert(hands, 'hands', 'planck_lengths')


def feet_to_meters(feet):
    return convert(feet, 'feet', 'meters')


def feet_to_centimeters(feet):
    return convert(feet, 'feet', 'centimeters')


def feet_to_millimeters(feet):
    return convert(feet, 'feet', 'millimeters')


def feet_to_kilometers(feet):
    return convert(feet, 'feet', 'kilometers')


def feet_to_inches(feet):
    return convert(feet, 'feet', 'inches')


def feet_to_hands(feet):
    return convert(feet, 'feet', 'hands')


def feet_to_yards(feet):
    return convert(feet, 'feet', 'yards')


def feet_to_miles(feet):
    return convert(feet, 'feet', 'miles')


def feet_to_light_years(feet):
    return convert(feet, 'feet', 'light_years')


def feet_to_astronomical_units(feet):
    return convert(feet, 'feet', 'astronomical_units')


def feet_to_parsecs(feet):
    return convert(feet, 'feet', 'parsecs')


def feet_to_nautical_miles(feet):
    return convert(feet, 'feet', 'nautical_miles')


def feet_to_angstroms(feet):
    return convert(feet, 'feet', 'angstroms')


def feet_to_microns(feet):
    return convert(feet, 'feet', 'microns')


def feet_to_planck_lengths(feet):
    return convert(feet, 'feet', 'planck_lengths')


def yards_to_meters(yards):
    return convert(yards, 'yards', 'meters')


def yards_to_centimeters(yards):
    return convert(yards, 'yards', 'centimeters')


def yards_to_millimeters(yards):
    return convert(yards, 'yards', 'millimeters')


def yards_to_kilometers(yards):
    return convert(yards, 'yards', 'kilometers')


def yards_to_inches(yards):
    return convert(yards, 'yards', 'inches')


def yards_to_hands(yards):
    return convert(yards, 'yards', 'hands')


def yards_to_feet(yards):
    return convert(yards, 'yards', 'feet')


def yards_to_miles(yards):
    return convert(yards, 'yards', 'miles')


def yards_to_light_years(yards):
    return convert(yards, 'yards', 'light_years')


def yards_to_astronomical_units(yards):
    return convert(yards, 'yards', 'astronomical_units')


def yards_to_parsecs(yards):
    return convert(yards, 'yards', 'parsecs')


def yards_to_nautical_miles(yards):
    return convert(yards, 'yards', 'nautical_miles')


def yards_to_angstroms(yards):
    return convert(yards, 'yards', 'angstroms')


def yards_to_microns(yards):
    return convert(yards, 'yards', 'microns')


def yards_to_planck_lengths(yards):
    return convert(yards, 'yards', 'planck_lengths')


def miles_to_meters(miles):
    return convert(miles, 'miles', 'meters')


def miles_to_centimeters(miles):
    return convert(miles, 'miles', 'centimeters')


def miles_to_millimeters(miles):
    return convert(miles, 'miles', 'millimeters')


def miles_to_kilometers(miles):
    return convert(miles, 'miles', 'kilometers')


def miles_to_inches(miles):
    return convert(miles, 'miles', 'inches')


def miles_to_hands(miles):
    return convert(miles, 'miles', 'hands')


def miles_to_feet(miles):
    return convert(miles, 'miles', 'feet')


def miles_to_yards(miles):
    return convert(miles, 'miles', 'yards')


def miles_to_light_years(miles):
    return convert(miles, 'miles', 'light_years')


def miles_to_astronomical_units(miles):
    return convert(miles, 'miles', 'astronomical_units')


def miles_to_parsecs(miles):
    return convert(miles, 'miles', 'parsecs')


def miles_to_nautical_miles(miles):
    return convert(miles, 'miles', 'nautical_miles')


def miles_to_angstroms(miles):
    return convert(miles, 'miles', 'angstroms')


def miles_to_microns(miles):
    return convert(miles, 'miles', 'microns')


def miles_to_planck_lengths(miles):
    return convert(miles, 'miles', 'planck_lengths')


def light_years_to_meters(light_years):
    return convert(light_years, 'light_years', 'meters')


def light_years_to_centimeters(light_years):
    return convert(light_years, 'light_years', 'centimeters')


def light_years_to_millimeters(light_years):
    return convert(light_years, 'light_years', 'millimeters')


def light_years_to_kilometers(light_years):
    return convert(light_years, 'light_years', 'kilometers')


def light_years_to_inches(light_years):
    return convert(light_years, 'light_years', 'inches')


def light_years_to_hands(light_years):
    return convert(light_years, 'light_years', 'hands')


def light_years_to_feet(light_years):
    return convert(light_years, 'light_years', 'feet')


def light_years_to_yards(light_years):
    return convert(light_years, 'light_years', 'yards')


def light_years_to_miles(light_years):
    return convert(light_years, 'light_years', 'miles')


def light_years_to_astronomical_units(light_years):
    return convert(light_years, 'light_years', 'astronomical_units')


def light_years_to_parsecs(light_years):
    return convert(light_years, 'light_years', 'parsecs')


def light_years_to_nautical_miles(light_years):
    return convert(light_years, 'light_years', 'nautical_miles')


def light_years_to_angstroms(light_years):
    return convert(light_years, 'light_years', 'angstroms')


def light_years_to_microns(light_years):
    return convert(light_years, 'light_years', 'microns')


def light_years_to_planck_lengths(light_years):
    return convert(light_years, 'light_years', 'planck_lengths')


def astronomical_units_to_meters(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'meters')


def astronomical_units_to_centimeters(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'centimeters')


def astronomical_units_to_millimeters(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'millimeters')


def astronomical_units_to_kilometers(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'kilometers')


def astronomical_units_to_inches(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'inches')


def astronomical_units_to_hands(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'hands')


def astronomical_units_to_feet(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'feet')


def astronomical_units_to_yards(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'yards')


def astronomical_units_to_miles(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'miles')


def astronomical_units_to_light_years(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'light_years')


def astronomical_units_to_parsecs(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'parsecs')


def astronomical_units_to_nautical_miles(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'nautical_miles')


def astronomical_units_to_angstroms(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'angstroms')


def astronomical_units_to_microns(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'microns')


def astronomical_units_to_planck_lengths(astronomical_units):
    return convert(astronomical_units, 'astronomical_units', 'planck_lengths')


def parsecs_to_meters(parsecs):
    return convert(parsecs, 'parsecs', 'meters')


def parsecs_to_centimeters(parsecs):
    return convert(parsecs, 'parsecs', 'centimeters')


def parsecs_to_millimeters(parsecs):
    return convert(parsecs, 'parsecs', 'millimeters')


def parsecs_to_kilometers(parsecs):
    return convert(parsecs, 'parsecs', 'kilometers')


def parsecs_to_inches(parsecs):
    return convert(parsecs, 'parsecs', 'inches')


def parsecs_to_hands(parsecs):
    return convert(parsecs, 'parsecs', 'hands')


def parsecs_to_feet(parsecs):
    return convert(parsecs, 'parsecs', 'feet')


def parsecs_to_yards(parsecs):
    return convert(parsecs, 'parsecs', 'yards')


def parsecs_to_miles(parsecs):
    return convert(parsecs, 'parsecs', 'miles')


def parsecs_to_light_years(parsecs):
    return convert(parsecs, 'parsecs', 'light_years')


def parsecs_to_astronomical_units(parsecs):
    return convert(parsecs, 'parsecs', 'astronomical_units')


def parsecs_to_nautical_miles(parsecs):
    return convert(parsecs, 'parsecs', 'nautical_miles')


def parsecs_to_angstroms(parsecs):
    return convert(parsecs, 'parsecs', 'angstroms')


def parsecs_to_microns(parsecs):
    return convert(parsecs, 'parsecs', 'microns')


def parsecs_to_planck_lengths(parsecs):
    return convert(parsecs, 'parsecs', 'planck_lengths')


def nautical_miles_to_meters(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'meters')


def nautical_miles_to_centimeters(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'centimeters')


def nautical_miles_to_millimeters(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'millimeters')


def nautical_miles_to_kilometers(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'kilometers')


def nautical_miles_to_inches(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'inches')


def nautical_miles_to_hands(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'hands')


def nautical_miles_to_feet(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'feet')


def nautical_miles_to_yards(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'yards')


def nautical_miles_to_miles(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'miles')


def nautical_miles_to_light_years(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'light_years')


def nautical_miles_to_astronomical_units(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'astronomical_units')


def nautical_miles_to_parsecs(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'parsecs')


def nautical_miles_to_angstroms(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'angstroms')


def nautical_miles_to_microns(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'microns')


def nautical_miles_to_planck_lengths(nautical_miles):
    return convert(nautical_miles, 'nautical_miles', 'planck_lengths')


def angstroms_to_meters(angstroms):
    return convert(angstroms, 'angstroms', 'meters')


def angstroms_to_centimeters(angstroms):
    return convert(angstroms, 'angstroms', 'centimeters')


def angstroms_to_millimeters(angstroms):
    return convert(angstroms, 'angstroms', 'millimeters')


def angstroms_to_kilometers(angstroms):
    return convert(angstroms, 'angstroms', 'kilometers')


def angstroms_to_inches(angstroms):
    return convert(angstroms, 'angstroms', 'inches')


def angstroms_to_hands(angstroms):
    return convert(angstroms, 'angstroms', 'hands')


def angstroms_to_feet(angstroms):
    return convert(angstroms, 'angstroms', 'feet')


def angstroms_to_yards(angstroms):
    return convert(angstroms, 'angstroms', 'yards')


def angstroms_to_miles(angstroms):
    return convert(angstroms, 'angstroms', 'miles')


def angstroms_to_light_years(angstroms):
    return convert(angstroms, 'angstroms', 'light_years')


def angstroms_to_astronomical_units(angstroms):
    return convert(angstroms, 'angstroms', 'astronomical_units')


def angstroms_to_parsecs(angstroms):
    return convert(angstroms, 'angstroms', 'parsecs')


def angstroms_to_nautical_miles(angstroms):
    return convert(angstroms, 'angstroms', 'nautical_miles')


def angstroms_to_microns(angstroms):
    return convert(angstroms, 'angstroms', 'microns')


def angstroms_to_planck_lengths(angstroms):
    return convert(angstroms, 'angstroms', 'planck_lengths')


def microns_to_meters(microns):
    return convert(microns, 'microns', 'meters')


def microns_to_centimeters(microns):
    return convert(microns, 'microns', 'centimeters')


def microns_to_millimeters(microns):
    return convert(microns, 'microns', 'millimeters')


def microns_to_kilometers(microns):
    return convert(microns, 'microns', 'kilometers')


def microns_to_inches(microns):
    return convert(microns, 'microns', 'inches')


def microns_to_hands(microns):
    return convert(microns, 'microns', 'hands')


def microns_to_feet(microns):
    return convert(microns, 'microns', 'feet')


def microns_to_yards(microns):
    return convert(microns, 'microns', 'yards')


def microns_to_miles(microns):
    return convert(microns, 'microns', 'miles')


def microns_to_light_years(microns):
    return convert(microns, 'microns', 'light_years')


def microns_to_astronomical_units(microns):
    return convert(microns, 'microns', 'astronomical_units')


def microns_to_parsecs(microns):
    return convert(microns, 'microns', 'parsecs')


def microns_to_nautical_miles(microns):
    return convert(microns, 'microns', 'nautical_miles')


def microns_to_angstroms(microns):
    return convert(microns, 'microns', 'angstroms')


def microns_to_planck_lengths(microns):
    return convert(microns, 'microns', 'planck_lengths')


def planck_lengths_to_meters(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'meters')


def planck_lengths_to_centimeters(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'centimeters')


def planck_lengths_to_millimeters(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'millimeters')


def planck_lengths_to_kilometers(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'kilometers')


def planck_lengths_to_inches(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'inches')


def planck_lengths_to_hands(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'hands')


def planck_lengths_to_feet(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'feet')


def planck_lengths_to_yards(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'yards')


def planck_lengths_to_miles(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'miles')


def planck_lengths_to_light_years(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'light_years')


def planck_lengths_to_astronomical_units(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'astronomical_units')


def planck_lengths_to_parsecs(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'parsecs')


def planck_lengths_to_nautical_miles(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'nautical_miles')


def planck_lengths_to_angstroms(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'angstroms')


def planck_lengths_to_microns(planck_lengths):
    return convert(planck_lengths, 'planck_lengths', 'microns')
