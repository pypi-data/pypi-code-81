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

import numbers
import random

from turberfield.dialogue.types import Stateful

from tos.calls import Calls
from tos.knowledge import Knowledge
from tos.lights import Lights
from tos.map import Map
from tos.mixins.helpful import Helpful
from tos.mixins.moving import Moving
from tos.mixins.patrolling import Patrolling
from tos.mixins.telegraph import Telegraph
from tos.mixins.types import Awareness
from tos.mixins.types import Artifact
from tos.mixins.types import Character
from tos.mixins.types import Mode
from tos.mixins.types import Significance
from tos.types import Motivation


class FirstPositions:

    def build(self, ensemble=None, **kwargs):
        yield from super().build(ensemble)

        yield Character(names=["Edward Lionheart"]).set_state(
            Awareness.ignorant, Motivation.leader, self.nav.Location.corridor
        )

        if not ensemble:
            player_name = kwargs.get("player_name", "Alan")
            self.player = Character(names=[player_name]).set_state(Mode.playing, self.nav.Location.car_park)
            yield self.player


class Act01(FirstPositions, Lights, Patrolling, Helpful):

    @property
    def turns(self):
        return len([i for i in self.history
                    if i.fn not in (self.do_help, self.do_history, self.do_hint)])

    def build(self, ensemble=None, **kwargs):
        for obj in super().build(ensemble):
            if "fuse" in getattr(obj, "names", []): obj.state = self.nav.Location.lighting
            if "lights" in getattr(obj, "names", []): obj.state = self.nav.Location.foyer

            if "Edward Lionheart" in obj.names:
                self.patrols.update(self.build_patrols(
                    Patrolling.Patrol(
                        obj, [self.nav.Location.wings, self.nav.Location.foyer], 1)
                ))

            yield obj

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        lights = next(iter(self.lookup["lights"]))
        state = lights.get_state(Significance)
        if isinstance(state, numbers.Number):
            lights.state = Significance.notknown
        elif lights.get_state(Significance) == Significance.indicate:
            lights.state = Significance.emphasis
        return rv


