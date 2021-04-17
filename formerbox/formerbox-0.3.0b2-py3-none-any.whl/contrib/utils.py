import difflib
import re
from itertools import zip_longest
from typing import Any, Dict, Iterable, List, Text

from formerbox.utils import iter_stride
from formerbox.utils.code_tokenizer import tokenize_python


def make_batches(sequences: Iterable[Any], batch_size: int) -> Iterable[List[Any]]:
    return iter_stride(sequences, batch_size, stride=0)


def flatten(nested_dict: Dict[Any, List[Any]]) -> List[Dict[Any, Any]]:
    result: List[Dict[Text, Any]] = []
    packed_values = zip_longest(*nested_dict.values())
    for packed_value in packed_values:
        flat_dict: Dict[Text, Any] = {}
        for key, value in zip(nested_dict.keys(), packed_value):
            if value is None:
                continue
            flat_dict[key] = value
        result.append(flat_dict)
    return result


# pylint: disable=too-many-arguments
class DiffPreprocessor:
    def __init__(
        self,
        fromfile_start_token: Text = "<fromfile>",
        fromfile_close_token: Text = "</fromfile>",
        tofile_start_token: Text = "<tofile>",
        tofile_close_token: Text = "</tofile>",
        del_start_token: Text = "<del>",
        del_close_token: Text = "</del>",
        add_start_token: Text = "<add>",
        add_close_token: Text = "</add>",
    ) -> None:
        self.fromfile_start_token = fromfile_start_token
        self.fromfile_close_token = fromfile_close_token
        self.tofile_start_token = tofile_start_token
        self.tofile_close_token = tofile_close_token
        self.del_start_token = del_start_token
        self.del_close_token = del_close_token
        self.add_start_token = add_start_token
        self.add_close_token = add_close_token

        self.special_tokens = [
            self.fromfile_start_token,
            self.fromfile_close_token,
            self.tofile_start_token,
            self.tofile_close_token,
            self.del_start_token,
            self.del_close_token,
            self.add_start_token,
            self.add_close_token,
        ]

    def preprocess(
        self,
        source_content: Text,
        target_content: Text,
        source_file: Text,
        target_file: Text,
        context_size: int,
        lineterm: Text = "",
    ) -> Text:
        source_lines = self.tokenize(source_content)
        target_lines = self.tokenize(target_content)

        lines_diff = difflib.unified_diff(
            source_lines,
            target_lines,
            source_file,
            target_file,
            n=context_size,
            lineterm=lineterm,
        )

        lines: List[Text] = []
        for line in lines_diff:
            if not source_file and line.startswith("---"):
                continue
            if not target_file and line.startswith("+++"):
                continue

            line = self.prepare_line(line)
            if not line:
                continue

            lines.append(line)

        return " ".join(lines)

    def prepare_line(self, line: Text) -> Text:
        # replace source file with `fromfile_token`
        replacement = r"{}\g<1>{}".format(
            self.fromfile_start_token, self.fromfile_close_token
        )
        line = re.sub(r"^\-\-\- (.*)", replacement, line)

        # replace target file with `tofile_token`
        replacement = r"{}\g<1>{}".format(
            self.tofile_start_token, self.tofile_close_token
        )
        line = re.sub(r"^\+\+\+ (.*)", replacement, line)

        # remove common metadata string
        line = re.sub(r"@@ .* @@", r"", line)

        # replace diff `-` tokens with `del_token`
        replacement = r"{} \g<1>".format(self.del_start_token)
        line = re.sub(r"^\-(.*)", replacement, line)

        # replace diff `+` tokens with `add_token`
        replacement = r"{} \g<1>".format(self.add_start_token)
        line = re.sub(r"^\+(.*)", replacement, line)

        return line.lstrip()

    def tokenize(self, content: Text) -> List[Text]:
        tokens = tokenize_python(content)
        program = " ".join(tokens)
        program = program.replace("<newline>", "<newline>\\n")
        clean_lines = [line.strip() for line in program.split("\\n")]
        return clean_lines
