import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.art3d import Path3DCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from wizzi_utils import misc_tools


def get_RGB_color(color_str: str) -> tuple:
    """
    :param color_str: e.g. "red", "blue" ...
    :return: RGB color
    rgb_r = get_RGB_color(color)
    rgba_r = get_RGBA_color(color, opacity=1.0)
    bgr_r = get_BGR_color(color)
    print('{}: RGB={}, RGBA={}, BGR={}'.format(color, rgb_r, rgba_r, bgr_r))
    # orange: RGB=(255, 165, 0), RGBA=(1.0, 0.6470588235294118, 0.0, 1.0), BGR=(0, 165, 255)
    """
    rgb = RGBA_to_RGB(color_str)
    return rgb


def get_RGBA_color(color_str: str, opacity: float = 1.0) -> tuple:
    """
    :param color_str: e.g. "red", "blue" ...
    :param opacity: value from 0 to 1
    :return: rgba color
    rgb_r = get_RGB_color(color)
    rgba_r = get_RGBA_color(color, opacity=1.0)
    bgr_r = get_BGR_color(color)
    print('{}: RGB={}, RGBA={}, BGR={}'.format(color, rgb_r, rgba_r, bgr_r))
    # orange: RGB=(255, 165, 0), RGBA=(1.0, 0.6470588235294118, 0.0, 1.0), BGR=(0, 165, 255)
    """
    rgba = matplotlib.colors.to_rgba(color_str, alpha=opacity)
    return rgba


def get_BGR_color(color_str: str) -> tuple:
    """
    :param color_str: e.g. "red", "blue" ...
    :return: bgr color
    rgb_r = get_RGB_color(color)
    rgba_r = get_RGBA_color(color, opacity=1.0)
    bgr_r = get_BGR_color(color)
    print('{}: RGB={}, RGBA={}, BGR={}'.format(color, rgb_r, rgba_r, bgr_r))
    # orange: RGB=(255, 165, 0), RGBA=(1.0, 0.6470588235294118, 0.0, 1.0), BGR=(0, 165, 255)
    """
    bgr = RGBA_to_BGR(color_str)
    return bgr


def RGBA_to_RGB(rgba: [str, tuple]) -> tuple:
    """
    :param rgba: e.g. "orange" or (1.0, 0.6470588235294118, 0.0, 1.0)
    :return: rgb color format
    e.g. orange: RGBA=(1.0, 0.6470588235294118, 0.0, 1.0), RGB=(255, 165, 0)
    """
    rgb_normed = matplotlib.colors.to_rgb(rgba)
    rgb = tuple([int(round(255 * x)) for x in rgb_normed])
    return rgb


def RGBA_to_BGR(rgba: [tuple, str]) -> tuple:
    """
    :param rgba: e.g. "orange" or (1.0, 0.6470588235294118, 0.0, 1.0)
    :return: bgr color format
    e.g. orange RGBA=(1.0, 0.6470588235294118, 0.0, 1.0), BGR=(0, 165, 255)
    """
    rgb = RGBA_to_RGB(rgba)
    bgr = RGB_to_BGR(rgb)
    return bgr


def BGR_to_RGB(bgr: tuple) -> tuple:
    """
    :param bgr:
    :return: rgb
    RGB=(255, 165, 0), BGR=(0, 165, 255)
    """
    rgb = misc_tools.reverse_tuple_or_list(bgr)  # reverse the tuple order
    return rgb


def BGR_to_RGBA(bgr: tuple, opacity: float = 1.0) -> tuple:
    """
    :param bgr:
    :param opacity:
    :return: rgba
    BGR=(0, 165, 255), RGBA=(1.0, 0.6470588235294118, 0.0, 1.0)
    """
    rgb = BGR_to_RGB(bgr)
    rgba = RGB_to_RGBA(rgb, opacity)
    return rgba


def RGB_to_BGR(rgb: tuple) -> tuple:
    """
    :param rgb:
    :return: bgr
    BGR=(0, 165, 255), RGB=(255, 165, 0)
    """
    bgr = misc_tools.reverse_tuple_or_list(rgb)  # reverse the tuple order
    return bgr


def RGB_to_RGBA(rgb: tuple, opacity: float = 1.0) -> tuple:
    """
    :param rgb:
    :param opacity:
    :return: rgba
    RGB=(255, 165, 0), RGBA=(1.0, 0.6470588235294118, 0.0, 1.0)
    """
    rgba = tuple([x / 255 for x in rgb])
    rgba += (opacity,)
    return rgba


def get_x_ticks_list(x_low, x_high, p=10):
    ten_percent_jump = (x_high - x_low) / p
    x_ticks = [x_low + i * ten_percent_jump for i in range(p + 1)]
    return x_ticks


