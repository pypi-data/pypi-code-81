from flask_scenario_testing.analysis.Results import Results
import matplotlib.colors as mcolors


class ReportSection(object):

    def __init__(self):
        self.color_idx = 0

    def next_color(self) -> str:
        colors = list(mcolors.TABLEAU_COLORS.items())

        c = colors[self.color_idx][0]

        self.color_idx += 1

        return c

    def print(self, results: Results):
        pass

    def print_row(self, cols, col_widths: []):
        for idx, col in enumerate(cols):
            print(str(col).ljust(col_widths[idx]), end='')

        print()

    def print_separator(self, length=40):
        print('-' * length)

    def table(self, headers, data):
        print('| ' + ' | '.join(headers) + ' | ')
        print('| ' + ' | '.join(['-' * max(1, len(header)) for header in headers]) + ' | ')

        for row in data:
            print('| ' + ' | '.join([str(item) for item in row]) + ' | ')

        print()

    def heading(self, text, level=1):
        print('#' * level + ' ' + text)

    def add_figure(self, figure):
        figure.show()
