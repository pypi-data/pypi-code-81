"""
This class contains code for the tool "Orteil Idle Game Maker Code Generator".
Author: GlobalCreativeCommunityFounder
"""


# Importing necessary libraries


import sys
import os
from datetime import datetime


# Creating necessary functions to be used throughout the code generator.


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


def lets_make_a_game(game_name: str, author_name: str, description: str) -> str:
    now = datetime.now()
    return """
Let's make a game!
    name:""" + str(game_name) + """
    by:""" + str(author_name) + """
    desc:""" + str(description) + """
    created:""" + str(now.day) + """/""" + str(now.month) + """/""" + str(now.year) + """
    updated:""" + str(now.day) + """/""" + str(now.month) + """/""" + str(now.year) + """
    version:1

"""


def settings(background: str, building_cost_increase: str, building_cost_refund: str,
             spritesheet: str, stylesheet: str) -> str:
    return """
Settings
    background:""" + str(background) + """
    building cost increase:""" + str(building_cost_increase) + """
    building cost refund:""" + str(building_cost_refund) + """
    spritesheet:""" + str(spritesheet) + """
    stylesheet:""" + str(stylesheet) + """   

"""


# Creating main function used to run the tool.


def main():
    """
    This main function is used to run "Orteil Idle Game Maker Code Generator" tool.
    :return: None
    """

    print("Welcome to 'Orteil Idle Game Maker Code Generator' tool by GlobalCreativeCommunityFounder.")
    print("This tool will quickly generate Orteil Idle Game Maker code to shorten your time taken in developing ")
    print("an idle game using the tool 'Orteil Idle Game Maker'.")
    print("Enter 'Y' for yes.")
    print("Enter anything else for no.")
    continue_using: str = input("Do you want to continue using the tool 'Orteil Idle Game Maker Code Generator'? ")
    while continue_using == "Y":
        clear()
        game_script: str = ""  # initial value
        print("Welcome to 'Let's make a game!' section!")
        game_name: str = input("Please enter name of game: ")
        author_name: str = input("Please enter your name: ")
        description: str = input("Please enter description of the game: ")
        game_script += lets_make_a_game(game_name, author_name, description)

        clear()
        print("Welcome to 'Settings' section!")
        background: str = input("Please enter link to background image file: ")
        building_cost_increase: str = input("Please enter building cost increase in the game: ")
        building_cost_refund: str = input("Please enter building cost refund in the game: ")
        spritesheet: str = input("Please enter spritesheet details: ")
        stylesheet: str = input("Please enter link to stylesheet file: ")
        game_script += settings(background, building_cost_increase, building_cost_refund, spritesheet, stylesheet)

        clear()
        print("Welcome to 'Layout' section!")
        game_script += """
Layout
"""
        num_box_keys: int = int(input("How many box keys do you want? "))
        if num_box_keys > 0:
            for i in range(num_box_keys):
                box_key_name: str = input("Please enter name of box key: ")
                contains: str = input("What sections does this box key contain? ")
                header: str = input("What would you put in the header of this box key? ")
                game_script += """
        *""" + str(box_key_name) + """
            contains:""" + str(contains) + """
            header:""" + str(header) + """
                        
    """
        else:
            game_script += """
    use default
            
"""

        clear()
        print("Welcome to 'Buttons' section!")
        button_item_key: str = input("Please enter item key for the button: ")
        button_name: str = input("Please enter name of button: ")
        description: str = input("Please enter button description: ")
        on_click_effects: list = []  # initial value
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        add_on_click_effect: bool = input("Do you want to add an 'on click' effect to this button? ") == "Y"
        while add_on_click_effect:
            on_click_effect: str = input("What 'on click' effect do you want to add to this button? ")
            on_click_effects.append(on_click_effect)
            print("Enter 'Y' for yes.")
            print("Enter anything else for no.")
            add_on_click_effect = input("Do you want to add an 'on click' effect to this button? ") == "Y"

        icon: str = input("Please enter link to this button's icon: ")
        button_class: str = input("Please enter button class: ")
        icon_class: str = input("Please enter button item class: ")
        tooltip_origin: str = input("Please enter tooltip origin of this button: ")
        tooltip_class: str = input("Please enter tooltip class of this button: ")
        game_script += """
Buttons
    *""" + str(button_item_key) + """
        name:""" + str(button_name) + """
        description:""" + str(description) + """
"""

        for effect in on_click_effects:
            game_script += """
        on click:""" + str(effect) + """            
"""

        game_script += """
        icon:""" + str(icon) + """
        no text
        class:""" + str(button_class) + """
        icon class:""" + str(icon_class) + """
        tooltip origin:""" + str(tooltip_origin) + """
        tooltip class:""" + str(tooltip_class) + """
                
"""

        clear()
        print("Welcome to 'Resources' section!")
        game_script += """
Resources        
"""
        num_resources: int = int(input("How many resources do you want in your game? "))
        for i in range(num_resources):
            print("You are required to enter information about the resource you want to add.")
            resource_item_key: str = input("Please enter item key for the resource: ")
            resource_name: str = input("Please enter name of resource: ")
            description = input("Please enter description of resource: ")
            icon = input("Please enter link to the icon of the resource: ")
            resource_class: str = input("Please enter class of the resource: ")
            additional_information: str = input("Enter additional information (e.g., show earned) about the "
                                                "resource: ")
            game_script += """
    *""" + str(resource_item_key) + """
        name:""" + str(resource_name) + """
        desc:""" + str(description) + """
        icon:""" + str(icon) + """
        class:""" + str(resource_class) + """
        """ + str(additional_information) + """
"""

        game_script += """
        
Shinies
"""
        clear()
        print("Welcome to 'Shinies' section!")
        num_shinies: int = int(input("How many shinies do you want in your game? "))
        for i in range(num_shinies):
            print("You are required to enter information about the shiny you want to add.")
            shiny_item_key: str = input("Please enter item key for the shiny: ")
            on_click_effects = []  # initial value
            add_on_click_effect: bool = input("Do you want to add an 'on click' effect to this shiny? ") == "Y"
            while add_on_click_effect:
                on_click_effect: str = input("What 'on click' effect do you want to add to this shiny? ")
                on_click_effects.append(on_click_effect)
                print("Enter 'Y' for yes.")
                print("Enter anything else for no.")
                add_on_click_effect = input("Do you want to add an 'on click' effect to this shiny? ") == "Y"

            movement: str = input("Please describe the movement of the shiny: ")
            frequency: str = input("Please enter the frequency of this shiny: ")
            frequency_variation: str = input("Please enter the frequency variation of this shiny: ")
            icon = input("Please enter the link to the icon of this shiny: ")
            shiny_class: str = input("Please enter the class of this shiny: ")
            game_script += """
    *""" + str(shiny_item_key) + """
        movement:""" + str(movement) + """
        frequency:""" + str(frequency) + """
        frequency variation:""" + str(frequency_variation) + """
        icon:""" + str(icon) + """
        class:""" + str(shiny_class) + """
"""

            for effect in on_click_effects:
                game_script += """
        on click:""" + str(effect) + """                
"""

        game_script += """

Buildings
    *TEMPLATE
        on click:anim glow
        
"""

        clear()
        print("Welcome to 'Buildings' section!")
        num_buildings: int = int(input("How many buildings do you want to have in your game? "))
        for i in range(num_buildings):
            print("You are required to enter information about the building you want to add.")
            building_item_key: str = input("Please enter item key for the building: ")
            building_name: str = input("Please enter name of building: ")
            description = input("Please enter building description: ")
            icon = input("Please enter link to this building's icon: ")
            cost: str = input("Please enter cost of the building: ")
            on_tick_effects: list = []  # initial value
            add_on_tick_effect: bool = input("Do you want to add an 'on tick' effect to this building? ") == "Y"
            while add_on_tick_effect:
                on_tick_effect: str = input("What 'on tick' effect do you want to add to this building? ")
                on_tick_effects.append(on_tick_effect)
                print("Enter 'Y' for yes.")
                print("Enter anything else for no.")
                add_on_tick_effect = input("Do you want to add an 'on tick' effect to this building? ") == "Y"

            game_script += """
    *""" + str(building_item_key) + """
        name:""" + str(building_name) + """
        desc:""" + str(description) + """
        icon:""" + str(icon) + """
        cost:""" + str(cost) + """             
"""
            for effect in on_tick_effects:
                game_script += """
        on tick:""" + str(effect) + """                
"""

            print("Enter 'Y' for yes.")
            print("Enter anything else for no.")
            has_requirements: bool = input("Does this building have requirements to unlock it? ") == "Y"
            if not has_requirements:
                game_script += """
        unlocked  
                      
"""
            else:
                requirements: str = input("What requirements does this building have? ")
                game_script += """
        req:""" + str(requirements) + """

"""

        game_script += """

Upgrades
    *TEMPLATE
        on click:anim glow
                
"""

        clear()
        print("Welcome to 'Upgrades' section!")
        num_upgrades: int = int(input("How many upgrades do you want to have in your game? "))
        for i in range(num_upgrades):
            print("You are required to enter information about the upgrade you want to add.")
            upgrade_item_key: str = input("Please enter item key for the upgrade: ")
            upgrade_name: str = input("Please enter name of upgrade: ")
            description = input("Please enter description for this upgrade: ")
            icon = input("Please enter link to this upgrade's icon: ")
            cost = input("Please enter this upgrade's cost: ")
            passive_effects: list = []  # initial value
            print("Enter 'Y' for yes.")
            print("Enter anything else for no.")
            add_passive_effect: bool = input("Do you want to add a passive effect to this upgrade? ") == "Y"
            while add_passive_effect == "Y":
                passive_effect: str = input("Please enter a passive effect you want to add to this upgrade:")
                passive_effects.append(passive_effect)
                print("Enter 'Y' for yes.")
                print("Enter anything else for no.")
                add_passive_effect = input("Do you want to add a passive effect to this upgrade? ") == "Y"

            requirements: str = input("Please enter the requirements to unlock this upgrade: ")
            game_script += """
    *""" + str(upgrade_item_key) + """
        name:""" + str(upgrade_name) + """
        desc:""" + str(description) + """
        icon:""" + str(icon) + """
        cost:""" + str(cost) + """
        req:""" + str(requirements) + """
"""

            for effect in passive_effects:
                game_script += """
        passive:""" + str(effect) + """                

"""

        game_script += """

Achievements
    *TEMPLATE
        on click:anim glow

"""

        clear()
        print("Welcome to 'Achievements' section!")
        num_achievements: int = int(input("How many achievements do you want to have in your game? "))
        for i in range(num_achievements):
            print("You are required to enter information about the achievement you want to add.")
            achievement_item_key: str = input("Please enter item key for the achievement: ")
            achievement_name: str = input("Please enter name of achievement: ")
            description = input("Please enter description for this achievement: ")
            icon = input("Please enter link to this achievement's icon: ")
            requirements: str = input("Please enter the requirements to get this achievement: ")
            game_script += """
    *""" + str(achievement_item_key) + """
        name:""" + str(achievement_name) + """
        desc:""" + str(description) + """
        icon:""" + str(icon) + """
        req:""" + str(requirements) + """

"""

        game_file = open(str(game_name) + ".txt", "w+")
        game_file.write(game_script)
        print("'Orteil Idle Game Maker' code is successfully generated! The code is in the file '"
              + str(game_name) + ".txt'.")
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_using = input("Do you want to continue using the tool 'Orteil Idle Game Maker Code Generator'? ")
    sys.exit()


# Calling the main function.


if __name__ == '__main__':
    main()
