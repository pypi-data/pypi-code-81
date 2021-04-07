import numpy as np
import pandas as pd


class SpecParser:
    def __init__(self, file_path: str):
        self._file_path = file_path
        with open(file_path) as file:
            self._file_lines = [line.rstrip() for line in file]

        self._scan_index = {}
        self._index_scans()
        print(f'{self.number_of_scans} scans found in {file_path}')

    @property
    def scan_info(self):
        return self._scan_index

    @property
    def number_of_scans(self):
        return len(self._scan_index)

    def extract_scan(self, scan_number):
        column_names = self._extract_column_names(scan_number)
        data = self._extract_scan_data(scan_number)
        return pd.DataFrame(data=data, columns=column_names)

    def _extract_column_names(self, scan_number):
        header_idx = self._scan_index[str(scan_number)]['data_start']
        column_names = self._file_lines[header_idx].lstrip('#L ').split('  ')
        return column_names

    def _extract_scan_data(self, scan_number):
        data_idx = self._scan_index[str(scan_number)]['data_start'] + 1
        data = []
        while True:
            try:
                line = self._file_lines[data_idx]
            except IndexError:
                break
            else:
                if line.startswith('#') or not line:
                    break
            data.append(line.split())
            data_idx += 1
        return np.array(data, dtype=float)

    def _search_for_next_scan(self, start_index=0):
        index = start_index
        while True:
            try:
                line = self._file_lines[index]
            except IndexError:
                return None
            else:
                if line.startswith('#S'):
                    return index
            index += 1

    def _index_scans(self, start_index=0):
        start_index = self._search_for_next_scan(start_index)
        if start_index is None:
            return
        scan = {'start_index': start_index}
        index = start_index
        while True:
            try:
                line = self._file_lines[index]
            except IndexError:
                scan['end_index'] = index - 1
                break
            if line.startswith('#S'):
                line_parts = line.split()
                scan_number = line_parts[1]
                scan['spec_command'] = ' '.join(line_parts[2:])
            elif line.startswith('#D'):
                line_parts = line.split()
                scan['time'] = ' '.join(line_parts[1:])
            elif line.startswith('#L'):
                scan['data_start'] = index
            elif not line.strip():
                scan['end_index'] = index - 1
                break
            index += 1
        self._scan_index[scan_number] = scan
        self._index_scans(scan['end_index'] + 1)