def get_random_color_map(n: int, opacity: float = 1.0) -> np.array:
    """
    get colors list uniform distribution
    :param n: how many colors
    :param opacity:
    :return: np array of size(n,4). each row in RGBA format
    e.g.
    print(misc_tools.to_str(get_random_color_map(n=3), 'random_color_map'))
    """
    colors_map = misc_tools.np_uniform(shape=(n, 4), lows=0, highs=1)
    colors_map[:, -1] = opacity
    return colors_map


def screen_dims():
    """
    should pip install PIL
    :return:
    """
    from PIL import ImageGrab
    try:
        img = ImageGrab.grab()
        window_w, window_h = img.size
    except (ValueError, Exception):
        window_w, window_h = 0, 0
        print('screen_dims()::Failed getting screen_dims')
    return window_w, window_h


def move_figure(fig, x: int, y: int):
    """Move figure's upper left corner to pixel (x, y)"""
    try:
        x, y = int(x), int(y)
        new_geom = "+{}+{}".format(x, y)
        backend = matplotlib.get_backend()
        if backend == 'TkAgg':
            manager = fig.canvas.manager
            manager.window.wm_geometry(new_geom)
        elif backend == 'WXAgg':
            fig.canvas.manager.window.SetPosition((x, y))
        else:
            # This works for QT and GTK
            # You can also use window.setGeometry
            fig.canvas.manager.window.move(x, y)
    except (ValueError, Exception):
        print('move_figure::Failed Moving figure to ({},{})'.format(x, y))
        return
    return


def move_plot(fig, where: str = 'top_left'):
    """
    :param fig:
    :param where:
        top_right, top_center, top_left, bottom_right, bottom_center, bottom_left
    :return:
    """
    try:
        window_w, window_h = screen_dims()  # screen dims in pixels
        fig_w, fig_h = fig.get_size_inches() * fig.dpi  # fig dims in pixels
        task_bar_offset = 100  # about 100 pixels due to task bar

        x, y = 0, 0  # top_left: default

        if where == 'top_center':
            x, y = (window_w - fig_w) / 2, 0
        elif where == 'top_right':
            x, y = (window_w - fig_w), 0
        elif where == 'bottom_left':
            x, y = 0, window_h - fig_h - task_bar_offset
        elif where == 'bottom_center':
            x, y = (window_w - fig_w) / 2, window_h - fig_h - task_bar_offset
        elif where == 'bottom_right':
            x, y = (window_w - fig_w), window_h - fig_h - task_bar_offset
        move_figure(fig=fig, x=x, y=y)
    except (ValueError, Exception):
        print('move_plot::Failed Moving figure to {}'.format(where))
        return
    return


# 2d plots
def plot_2d_iterative_figure(
        rows: int = 1,
        cols: int = 1,
        main_title: str = None,
        sub_titles: list = None,
        labels: list = None,
        default_color: str = 'green',
        resize: float = 0,
        plot_location: str = None,
        x_y_lims: list = None,
        add_center: dict = False,
        zoomed: bool = False,
        render_d: dict = None
) -> (matplotlib.figure, list, list):
    """
    THIS is for building a figure with 1 or more subplots that changes each iteration.
        this function just builds the frame. use update_subplots to insert\change the data of the scatters
    :param rows:
    :param cols:
    :param main_title:
    :param sub_titles: if not None, sub title to each sub plots. |sub_titles| must be equal to rows*cols
    :param labels: if labels are given to each subplot, legend will be on
    :param default_color: when updating, color is not mandatory. if non given, default color will remain
    :param resize: if not 0, figure size *= resize
    :param plot_location: top_right, top_center, top_left, bottom_right, bottom_center, bottom_left or None
    :param x_y_lims: limits of x and y axes. list of 4 ints: x_left, x_right, y_bottom, y_top
    :param add_center: dict. if not None - add center with the params in the dict
        e.g. add_center = {'c': 'orange', 'marker': 'x', 'marker_size': 150, 'label': 'Scene Center'}
    :param zoomed: bool - full screen or not
    :param render_d: dict - if not None: show plot
        block mandatory. pause optional.
        e.g. render = {'block': False, 'pause': 0.0001}
    :return:
    figure
    list of axes
    list of scatters (1 for each ax in axes - this will be used to update the data)

    see full example in update_2d_scatters comments
    """
    plt.close('all')
    figsize = (6.4, 4.8) if resize == 0 else (6.4 * resize, 4.8 * resize)  # default figsize=(6.4, 4.8)
    fig, axes = plt.subplots(nrows=rows, ncols=cols, sharex=False, sharey=False, figsize=figsize)
    axes_list = [axes] if (rows == 1 and cols == 1) else axes.flatten().tolist()

    if sub_titles is not None:
        err_msg = '|sub_titles| must be equal to rows*cols ({}!={})'.format(len(sub_titles), rows * cols)
        assert len(sub_titles) == len(axes_list), err_msg
    if labels is not None:
        err_msg = '|labels| must be equal to rows*cols ({}!={})'.format(len(labels), rows * cols)
        assert len(labels) == len(axes_list), err_msg

    if main_title is not None:
        fig.suptitle(main_title)
    if plot_location is not None:
        move_plot(fig, where=plot_location)

    scatters = []
    for i, ax in enumerate(axes_list):
        if sub_titles is not None:
            ax.set_title(sub_titles[i])
        ax.set_aspect('equal', adjustable='box')

        if x_y_lims is not None:
            ax.set_xlim(left=x_y_lims[0], right=x_y_lims[1])
            ax.set_ylim(bottom=x_y_lims[2], top=x_y_lims[3])
            # scatters.append(sc)

        x_left, x_right = ax.get_xlim()
        y_bottom, y_top = ax.get_ylim()

        cx = int((x_right - x_left) / 2) + x_left
        cy = int((y_top - y_bottom) / 2) + y_bottom

        ax.set_xticks([x_left, cx, x_right])
        ax.set_yticks([y_bottom, cy, y_top])

        if add_center is not None:
            ax.scatter(
                [cx], [cy],
                c=add_center['c'], marker=add_center['marker'],
                s=add_center['marker_size'], label='{}({},{})'.format(add_center['label'], cx, cy)
            )

        # init data scatter for this axis
        if labels is not None:
            sc = ax.scatter([10], [10], c=default_color, marker='.', label=labels[i])
            ax.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5, edgecolor='black')
        else:
            sc = ax.scatter([10], [10], c=default_color, marker='.')
        scatters.append(sc)

    if zoomed:
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')

    if render_d is not None:
        if 'pause' in render_d:
            render(block=render_d['block'], pause=render_d['pause'])
        else:
            render(block=render_d['block'])
    return fig, axes_list, scatters


