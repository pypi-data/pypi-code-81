#!/usr/bin/env python3
#   encoding: utf-8

# This is a parser-based, web-enabled narrative.
# Copyright (C) 2021 D E Haynes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import sys
import time

# import logging
# logging.basicConfig(level=logging.DEBUG)

from tos.story import Story


def parser():
    rv = argparse.ArgumentParser()
    rv.add_argument(
        "--debug", action="store_true", default=False,
        help="Write generated dialogue for debugging."
    )
    rv.add_argument(
        "--quick", action="store_true", default=False,
        help="Don't perform timed animations."
    )
    rv.add_argument(
        "--state", type=int, default=1,
        help="Apply state to the story."
    )
    return rv


def main(opts):
    name = input("Enter your character's first name: ") or "Francis"
    story = Story()
    bookmark = story.enact(opts.state, player_name=name, description="Theatre of Spud")

    lines = []
    while story.bookmark.drama.active:
        presenter = story.represent(lines)
        if opts.debug:
            print(presenter.text, file=sys.stderr)
            print(*story.bookmark.drama.ensemble, sep="\n", file=sys.stderr)
        for frame in presenter.frames:
            animation = presenter.animate(frame, dwell=presenter.dwell, pause=presenter.pause)
            if not animation:
                continue
            for line, duration in story.render_frame_to_terminal(animation):
                print(line, "\n")
                if not opts.quick:
                    time.sleep(duration)

        bookmark = story.update(presenter.index)
        if bookmark:
            presenter = story.represent(lines)
            if opts.debug:
                print(*story.bookmark.drama.ensemble, sep="\n", file=sys.stderr)
        story.input = input("{0} ".format(story.prompt)).strip() or story.input
        fn, args, kwargs = story.bookmark.drama.interpret(story.bookmark.drama.match(story.input))
        try:
            lines = list(story.bookmark.drama(fn, *args, **kwargs))
        except TypeError as e:
            if opts.debug:
                print(e, file=sys.stderr)
            lines = [story.refusal.format(story.input)]
        finally:
            story.bookmark.folder.metadata.update(
                story.bookmark.drama.interlude(story.bookmark.folder, presenter.index)
            )


def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
