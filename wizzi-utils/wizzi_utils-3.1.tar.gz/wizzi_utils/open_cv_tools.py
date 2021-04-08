import numpy as np
import cv2
import math
from wizzi_utils import misc_tools
from wizzi_utils import pyplot_tools


def get_cv_version() -> str:
    string = '* Open cv version {}'.format(cv2.getVersionString())
    return string


def load_img(path: str, ack: bool = True, tabs: int = 1) -> np.array:
    img = cv2.imread(path)
    if ack:
        print('{}loaded img from {}'.format(tabs * '\t', path))
    return img


def save_img(path: str, img: np.array, ack: bool = True, tabs: int = 1) -> None:
    cv2.imwrite(path, img)
    if ack:
        print('{}saving img to {}'.format(tabs * '\t', path))
    return


def list_to_cv_image(cv_img: [list, np.array]) -> np.array:
    """
    :param cv_img: numpy or list. if list: convert to numpy with dtype uint8
    :return: cv_img
    """
    if isinstance(cv_img, list):
        cv_img = np.array(cv_img, dtype='uint8')
    return cv_img


def display_open_cv_image(
        img: np.array,
        ms: int = 0,
        title: str = '',
        x_y: tuple = (0, 0),
        resize_scale_percent: float = 0
) -> None:
    """
    :param img: cv image in numpy array or list
    :param ms: 0 blocks, else time in milliseconds before image is closed
    :param title: window title
    :param x_y: top left window coordinates
    :param resize_scale_percent: 0 for original size. else img_size *= resize (resize > 0)
    im_path = '../temp/test_img.jpg'
    img = load_img(im_path, ack=True, tabs=0)
    print(misc_tools.to_str(img, 'cv_img'))
    display_open_cv_image(
        img=img,  # img=img.tolist() also supported
        ms=0,  # block
        title='test image',  # title
        x_y=(200, 150),  # window top left corner
        resize_scale_percent=0.8,  # 80% of img size
    )
    cv2.destroyAllWindows()
    """
    img = list_to_cv_image(img)
    if resize_scale_percent > 0:
        img = resize_opencv_image(img, resize_scale_percent)
    cv2.imshow(title, img)
    cv2.moveWindow(title, x_y[0], x_y[1])
    cv2.waitKey(ms)
    return


def resize_opencv_image(img: np.array, scale_percent: float):
    """
    :param img: cv img
    :param scale_percent: float>0(could be bigger than 1)
    img_size *= scale_percent
    :return:
    """
    width = math.ceil(img.shape[1] * scale_percent)
    height = math.ceil(img.shape[0] * scale_percent)
    dim = (width, height)
    resize_image = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resize_image


def unpack_list_imgs_to_big_image(imgs: list, resize: int, grid: tuple) -> np.array:
    for i in range(len(imgs)):
        imgs[i] = list_to_cv_image(imgs[i])
        if resize > 0:
            imgs[i] = resize_opencv_image(imgs[i], resize)
        if len(imgs[i].shape) == 2:  # if gray - see as rgb
            imgs[i] = gray_scale_img_to_RGB_form(imgs[i])

    imgs_n = len(imgs)
    if imgs_n == 1:
        big_img = imgs[0]
    else:
        padding_bgr = list(pyplot_tools.get_BGR_color('red'))
        height, width, cnls = imgs[0].shape
        rows, cols = grid
        big_img = np.zeros(shape=(height * rows, width * cols, cnls), dtype='uint8') + 255  # white big image

        row_ind, col_ind = 1, 1
        for i, img in enumerate(imgs):
            h_begin, h_end = height * (row_ind - 1), height * row_ind
            w_begin, w_end = width * (col_ind - 1), width * col_ind
            big_img[h_begin:h_end, w_begin:w_end, :] = img  # 0

            if rows > 1:  # draw bounding box on the edges. no need if there is 1 row or 1 col
                big_img[h_begin, w_begin:w_end, :] = padding_bgr
                big_img[h_end - 1, w_begin:w_end - 1, :] = padding_bgr
            if cols > 1:
                big_img[h_begin:h_end, w_begin, :] = padding_bgr
                big_img[h_begin:h_end, w_end - 1, :] = padding_bgr

            col_ind += 1
            if col_ind > cols:
                col_ind = 1
                row_ind += 1
    return big_img


def display_open_cv_images(
        imgs: list,
        ms: int = 0,
        title: str = '',
        x_y: tuple = (0, 0),
        resize_scale_percent: float = 0,
        grid: tuple = (1, 2)
) -> None:
    """
    :param imgs: list of RGB or gray scale images
    :param ms: 0 blocks, else time in milliseconds before image is closed
    :param title: window title
    :param x_y: top left window coordinates
    :param resize_scale_percent: 0 for original size. else img_size *= resize (resize > 0)
    :param grid: size of rows and cols of the new image. e.g. (2,1) 2 rows with 1 img on each
        grid slots must be >= len(imgs)
    :return:
    im_path = '../temp/test_img.jpg'
    img = load_img(im_path, ack=True, tabs=0)
    print(misc_tools.to_str(img, 'cv_img'))
    imgs_list = [img, img, img, RGB_img_to_gray(img)]

    display_open_cv_images(
        imgs=imgs_list,
        ms=0,
        title='3 in a row',
        x_y=(200, 200),
        resize_scale_percent=0.5,
        grid=(2, 2)
    )
    cv2.destroyAllWindows()
    """
    imgs_n = len(imgs)
    if imgs_n > 0:
        total_slots = grid[0] * grid[1]
        assert imgs_n <= total_slots, 'grid has {} total_slots, but len(imgs)={}'.format(total_slots, imgs_n)
        big_img = unpack_list_imgs_to_big_image(imgs, resize_scale_percent, grid)
        display_open_cv_image(big_img, ms, title, x_y, resize_scale_percent=0)
    return


def gray_scale_img_to_RGB_form(gray_img: np.array) -> np.array:
    """
    :param gray_img: from shape (x,y) - 1 channel (gray)
    e.g 480,640
    :return: RGB form image e.g 480,640,3. no real colors added - just shape as RGB
    """
    RGB_image = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    return RGB_image


def RGB_img_to_gray(rgb_img: np.array) -> np.array:
    """
    :param rgb_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: gray image e.g 480,640. colors are replaced to gray colors
    im_path = '../temp/test_img.jpg'
    img = load_img(im_path, ack=True, tabs=0)
    print(misc_tools.to_str(img, 'cv_img'))
    gray = RGB_img_to_gray(img)
    """
    gray = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    return gray


def main():
    print(get_cv_version())
    im_path = '../temp/test_img.jpg'
    img = load_img(im_path, ack=True, tabs=0)
    print(misc_tools.to_str(img, 'cv_img'))
    imgs_list = [img, img, img, RGB_img_to_gray(img)]

    display_open_cv_images(
        imgs=imgs_list,
        ms=0,
        title='3 in a row',
        x_y=(200, 200),
        resize_scale_percent=0.5,
        grid=(2, 2)
    )
    cv2.destroyAllWindows()

    return


if __name__ == '__main__':
    misc_tools.main_wrapper(
        main_function=main,
        cuda_off=True,
        torch_v=True,
        tf_v=False,
        cv2_v=True,
        with_profiler=False
    )