def update_2d_scatters(
        scatters: list,
        datum: list,
        colors_sets: list = None,
        new_title: str = None,
        save_img_path: str = None,
        render_d: dict = None
) -> None:
    """
    :param scatters: list of scatters to update
    :param datum: list of data per scatter.
            |datum| == |scatters|
            data could be empty list or None
    :param colors_sets: list of colors per scatter.
            if colors_sets is not None: |colors_sets| == |scatters| == |datum|
            color_set could be:
                empty list or None - former color will remain (first is default color)
                list of size 1 - RGBA color. all points will get this color
                list of size |data| - RGBA colors. each point will get it's corresponding color
    :param new_title: changed main title
    :param save_img_path: if not none, save the fig to this path
    :param render_d: dict - if not None: show plot
        block mandatory. pause optional.
        e.g. render = {'block': False, 'pause': 0.0001}
    :return:
    example
    fig, axes_list, scatters = plot_2d_iterative_figure(
        rows=1,
        cols=2,
        main_title='1x1 scatter',
        sub_titles=['left cam', 'right cam'],
        labels=['MVS1', 'MVS2'],
        default_color='blue',
        resize=0,
        plot_location='top_center',
        x_y_lims=[0, 640, 0, 480],  # fits cv img
        add_center={'c': 'orange', 'marker': 'x', 'marker_size': 150, 'label': 'Scene Center'},
        zoomed=False,
        render_d={'block': False, 'pause': 0.0001}
    )
    iters = 10
    for i in range(iters):
        misc_tools.sleep(seconds=1)
        block = (i == iters - 1)  # last iter
        # emulate data of each scatter - say number of points is 3
        datum, colors_sets = [], []
        for j in range(len(scatters)):
            data_j = misc_tools.np_random_integers(low=0, high=480, size=(3, 2))
            if j == 0:  # cam0
                colors = [get_RGBA_color('y')]  # 1 color for all
            else:  # cam1
                colors = get_random_color_map(3)  # random color for each point
                # # fixed color per point
                # colors = [get_RGBA_color('r'), get_RGBA_color('b'), get_RGBA_color('g')]
            if i == 2 and j == 1:  # emulate in iter 2, cam 1 found no data
                data_j = []
                colors = []
            datum.append(data_j)
            colors_sets.append(colors)

        update_2d_scatters(
            scatters=scatters,
            datum=datum,
            colors_sets=colors_sets,
            new_title='iter {}'.format(i),
            render_d={'block': block, 'pause': 0.0001}
        )
    """
    assert len(datum) == len(scatters), 'data per scatter is required.'
    err_msg = 'colors_sets should be none or same size as scatters and datum'
    assert colors_sets is None or len(colors_sets) == len(scatters) == len(datum), err_msg

    if new_title is not None:
        plt.suptitle(new_title)
    for i in range(len(scatters)):
        sc_i = scatters[i]
        if datum[i] is not None and len(datum[i]) > 0:
            sc_i._offsets = datum[i]
            if colors_sets is not None and colors_sets[i] is not None and len(colors_sets[i]) > 0:
                sc_i._facecolors = colors_sets[i]
                sc_i._edgecolors = colors_sets[i]

    if save_img_path is not None:
        plt.savefig(save_img_path, dpi=200, bbox_inches='tight')
        print('saved to {}.png'.format(save_img_path))

    if render_d is not None:
        if 'pause' in render_d:
            render(block=render_d['block'], pause=render_d['pause'])
        else:
            render(block=render_d['block'])
    return


