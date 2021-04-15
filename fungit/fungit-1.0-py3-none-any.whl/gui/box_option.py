import os
import math

from fungit.shared import GitType
from .box.navigation_box import NavBox
from .box.git_box import GIT_BOXS
from .box.content_box import ContentBox


def update_git_box_w_h():
    w, h = os.get_terminal_size()

    _selected_type = NavBox.current
    limit_w = math.floor(w / 3)

    if w < 90 or h < 8:
        # TODO: need create error box and show...
        pass

    elif h <= 20:
        _old = None
        for sub in GIT_BOXS:
            sub.x = 1
            sub.w = limit_w

            if not _old:
                sub.y = 1
            else:
                sub.y = _old.y + _old.h
            _old = sub

            if sub.genre & _selected_type:
                sub.h = h - (1 * 4) - 1
            else:
                sub.h = 1

    elif h <= 25:
        _old = None
        for sub in GIT_BOXS:
            sub.x = 1
            sub.w = limit_w

            if not _old:
                sub.y = 1
            else:
                sub.y = _old.y + _old.h
            _old = sub

            if sub.genre & _selected_type:
                sub.h = h - (3 * 4) - 1
            else:
                sub.h = 3

    else:
        temp_x = GIT_BOXS[0].x = 1
        temp_y = GIT_BOXS[0].y = 1
        temp_w = GIT_BOXS[0].w = limit_w
        temp_h = GIT_BOXS[0].h = 3

        if _selected_type & GitType.STASH:
            _split_h, _less = divmod(h - 4, 4)
        else:
            _split_h, _less = divmod(h - 7, 3)

        for idx, sub in enumerate(GIT_BOXS[1:-1]):
            sub.x = 1
            sub.y = temp_y + temp_h
            sub.w = limit_w
            sub.h = _split_h + (1 if _less > idx else 0)

            temp_x, temp_y, temp_w, temp_h = sub.x, sub.y, sub.w, sub.h

        GIT_BOXS[-1].x = 1
        GIT_BOXS[-1].y = temp_y + temp_h
        GIT_BOXS[-1].w = limit_w
        if _selected_type & GitType.STASH:
            GIT_BOXS[-1].h = _split_h
        else:
            GIT_BOXS[-1].h = 3


def create_content_box():
    w, h = os.get_terminal_size()
    limit_w = math.floor(w / 3)

    ContentBox.x = limit_w + 1
    ContentBox.y = 1
    ContentBox.w = w - limit_w
    ContentBox.h = h - 1

    # ContentBox.create_profile()
    # ContentBox.generate()
    # ContentBox.update()

    # BOXS[ContentBox.name] = ContentBox


def initial_git_box(update_data: bool = True, lazy_render: bool = False):
    update_git_box_w_h()  # update all nav box (w)idth and (h)eigth.
    create_content_box()

    for sub in GIT_BOXS:
        if update_data:
            sub.fetch_data()
        sub.generate()
        sub.create_profile()
        sub.update()
        if not lazy_render:
            sub.render()
