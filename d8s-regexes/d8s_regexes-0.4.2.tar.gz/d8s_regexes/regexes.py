import re
from typing import List

from d8s_lists import deduplicate, longest


def is_regex(possible_regex: str) -> bool:
    """Determine whether or not the possible_regex is a valid regex."""
    try:
        re.compile(possible_regex)
    except re.error:
        return False
    else:
        return True


# TODO: I'd like to rename this function
def regex_closest_match(regex: str, string: str) -> str:
    """Find the longest version of regex that matches something in string."""
    try:
        match = re.match(regex, string)
    except re.error:
        regex = regex_closest_match(regex[:-1], string)
    else:
        if match is None:
            regex = regex_closest_match(regex[:-1], string)
    return regex


def regex_simplify(regex: str, *, consolidation_threshold: int = 5) -> str:
    """Clean and simplify a regex to a more efficient form."""
    from itertools import islice

    regex_section_pattern = r'(?<!\\)\[[\w\- ]+\]'
    regex_sections = re.findall(regex_section_pattern, regex)

    # collapse regexes into generalized sections
    for section in regex_sections:
        section_content = section.strip('[').strip(']')
        if len(section_content) > consolidation_threshold:
            new_section = '[a-zA-Z0-9]'
            regex = regex.replace(section, new_section, 1)

    # find the regex sections again because some sections may have been collapsed in the previous code
    regex_section_pattern = r'(?<!\\)\[[\w\- ]+\]'
    regex_sections = re.findall(regex_section_pattern, regex)

    # merge repeated sections
    sections = iter(enumerate(regex_sections))
    for index, section in sections:
        repetition_count = 1
        repeated_section = section
        for s in regex_sections[index + 1 :]:  # noqa: E203
            # if this section equals the current section...
            if s == section:
                repetition_count += 1
                repeated_section += s
            # if the next section is not equal, we can move on
            else:
                break

        if repetition_count != 1:
            new_section = section + '{' + str(repetition_count) + '}'
            regex = regex.replace(repeated_section, new_section, 1)
            next(islice(sections, index, repetition_count), None)

    return regex


def regex_create(inputs: List[str], *, simplify_regex: bool = True, consolidation_threshold: int = 5) -> str:
    """Create a regex that matches all of the inputs."""
    regex = ''
    longest_input = longest(inputs)

    for index, char in enumerate(longest_input):
        chars_at_index = []
        value_is_optional = False
        for i in inputs:
            if index < len(i):
                chars_at_index.append(i[index])
            else:
                value_is_optional = True

        chars_match = True
        for char_at_index in chars_at_index:
            if char_at_index != char:
                chars_match = False
                break

        if not chars_match:
            new_regex_section = ''.join(sorted(deduplicate(chars_at_index)))
            regex += '[{}]'.format(new_regex_section)
        else:
            regex += char

        if value_is_optional:
            regex += '?'

    if simplify_regex:
        return regex_simplify(regex, consolidation_threshold=consolidation_threshold)
    else:
        return regex