def plot_2d_scatter(
        data: np.array,
        colors: list = None,
        data_label: str = None,
        main_title: str = None,
        sub_title: str = None,
        def_color: str = None,
        resize: float = 0,
        plot_location=None,
        x_y_lims=None,
        save_img_path: str = None,
        add_center: dict = False,
        zoomed: bool = False,
) -> None:
    """
    see documentation in plot_2d_iterative_figure() and update_2d_scatters()

    example:
    data_j = misc_tools.np_random_integers(low=0, high=480, size=(3, 2))
    colors = [get_RGBA_color('r'), get_RGBA_color('b'), get_RGBA_color('g')]
    plot_2d_scatter(
        data=data_j,
        colors=colors,
        data_label='SCP',
        main_title='1x1 scatter',
        sub_title='normal 2d scatter',
        def_color='green',
        resize=0,
        plot_location='top_center',
        x_y_lims=[0, 640, 0, 480],  # fits cv img,
        save_img_path='./test',
        add_center={'c': 'orange', 'marker': 'x', 'marker_size': 150, 'label': 'Scene Center'},
        zoomed=False,
    )
    """
    fig, axes_list, scatters = plot_2d_iterative_figure(
        rows=1,
        cols=1,
        main_title=main_title,
        sub_titles=[sub_title],
        labels=[data_label],
        default_color=def_color,
        resize=resize,
        plot_location=plot_location,
        x_y_lims=x_y_lims,
        add_center=add_center,
        zoomed=zoomed,
        render_d=None
    )
    update_2d_scatters(
        scatters=scatters,
        datum=[data],
        colors_sets=[colors],
        new_title=None,
        save_img_path=save_img_path,
        render_d={'block': True}
    )
    return


def plot_x_y_std(data_x: np.array, groups: list, title: str = None, x_label: str = 'Size', y_label: str = 'Error',
                 save_path: str = None, show_plot: bool = True, with_shift: bool = False):
    """
    data_x: x values
    groups: list of groups s.t. each tuple(y values, y std, color, title)  y std could be None
    example:
        data_x = [10, 20, 30]
        C_errors = [5, 7, 1]
        C_errors_stds = [2, 1, 0.5]
        group_c = (C_errors, C_errors_stds, 'g', 'C')
        U_errors = [10, 8, 3]
        U_errors_vars = [4, 3, 1.5]
        group_u = (U_errors, U_errors_vars, 'r', 'U')
        groups = [group_c, group_u]
        title = 'bla'
        plot_x_y_std(data_x, groups, title)
    :return:
    """
    data_x_last = data_x  # in order to see all STDs, move a little on the x axis
    data_x_jump = 0.5
    data_x_offset = - int(len(groups) / 2) * data_x_jump
    line_style = {"linestyle": "-", "linewidth": 1, "markeredgewidth": 2, "elinewidth": 1, "capsize": 4}
    for i, group in enumerate(groups):
        data_y, std_y = group[0], group[1]  # std_y could be None
        color, label = group[2], group[3]
        if with_shift:  # move x data for each set a bit so you can see it clearly
            dx_shift = [x + i * data_x_jump + data_x_offset for x in data_x]
            data_x_last = dx_shift
        plt.errorbar(data_x_last, data_y, std_y, color=color, fmt='.', label=label, **line_style)

    plt.grid()
    plt.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5)
    if title is not None:
        plt.title(title)
    plt.xticks(data_x)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if save_path is not None:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print('\tsaved to {}.png'.format(save_path))
    plt.pause(0.0001)
    if show_plot:
        plt.show(block=True)
    plt.cla()
    return


def histogram(values: np.array, title: str, save_path: str = None, bins_n: int = 50):
    """ plots a histogram """
    plt.hist(values, bins_n, density=False, facecolor='blue', alpha=0.75)
    plt.xlabel('Values')
    plt.ylabel('Bin Count')
    plt.title(title)
    plt.grid(True)
    if save_path is not None:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        print('\tsaved to {}.png'.format(save_path))
    plt.show()
    plt.cla()
    return