class Act03(Calls, Patrolling, Helpful):

    def __call__(self, fn, *args, **kwargs):
        phone = next(iter(self.lookup["phone"]))
        for line in super().__call__(fn, *args, **kwargs):
            if "ring" in line and not phone.state % 2:
                continue
            else:
                yield line

    def build(self, ensemble=None, **kwargs):
        for obj in super().build(ensemble):
            if obj.get_state(Mode) == Mode.playing:
                obj.state = self.nav.Location.foyer

            names = getattr(obj, "names", [])
            if "Edward Lionheart" in names:
                self.patrols.update(self.build_patrols(
                    Patrolling.Patrol(
                        obj,
                        [self.nav.Location.corridor, self.nav.Location.backstage, self.nav.Location.costume],
                        1
                    )
                ))
            elif "phone" in names:
                obj.detail.update({
                    0: ["The telephone is mounted on the wall.", "It's a grey rotary telephone."],
                    Significance.indicate: ["The phone is ringing."],
                })
                self.messengers.append(
                    Telegraph.Messenger(obj, [
                        Knowledge.Message(
                            Knowledge.Noun("Angela Grant", "f"), (Knowledge.Noun("Daniel", "m"),),
                            (
                                "{nouns[0].name}'s Dad has managed to get in to the football tonight.",
                                "{nouns[0].name}'s going with him."
                            ),
                            ("It's only a few lines, but who could fill in for {tags[1]}?",),
                            ("the Officer", "Danny")
                        ),
                        Knowledge.Message(
                            Knowledge.Noun("Sarah Scott", "f"), (Knowledge.Noun("Michael", "m"),),
                            (
                                "{nouns[0].name} has been asking to go to the match all weekend.",
                                "We were in the Cedar Tree and got hold of some tickets.",
                            ),
                            ("Can someone else play {tags[0]}?.",),
                            ("Bluntschli", "Mikey")
                        ),
                        Knowledge.Message(
                            Knowledge.Noun("Paul Robbins", "m"), (Knowledge.Noun("Hayley", "f"),),
                            (
                                "I've decided to take {nouns[0].name} to the football this evening.",
                                "She's really looking forward to seeing Bruce Grobbelaar."
                            ),
                            ("One of the other girls might like to do it.",),
                            ("Louka", "Hayley")
                        ),
                    ], 1, period=2)
                )
                obj.state = self.nav.Location.office

            yield obj

        yield Character(names=["Man's Voice"]).set_state(Motivation.father)
        yield Character(names=["Woman's Voice"]).set_state(Motivation.mother)
        yield Character(names=["Spud"]).set_state(
            Awareness.ignorant, Motivation.acting, self.nav.Location.backstage
        )

    def interlude(self, folder, index, **kwargs):
        rv = super().interlude(folder, index, **kwargs)
        for obj in (i for i in self.ensemble if isinstance(i, Character)):
            if obj.get_state(Significance) == Significance.indicate:
                obj.state = Significance.emphasis
        return rv

    def do_go(self, this, text, /, *args, locn: Map.Location):
        """
        enter {locn.value[0]}
        enter {locn.value[1]}
        enter {locn.value[2]}
        go {locn.value[0]} | go to {locn.value[0]}
        go {locn.value[1]} | go to {locn.value[1]}
        go {locn.value[2]} | go to {locn.value[2]}

        """
        yield from super().do_go(this, text, locn=locn)

    def do_look(self, this, text, *args):
        """
        look | look around

        """
        yield from super().do_look(this, text, *args)
        artifacts = [
            i for i in self.ensemble
            if isinstance(i, Artifact)
            and self.player.get_state(self.nav.Location) == i.get_state(self.nav.Location)
        ]
        if artifacts:
            yield random.choice(["In view:", "We can see:"])
            yield from ("* {0.names[0]}".format(i) for i in artifacts)

    def do_receive_call(self, this, text, /, *args, obj: Artifact):
        """
        answer {obj.names[0]} | answer the {obj.names[0]}
        get {obj.names[0]} | get the {obj.names[0]}
        pick up {obj.names[0]} | pick up the {obj.names[0]}

        """
        msg = self.messengers[0].messages[0]
        pronoun = "She" if msg.nouns[0].gender == "f" else "He"
        yield from super().do_receive_call(this, text, obj=obj)
        if msg.attribution.gender == "f":
            relation = random.choice([f"{msg.nouns[0].name}'s Mom", f"I'm {msg.nouns[0].name}'s Mother"])
            speaker = "[MOTHER]_"
        else:
            relation = random.choice([f"{msg.nouns[0].name}'s Dad", f"I'm {msg.nouns[0].name}'s Father"])
            speaker = "[FATHER]_"
        yield speaker
        yield ""
        yield "    Hello, it's {0.attribution.name}{1}".format(
            msg, random.choice([" here.", " speaking.", ", who's that please?"])
        )
        yield "    {0}.".format(relation)
        yield ""

        yield "[PLAYER]_"
        yield ""
        yield "    {0}{1}, {2} {3.player.name}.".format(
            random.choice(["Hello, ", "Hi ", ""]),
            msg.attribution.name.split()[0],
            random.choice(["it's", "this is"]),
            self
        )
        yield ""
        yield speaker
        yield ""
        yield "    {0}".format(
            random.choice(["Ever so sorry.", "Just to let you know", "Apologies for the short notice."])
        )
        yield from ("    {0}".format(i) for i in Knowledge.intentions(msg))
        yield "    {0}".format(random.choice(
                ["Hope that's OK.", "Will you be able to manage?", f"{pronoun}'ll be fine for tomorrow though."],
        ))
        yield ""
        yield random.choice(list(Knowledge.implications(msg)))
