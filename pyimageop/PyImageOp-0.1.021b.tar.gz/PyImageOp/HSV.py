class HsvFilter:
    def __init__(self, h_min=None, s_min=None, v_min=None, h_max=None, s_max=None, v_max=None,
                 s_add=None, s_sub=None, v_add=None, v_sub=None):
        """
        Object as a struct to create data of hsv settings

        Parameters
        ----------
        h_min : int
            hue minimum
        s_min : int
            saturation minimum
        v_min : int
            value minimum
        h_max : int
            hue maximum
        s_max : int
            saturation maximum
        v_max : int
            value maximum
        s_add : int
            saturation add provided amount
        s_sub : int
            saturation subtract provided amount
        v_add : int
            value add provided amount
        v_sub : int
            value subtract provided amount
        """
        self.hMin = h_min
        self.sMin = s_min
        self.vMin = v_min
        self.hMax = h_max
        self.sMax = s_max
        self.vMax = v_max
        self.sAdd = s_add
        self.sSub = s_sub
        self.vAdd = v_add
        self.vSub = v_sub