def compare_images_sets(set_a, set_b, title: str = None):
    """
    build for images BEFORE transform:
    notice images should be in the format:
        gray scale mnist: [number of images, 28, 28]
        RGB  Cifar10    : [number of images, 32, 32, 3]

    :param set_a: array (nd\torch) of images
    :param set_b: array (nd\torch) of images
    :param title: plot title
    plot set a of images in row 1 and set b in row 2
    set_a and set_b can be ndarray or torch arrays
    example:
        from torchvision import datasets
        # choose data set - both work
        # data_root = path to the data else download
        data_root = '../../2019SGD/Datasets/'
        # dataset = datasets.MNIST(root=data_root, train=False, download=False)
        dataset = datasets.CIFAR10(root=data_root, train=False, download=False)
        set_a = dataset.data[:3]
        set_b = dataset.data[10:50]
        compare_images_sets(set_a, set_b)
        set_a = dataset.data[0:3]
        set_b = dataset.data[0:3]
        compare_images_sets(set_a, set_b)
    """
    n_cols = max(set_a.shape[0], set_b.shape[0])
    fig, axes = plt.subplots(nrows=2, ncols=n_cols, sharex='all', sharey='all', figsize=(15, 4))
    for images, row in zip([set_a, set_b], axes):
        for img, ax in zip(images, row):
            ax.imshow(np.squeeze(img), cmap='gray')
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
    if title is not None:
        plt.title(title)
    plt.show()
    return


def compare_images_multi_sets_squeezed(sets_dict: dict, title: str = None) -> str:
    """
    build for images AFTER transform:
    notice images should be in the format:
        gray scale mnist: [number of images, 1, 28, 28]
        RGB  Cifar10    : [number of images, 3, 32, 32]

    :param sets_dict: each entry in dict is title, set of images(np/tensor)
    :param title: for plot
    :return str with details which set in each row
    plot sets of images in rows
    example:
        import torch
        from torchvision import datasets
        import torchvision.transforms as transforms
        transform = transforms.Compose([transforms.ToTensor(), ])
        # choose data set - both work
        # data_root = path to the data else download
        data_root = '../../2019SGD/Datasets/'
        # dataset = datasets.MNIST(root=data_root, train=False, download=False, transform=transform)
        dataset = datasets.CIFAR10(root=data_root, train=False, download=False, transform=transform)
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True, num_workers=2)
        images32, labels = iter(data_loader).next()

        images = images32[:16]  # imagine the first 16 are base images and predicted_images are the model output
        predicted_images = images32[16:32]
        d = {'original_data': images, 'predicted_data': predicted_images}
        print(compare_images_multi_sets_squeezed(d))
    """
    from wizzi_utils import torch_tools as tt
    from torchvision.utils import make_grid
    import torch
    for k, v in sets_dict.items():
        if isinstance(sets_dict[k], np.ndarray):
            sets_dict[k] = tt.numpy_to_torch(sets_dict[k])

    all_sets = None
    msg = ''
    set_len = 0
    msg_base = 'row {}: {}, '

    for i, (k, v) in enumerate(sets_dict.items()):
        all_sets = v if all_sets is None else torch.cat((all_sets, v), 0)
        msg += msg_base.format(i, k)
        set_len = v.shape[0]

    grid_images = make_grid(all_sets, nrow=set_len)
    if title is not None:
        plt.title(title)
    plt.axis('off')
    plt.imshow(np.transpose(tt.torch_to_numpy(grid_images), (1, 2, 0)))
    plt.show()
    return msg


def render(block: bool = False, pause: float = 0.0001):
    plt.draw()
    plt.show(block=block)
    plt.pause(pause)
    return


