#!/usr/bin/env python3
# encoding: utf-8

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

import unittest

from turberfield.dialogue.model import SceneScript

from tos.acts import Act01
from tos.story import Story
from tos.mixins.types import Character
from tos.mixins.types import Motion
from tos.mixins.types import Proximity


class StoryTests(unittest.TestCase):

    def test_actions(self):
        s = Story()
        bookmark = s.build(player_name="tester")
        self.assertTrue(s.actions)
        action = next(s.actions)
        form = "\n".join(s.render_action_form(action, autofocus=True))
        self.assertIn('<label for="input-cmd-text" id="input-cmd-text-tip">&gt;</label>', form)
        self.assertIn("<fieldset>", form)
        self.assertIn("</fieldset>", form)
        self.assertIn('autofocus="autofocus"', form)
        self.assertIn('placeholder="?"', form)
        self.assertIn('pattern="[\\w ]{1,36}"', form)  # Don't forget the space
        self.assertIn('<button type="submit">Enter</button>', form, form)

    def test_build_drama(self):
        s = Story()
        drama = s.build_drama("tos.dlg.act01", ensemble=[], player_name="tester")
        self.assertIsInstance(drama.player, Character)
        self.assertIsInstance(drama, Act01)

    def test_build(self):
        s = Story()
        bookmark = s.build("tos.dlg.act01", player_name="tester")
        self.assertIsInstance(bookmark.drama.player, Character)
        self.assertIsInstance(bookmark.drama, Act01)


class TestAct1(unittest.TestCase):

    def test_patrol(self):
        story = Story()
        presenter = None
        response = []
        commands = ["wait", "next", "help", "enter foyer"] + ["w"] * 8
        story.build(player_name="tester", description="Patrol Test")
        ed = next(iter(story.bookmark.drama.lookup["Edward Lionheart"]))
        for n, cmd in enumerate(commands):
            with self.subTest(cmd=cmd, n=n):
                story.input = cmd
                fn, args, kwargs = story.bookmark.drama.interpret(story.bookmark.drama.match(cmd))
                try:
                    response = list(story.bookmark.drama(fn, *args, **kwargs))
                except TypeError:
                    response = [story.refusal.format(story.input)]
                finally:
                    if presenter:
                        story.bookmark.folder.metadata.update(
                            story.bookmark.drama.interlude(story.bookmark.folder, presenter.index)
                        )

                presenter = story.represent(response)
                for frame in presenter.frames:
                    animation = presenter.animate(frame)
                    if not animation: continue
                    lines = [line for (line, duration) in story.render_frame_to_terminal(animation)]

                story.update(presenter.index)

                if n == 1:
                    self.assertFalse(ed.get_state(Motion))
                    self.assertEqual(
                        story.bookmark.drama.nav.Location.corridor,
                        ed.get_state(story.bookmark.drama.nav.Location), ed
                    )
                    self.assertEqual(Proximity.distant, ed.get_state(Proximity), ed)
                elif cmd == "enter foyer":
                    self.assertEqual(
                        story.bookmark.drama.nav.Location.foyer,
                        story.bookmark.drama.player.get_state(story.bookmark.drama.nav.Location),
                        story.bookmark.drama.player
                    )
                    self.assertEqual(Proximity.outside, ed.get_state(Proximity), ed)
                elif n == 3:
                    self.assertEqual(Motion.patrol, ed.get_state(Motion))
                    self.assertEqual(
                        story.bookmark.drama.nav.Location.corridor,
                        ed.get_state(story.bookmark.drama.nav.Location),
                        ed
                    )
                    self.assertEqual(Proximity.outward, ed.get_state(Proximity), ed)
