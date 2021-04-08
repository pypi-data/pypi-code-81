#  Copyright © 2020 Hashmap, Inc
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

def header(text, level=1) -> str:
    depth = '#' * level
    return f"{depth} {text}"


def table(data) -> str:
    from tabulate import tabulate
    return tabulate(data, headers="keys", tablefmt="github", showindex=False)


def hrule() -> str:
    return "-" * 3


def blockquote(text) -> str:
    blockquoted_str = ['>' + line for line in text.split('\n')]
    return join_with_newline(blockquoted_str)


def bold(text) -> str:
    return f"**{text}**"


def italics(text) -> str:
    return f"*{text}*"


def backtics(text) -> str:
    return f"`{text}`"


def nbsp() -> str:
    return "&nbsp;"


def emsp() -> str:
    return "&emsp;"


def join_with_newline(str_list):
    return '\n'.join(str_list)