# 3d plots
def plot_3d_iterative_figure(
        scatter_dict: dict,
        main_title: str = None,
        resize: float = 0,
        plot_location: str = None,
        x_y_z_lims: list = None,
        fig_face_color: str = None,
        ax_background: str = None,
        ax_labels_and_ticks_c: str = None,
        add_center: dict = None,
        zoomed: bool = False,
        view: dict = None,
        render_d: dict = None
) -> (matplotlib.figure, Axes3D, Path3DCollection, FigureCanvasTkAgg):
    """
    THIS is for building a figure with 1 or more subplots that changes each iteration.
        this function just builds the frame. use update_subplots to insert\change the data of the scatters
    :param scatter_dict: dict with mandatory entries of the main scatter
        e.g. {'c': 'b', 'marker_size': 1, 'marker': 'o', 'label': 'MVS'} # c for color
    :param main_title:
    :param resize: if not 0, figure size *= resize
    :param plot_location: top_right, top_center, top_left, bottom_right, bottom_center, bottom_left or None
    :param x_y_z_lims: limits of x, y and z axes. list of 6 ints: x_left, x_right, y_bottom, y_top, z_in, z_out
    :param fig_face_color: color of the whole background - default is white
    :param ax_background: color of the axes background - default is white
    :param ax_labels_and_ticks_c: color of the ticks and axes labels
    :param add_center: dict. if not None - add center with the params in the dict
        e.g. add_center = {'c': 'orange', 'marker': 'x', 'marker_size': 150, 'label': 'Scene Center'}
    :param zoomed: bool - full screen or not
    :param view: dict - view onto the world. e.g. {'azim': 90.0, 'elev': -100.0}
    :param render_d: dict - if not None: show plot
        block mandatory. pause optional.
        e.g. render = {'block': False, 'pause': 0.0001}
    :return:
    figure
    axes3d
    Path3DCollection (pointer to the scatter data) - used for updating
    FigureCanvasTkAgg - used to change title
    see full example in update_3d_scatters comments
    """
    plt.close('all')
    figsize = (6.4, 4.8) if resize == 0 else (6.4 * resize, 4.8 * resize)  # default figsize=(6.4, 4.8)
    fig = plt.figure(figsize=figsize)
    fig_canvas = fig.canvas
    ax = Axes3D(fig)
    if fig_face_color is not None:
        ax.set_facecolor(fig_face_color)

    if ax_background is not None:
        ax_background = get_RGBA_color(ax_background)
        ax.w_xaxis.set_pane_color(ax_background)
        ax.w_yaxis.set_pane_color(ax_background)
        ax.w_zaxis.set_pane_color(ax_background)

    if main_title is not None:
        fig.suptitle(main_title)
    if plot_location is not None:
        move_plot(fig, where=plot_location)

    if x_y_z_lims is not None:
        ax.set_xlim3d(left=x_y_z_lims[0], right=x_y_z_lims[1])
        ax.set_ylim3d(bottom=x_y_z_lims[2], top=x_y_z_lims[3])
        ax.set_zlim3d(bottom=x_y_z_lims[4], top=x_y_z_lims[5])

    x_left, x_right = ax.get_xlim()
    y_bottom, y_top = ax.get_ylim()
    z_in, z_out = ax.get_zlim()

    cx = int((x_right - x_left) / 2) + x_left
    cy = int((y_top - y_bottom) / 2) + y_bottom
    cz = int((z_out - z_in) / 2) + z_in

    ax.set_xticks([x_left, cx, x_right])
    ax.set_yticks([y_bottom, cy, y_top])
    ax.set_zticks([z_in, cz, z_out])

    if ax_labels_and_ticks_c is not None:
        ax.w_xaxis.line.set_color(ax_labels_and_ticks_c)
        ax.w_yaxis.line.set_color(ax_labels_and_ticks_c)
        ax.w_zaxis.line.set_color(ax_labels_and_ticks_c)
        ax.tick_params(axis='x', colors=ax_labels_and_ticks_c)
        ax.tick_params(axis='y', colors=ax_labels_and_ticks_c)
        ax.tick_params(axis='z', colors=ax_labels_and_ticks_c)
        ax.set_xlabel("X", color=ax_labels_and_ticks_c)
        ax.set_ylabel("Y", color=ax_labels_and_ticks_c)
        ax.set_zlabel("Z", color=ax_labels_and_ticks_c)
    else:
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    if add_center is not None:
        ax.scatter(
            cx, cy, cz,
            c=add_center['c'], marker=add_center['marker'],
            s=add_center['marker_size'], label='{}({},{},{})'.format(add_center['label'], cx, cy, cz)
        )

    iterative_scatter = ax.scatter(
        0, 0, 0,
        c=scatter_dict['c'], marker=scatter_dict['marker'],
        s=scatter_dict['marker_size'], label=scatter_dict['label']
    )

    plt.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5)

    if view is not None:
        ax.view_init(azim=view['azim'], elev=view['elev'])

    if zoomed:
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')

    if render_d is not None:
        if 'pause' in render_d:
            render(block=render_d['block'], pause=render_d['pause'])
        else:
            render(block=render_d['block'])
    return fig, ax, iterative_scatter, fig_canvas


