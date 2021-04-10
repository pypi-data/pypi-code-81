class Spinner:
    spinners = {
        'classic': (['|', '/', '-', '\\'], 0.1),
        'dots': (['▫ ▫ ▫', '▪ ▫ ▫', '▫ ▪ ▫', '▫ ▫ ▪'], 0.2),
        'equal': (
            ['⁼ ⁼ ⁼ ⁼ ⁼', '= ⁼ ⁼ ⁼ ⁼', '⁼ = ⁼ ⁼ ⁼', '⁼ ⁼ = ⁼ ⁼', '⁼ ⁼ ⁼ = ⁼', '⁼ ⁼ ⁼ ⁼ ='], 0.2),

        'braille': (['⠏', '⠹', '⠼', '⠧'], 0.1),
        'braille_long': (['⡏', '⢹', '⣸', '⣇'], 0.1),
        'braille_crawl': (['⠌', '⠒', '⠡', '⠨'], 0.1),
        'braille_bounce': (['⣶', '⣭', '⠿', '⣭'], 0.1),
        'arc': (['◜', '◝', '◞', '◟'], 0.1),
        'clear_quadrants': (['◴', '◷', '◶', '◵'], 0.1),
    }

    def __iter__(self):
        self._count = 0
        return self

    def __next__(self):
        if self._count < self._spinner_len:
            spinner_instance = self._spinner[self._count]
            self._count += 1
            return spinner_instance
        raise StopIteration

    def __init__(self, style, interval=None):
        self._style = style or 'classic'

        try:
            spinner_group = self.spinners[self._style]
        except KeyError:
            spinner_group = self.spinners['classic']
        self._spinner, self.interval = spinner_group

        self._spinner_len = len(self._spinner)
