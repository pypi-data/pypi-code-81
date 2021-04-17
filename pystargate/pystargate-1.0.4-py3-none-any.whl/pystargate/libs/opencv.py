#!/usr/bin/env python
# -*- coding:utf-8

import cv2
class Opencv():
    def OpencvFindPicture(self, target, template):
        _target = cv2.imread( target )
        _template = cv2.imread( template )
        theight, twidth = _template.shape[:2]
        result = cv2.matchTemplate( _target, _template, cv2.TM_SQDIFF_NORMED )
        cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc( result )
        # strmin_val = str( min_val )
        cv2.rectangle( _target, min_loc, (min_loc[0] + twidth, min_loc[1] + theight), (0, 0, 225), 2 )
        x = min_loc[0]
        y = min_loc[1]
        return x, y