def update_3d_scatters(
        scatter: Path3DCollection,
        fig_canvas: FigureCanvasTkAgg,
        data: np.array,
        colors: [list, np.array] = None,
        new_title: str = None,
        save_img_path: str = None,
        render_d: dict = None
) -> None:
    """
    :param scatter: the data scatter obj
    :param fig_canvas: used to change title
    :param data: array of 3d data.
    :param colors: list of colors. None, 1 color or |data| colors. rgba format
    :param new_title: changed main title
    :param save_img_path: if not none, save the fig to this path
    :param render_d: dict - if not None: show plot
        block mandatory. pause optional.
        e.g. render = {'block': False, 'pause': 0.0001}
    :return:
    example

    fig, ax, iterative_scatter, fig_canvas = plot_3d_iterative_figure(
        scatter_dict={'c': 'b', 'marker_size': 100, 'marker': 'o', 'label': 'MVS'},
        main_title='3d scatter plot',
        resize=1.5,
        plot_location='top_center',
        x_y_z_lims=[-20, 20, -20, 20, -20, 20],
        fig_face_color=None,
        ax_background=None,
        ax_labels_and_ticks_c=None,
        add_center={'c': 'orange', 'marker': 'x', 'marker_size': 150, 'label': 'Scene Center'},
        zoomed=False,
        view=None,
        render_d=None
    )

    # # CUSTOM ADD ON 1 - update each round
    center_mass_x_y = {"x1": 0.05, "y1": 0.95, }
    center_mass_label_base = "(xyz)={}"
    center_mass_label = ax.text2D(
        x=center_mass_x_y['x1'],
        y=center_mass_x_y['y1'],
        s=center_mass_label_base.format(np.zeros(3)),
        transform=ax.transAxes,
        color='green'
    )

    # # CUSTOM ADD ON 2 - done once
    add_cube_around_origin(ax, edge_len=4, add_labels=False)

    # should call legend if you want custom addons in it
    # plt.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5)

    render(block=False)  # not necessary - only if you want to see the plot before first data comes

    num_points = 5
    iters = 10
    for i in range(10):
        misc_tools.sleep(seconds=1)
        data_j = misc_tools.np_random_integers(low=-15, high=15, size=(num_points, 3))
        colors = get_random_color_map(num_points)
        block = (i == iters - 1)  # last iter

        update_3d_scatters(
            scatter=iterative_scatter,
            fig_canvas=fig_canvas,
            data=data_j,
            colors=colors,
            new_title='iter {}'.format(i),
            render_d=None
        )

        # # CUSTOM ADD ON 1 - update each round
        center_mass_label.set_text(center_mass_label_base.format(np.round(np.mean(data_j, axis=0), 2)))

        render(block=block)
    """
    fig_canvas.set_window_title(new_title)
    scatter._offsets3d = data.T

    if colors is not None:
        scatter._facecolor3d = colors
        scatter._edgecolor3d = colors

    if save_img_path is not None:
        plt.savefig(save_img_path, dpi=200, bbox_inches='tight')
        print('saved to {}.png'.format(save_img_path))

    if render_d is not None:
        if 'pause' in render_d:
            render(block=render_d['block'], pause=render_d['pause'])
        else:
            render(block=render_d['block'])
    return


def plot_3d_scatter(
        scatter_dict: dict,
        data: np.array,
        colors: [list, np.array] = None,
        main_title: str = None,
        resize: float = 0,
        plot_location: str = None,
        x_y_z_lims: list = None,
        fig_face_color: str = None,
        ax_background: str = None,
        ax_labels_and_ticks_c: str = 'black',
        add_center: dict = False,
        zoomed: bool = False,
        view: dict = None,
        save_img_path: str = None,
) -> None:
    """
    see documentation in plot_3d_iterative_figure() and update_3d_scatters()

    example:
    num_points = 50
    data_j = misc_tools.np_random_integers(low=-15, high=15, size=(num_points, 3))
    plot_3d_scatter(
        scatter_dict={'c': 'b', 'marker_size': 100, 'marker': 'o', 'label': 'MVS'},
        data=data_j,
        colors=get_random_color_map(num_points),
        main_title='3d scatter plot',
        resize=1.5,
        plot_location='top_center',
        x_y_z_lims=[-20, 20, -20, 20, -20, 20],
        fig_face_color=None,
        ax_background=None,
        ax_labels_and_ticks_c=None,
        add_center={'c': 'orange', 'marker': 'x', 'marker_size': 150, 'label': 'Scene Center'},
        zoomed=False,
        view=None,
        save_img_path='./3dplot'
    )
    """
    fig, ax, iterative_scatter, fig_canvas = plot_3d_iterative_figure(
        scatter_dict=scatter_dict,
        main_title=main_title,
        resize=resize,
        plot_location=plot_location,
        x_y_z_lims=x_y_z_lims,
        fig_face_color=fig_face_color,
        ax_background=ax_background,
        ax_labels_and_ticks_c=ax_labels_and_ticks_c,
        add_center=add_center,
        zoomed=zoomed,
        view=view,
        render_d=None
    )

    update_3d_scatters(
        scatter=iterative_scatter,
        fig_canvas=fig_canvas,
        data=data,
        colors=colors,
        new_title=None,
        save_img_path=save_img_path,
        render_d={'block': True}
    )
    return


