from PygFW.Text.Character import CharacterCollection, Character
from PygFW import Entity
from PygFW.Data import DataContainer
from PygFW.Constants import *
from PygFW.Event import Eventifies
from PygFW.Volatile import default_clock
import pygame

default_font_path = 'Assets/Fonts/NotoSerif/NotoSerif-Bold.ttf'

def draw_text_absolute(surface, text = 'A', position: [int, int] = (0, 0), colour: [int, int, int] = (255, 255, 255), font_path: str = default_font_path, font_size: int = 18):

    # TODO make a place to store fonts to be reused to reduce lag

    font = pygame.font.Font(font_path, font_size)
    text_display = font.render(text, True, colour)
    # TODO incorporate drawing text into textfield character
    surface.blit(text_display, position)

class TextFieldStringConstructor(DataContainer):

    def __init__(self, string: str, colour: [int, int, int] = (255, 255, 255), font_path: str = default_font_path, font_size: int = 18):

        DataContainer.__init__(self)

        self.colour = colour
        self.font_path = font_path
        self.font_size = font_size

        [self.add(TextFieldCharacter(character, self.colour, self.font_path, self.font_size)) for character in string]

    @property
    def _string_(self):

        string = ''

        for character in self._list_:

            string += character.character

        return string

    @property
    def rgb(self):

        return self.colour

    @property
    def font(self):

        return self.font_path, self.font_size

class TextFieldCharacter(Character):

    def __init__(self, character, colour: [int, int, int] = (255, 255, 255), font_path: str = default_font_path, font_size: int = 18):

        Character.__init__(self, character)
        self.colour = colour
        self.font_path = font_path
        self.font_size = font_size

        self.constructed = self.construct()

    @property
    def rgb(self):

        return self.colour

    @property
    def font(self):

        return self.font_path, self.font_size

    @property
    def rect(self):

        return self.constructed.get_rect()

    def fade(self, fade_amount):

        self.constructed.set_alpha(fade_amount)

    def construct(self):

        # TODO make global font bank
        font = pygame.font.Font(self.font_path, self.font_size)
        return font.render(self.character, True, self.colour)

    def draw(self, surface, position):

        surface.blit(self.constructed, position)


class TextFieldCharacterCollection(CharacterCollection):

    def __init__(self, characters: [TextFieldCharacter, ]):

        CharacterCollection.__init__(self, characters)

    @property
    def width(self):

        combined_width = 0

        for character in self.characters._list_:

            combined_width += character.rect.width

        return combined_width

    @property
    def height(self):

        max_height = 0

        for character in self.characters._list_:

            if (height := character.rect.height) > max_height:

                max_height = height

        return max_height


    def draw(self, surface, position):

        x, y = position

        for character in self.characters._list_:

            character.draw(surface, (x, y))

            x += character.rect.width + 1

    def concatenate(self, character_collection: CharacterCollection):

        print(character_collection)

        for character in character_collection.characters._list_:

            self.characters.add(character)

    def truncate(self, size=48):

        removed_characters = CharacterCollection()

        while self.width > size:

            removed_characters.characters.add(self.characters.remove_index(-1, True))

        return removed_characters if removed_characters.characters.size > 0 else None



class TextFieldBoxEntity(Entity):

    def __init__(self, scene_surface, background_sprites, relative_text_spawn: [int, int] = (5, 5), character_collection: CharacterCollection = CharacterCollection(), spawn: [int, int] = (0, 0)):

        Entity.__init__(self, scene_surface=scene_surface, sprites=background_sprites, spawn=spawn)

        self.string = TextFieldCharacterCollection([])
        self.string.concatenate(character_collection)

        self.relative_text_spawn = relative_text_spawn

    def draw(self):

        #self.sprites.front.draw(self, self.scene.engine_surface.pygame_surface, self.relative_position)

        text_x, text_y = self.relative_position
        rel_x, rel_y = self.relative_text_spawn

        text_x += rel_x
        text_y += rel_y

        self.string.draw(self.scene.engine_surface.pygame_surface, (text_x, text_y))

class TextAlertBoxEntity(TextFieldBoxEntity):

    def __init__(self, scene_surface, background_sprites, relative_text_spawn: [int, int] = (5, 5), character_collection: CharacterCollection = CharacterCollection(), spawn: [int, int] = (0, 0), fade_ferocity: int = 1, fade_interval: int = 1):

        TextFieldBoxEntity.__init__(self, scene_surface=scene_surface, background_sprites=background_sprites, relative_text_spawn=relative_text_spawn, spawn=spawn, character_collection=character_collection)
        self.opacity = 255
        self.fade_ferocity = fade_ferocity
        self.fade_interval = fade_interval

    def update(self):

        if default_clock.milliseconds % self.fade_interval == 0:

            self.opacity -= self.fade_ferocity

        for character in self.string.characters._list_:

            character.fade(self.opacity)

        if self.opacity < 0:

            @Eventifies(scene=self.scene, listener=None)
            def remove_self(scene, event):
                scene.entities.remove(scene.entities.get_tag(self), True)

            self.scene.engine_surface.single_events.add(remove_self)

class TextFieldGrid:

    def __init__(self):

        self._entity_grid = []