#  Copyright (c) 2019-2020  Marc van der Sluys - marc.vandersluys.nl
#   
#  This file is part of the AstroTool Python package,
#  see: http://astro.ru.nl/~sluys/AstroTool/
#   
#  This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#  
#  This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License along with this code.  If not, see
#  <http://www.gnu.org/licenses/>.


"""Date and time programs for AstroTool."""

# Modules:
# import math as m
# import numpy as np
import sys


def cli_cal2jd():
    """Command-line tool to convert a Gregorian or Julian calendar date (and time) to a Julian day."""
    
    from astrotool.datetime import julianDay
    
    if( (len(sys.argv) < 3) | (len(sys.argv) > 6) ):
        print("%s converts a Gregorian or Julian calendar date (and time) to a Julian day." % sys.argv[0] )
        sys.exit('Usage: %s <year> <month> <day> [<hour [<minute> [<second>]]' % sys.argv[0])
        
    year  = int(sys.argv[1])
    month = int(sys.argv[2])
    day   = int(sys.argv[3])
    
    if(len(sys.argv) > 3):
        hour  = int(sys.argv[4])
        if(len(sys.argv) > 4):
            minute  = int(sys.argv[5])
            if(len(sys.argv) > 5):
                second  = int(sys.argv[6])
    
    jd = julianDay(year, month, day + hour/24)
            
    print(jd)
    
    return