def plot_3d_cube(axes: Axes3D, cube_definition: list, color='b', label='cube', add_labels=False):
    """
    :param axes:
    :param cube_definition: list of np.arrays
        4 points of the cube (1 corner node and 3 nodes to the left right and top)
    :param color:
    :param label:
    :param add_labels: add cube corners label on figure
    :return:
    """

    points = []
    points += cube_definition
    vectors = [
        cube_definition[1] - cube_definition[0],
        cube_definition[2] - cube_definition[0],
        cube_definition[3] - cube_definition[0]
    ]

    points += [cube_definition[0] + vectors[0] + vectors[1]]
    points += [cube_definition[0] + vectors[0] + vectors[2]]
    points += [cube_definition[0] + vectors[1] + vectors[2]]
    points += [cube_definition[0] + vectors[0] + vectors[1] + vectors[2]]

    points = np.array(points)

    edges = [
        [points[0], points[3], points[5], points[1]],
        [points[1], points[5], points[7], points[4]],
        [points[4], points[2], points[6], points[7]],
        [points[2], points[6], points[3], points[0]],
        [points[0], points[2], points[4], points[1]],
        [points[3], points[6], points[7], points[5]]
    ]

    faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
    color_rgba = matplotlib.colors.to_rgba(color, alpha=0.1)
    faces.set_facecolor(color_rgba)
    axes.add_collection3d(faces)

    # Plot the points themselves to force the scaling of the axes
    axes.scatter(points[:, 0], points[:, 1], points[:, 2], s=0.1, color=color, label=label)

    if add_labels:
        for p in points:
            x, y, z = p
            text = '{},{},{}'.format(x, y, z)
            axes.text(x, y, z, text, zdir=(1, 1, 1))
    return


def add_cube3d_around_origin(axes: Axes3D, edge_len: int, add_labels: bool = False):
    """
    :param axes:
    :param edge_len: cube edge size
    :param add_labels: add cube labels on the scene
    :return:
    """
    half_edge = int(edge_len / 2)
    xyz_bot_left = np.array([-half_edge, -half_edge, -half_edge], dtype=float)
    xyz_top_left = np.copy(xyz_bot_left)
    xyz_bot_right = np.copy(xyz_bot_left)
    xyz_bot_left_depth = np.copy(xyz_bot_left)
    xyz_top_left[1] += edge_len  # add just y
    xyz_bot_right[0] += edge_len  # add just x
    xyz_bot_left_depth[2] += edge_len  # add just z

    cube_4_edges = [xyz_bot_left, xyz_top_left, xyz_bot_right, xyz_bot_left_depth]
    plot_3d_cube(
        axes,
        cube_4_edges,
        label='cube(edge={})'.format(edge_len),
        add_labels=add_labels
    )
    return


def main():
    fig, ax, iterative_scatter, fig_canvas = plot_3d_iterative_figure(
        scatter_dict={'c': 'b', 'marker_size': 100, 'marker': 'o', 'label': 'MVS'},
        main_title='3d scatter plot',
        resize=1.5,
        plot_location='top_center',
        x_y_z_lims=[-20, 20, -20, 20, -20, 20],
        fig_face_color=None,
        ax_background=None,
        ax_labels_and_ticks_c=None,
        add_center={'c': 'orange', 'marker': 'x', 'marker_size': 150, 'label': 'Scene Center'},
        zoomed=False,
        view=None,
        render_d=None
    )

    # # CUSTOM ADD ON 1 - update each round
    center_mass_x_y = {"x1": 0.05, "y1": 0.95, }
    center_mass_label_base = "(xyz)={}"
    center_mass_label = ax.text2D(
        x=center_mass_x_y['x1'],
        y=center_mass_x_y['y1'],
        s=center_mass_label_base.format(np.zeros(3)),
        transform=ax.transAxes,
        color='green'
    )

    # # CUSTOM ADD ON 2 - done once
    add_cube3d_around_origin(ax, edge_len=4, add_labels=False)

    # should call legend if you want custom addons in it
    # plt.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5)

    render(block=False)  # not necessary - only if you want to see the plot before first data comes

    num_points = 5
    iters = 10
    for i in range(10):
        misc_tools.sleep(seconds=1)
        data_j = misc_tools.np_random_integers(low=-15, high=15, size=(num_points, 3))
        colors = get_random_color_map(num_points)
        block = (i == iters - 1)  # last iter

        update_3d_scatters(
            scatter=iterative_scatter,
            fig_canvas=fig_canvas,
            data=data_j,
            colors=colors,
            new_title='iter {}'.format(i),
            render_d=None
        )

        # # CUSTOM ADD ON 1 - update each round
        center_mass_label.set_text(center_mass_label_base.format(np.round(np.mean(data_j, axis=0), 2)))

        render(block=block)
    return


if __name__ == '__main__':
    main()
