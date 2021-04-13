

"""
Example of using this library
"""
if __name__ == "__main__":
    import cv2 as cv
    import os
    from time import time
    from Capturing import Capture
    from LiveSettings import Settings
    from Filters import Filters
    from HSV import HsvFilter

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    win = Capture()
    vision_limestone = Settings()
    vision_limestone.init_control_gui()

    # limestone HSV filter
    hsv_filter = HsvFilter(17, 176, 141, 17, 226, 235, 0, 0, 0, 0)

    loop_time = time()
    while True:
        screenshot = win.get_screenshot()

        # screenshot = vision_limestone.apply_hsv_filter(screenshot)
        processed_image = Filters.warm_image(screenshot)

        # rectangles = vision_limestone.find(processed_image, 0.21)
        # points = vision_limestone.get_click_points(rectangles)
        # output_image = vision_limestone.draw_rectangles(screenshot, rectangles)

        cv.imshow('Processed', processed_image)
        # cv.imshow('Matches', output_image)

        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
