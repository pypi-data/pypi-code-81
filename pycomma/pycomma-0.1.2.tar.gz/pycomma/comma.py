import json
import typing
import statistics
import os

class Comma:
    def __init__(
        self, 
        filepath, 
        includes_header=True, 
        delimiter=",", 
    ):
        self.__filepath = filepath

        if isinstance(includes_header, bool):
            self.__includes_header = includes_header
        else:
            raise ValueError("Wrong argument type for includes_header")

        self.__delimiter = delimiter

        self.__csv_file = None
        self.__data = []
        self.__header = []
        self.__prepared = False
        self.__json = {}
        self.__primary_column_name = None
        self.__configs = {
            "success_messages": True,
            "max_row_display": 5
        }

        self.__internal_configs = {
            "row_display_start": -1,
            "row_display_end": -1
        }
        
        # self.__history WIP

    def __repr__(self):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")\

        rows = self.__data[:self.__configs["max_row_display"]]

        if self.__internal_configs["row_display_start"] != -1 and \
            self.__internal_configs["row_display_end"] != -1:
            start = self.__internal_configs["row_display_start"]
            end = self.__internal_configs["row_display_end"]

            rows = self.__data[start:end+1]

        longest_values = {}

        for column_name in self.__header:
            longest_values[column_name] = len(column_name)

        for i in range(len(rows)):
            for j in range(len(rows[i])):
                if self.__header[j] not in longest_values:
                    longest_values[self.__header[j]] = len(rows[i][j])
                else:
                    if longest_values[self.__header[j]] < len(rows[i][j]):
                        longest_values[self.__header[j]] = len(rows[i][j])

        # length of placeholder must be same as length of overflow_sign
        output = ""
        placeholder = " "
        terminal_column_size = os.get_terminal_size().columns
        overflow_sign = "->"

        for key in list(longest_values.keys()):
            diff = len(key) - longest_values[key]

            if diff < 0:
                column = key + (" " * abs(diff))

                reserved = len(output) + len(column) + len(overflow_sign)
                if reserved <= terminal_column_size:
                    output += column
                else:
                    output += overflow_sign
                    break

            elif diff >= 0:
                reserved = len(output) + len(key) + len(overflow_sign)
                if reserved <= terminal_column_size:
                    output += key
                else:
                    output += overflow_sign
                    break

            output += placeholder

        output += "\n"
        
        longest_values_keys = list(longest_values.keys())
        for i in range(len(rows)):
            row = rows[i]
            row_string = ""

            for j in range(len(row)):
                key = longest_values_keys[j]
                diff = len(row[j]) - longest_values[key]

                if diff < 0:
                    column = row[j] + (" " * abs(diff))

                    reserved = len(row_string)+len(column)+len(overflow_sign)
                    if reserved <= terminal_column_size:
                        row_string += column
                        row_string += placeholder
                    else:
                        row_string += overflow_sign
                        break
                        
                elif diff >= 0:
                    reserved = len(row_string) + len(key) + len(overflow_sign)
                    if reserved <= terminal_column_size:
                        row_string += row[j]
                        row_string += placeholder
                    else:
                        row_string += overflow_sign
                        break
            
            row_string += "\n"
            output += row_string
            
            self._set_internal_config("row_display_start", -1)
            self._set_internal_config("row_display_end", -1)

        return output

    def show(self, row_start=-1, row_end=-1):
        self._set_internal_config("row_display_start", row_start)
        self._set_internal_config("row_display_end", row_end)
        return self

    def _set_internal_config(self, config, value):
        if not isinstance(config, str):
            raise ValueError("Argument config must be a string")

        if config in self.__internal_configs:
            if config == "row_display_start":
                if not isinstance(value, int):
                    raise ValueError("Config must be of int type")
                else:
                    self.__internal_configs[config] = value
            elif config == "row_display_end":
                if not isinstance(value, int):
                    raise ValueError("Config must be of int type")
                else:
                    self.__internal_configs[config] = value
        else:
            raise ValueError("Invalid configuration " + str(config))

    def get_configs(self) -> dict:
        return self.__configs

    def get_config(self, config) -> dict:
        if str(config) not in self.__configs:
            raise ValueError("Config does not exist")
        return {"config": str(config), "value": self.__configs[str(config)]}

    def set_config(self, config, value):
        if not isinstance(config, str):
            raise ValueError("Argument config must be a string")

        if config in self.__configs:
            if config == "success_messages":
                if not isinstance(value, bool):
                    raise ValueError("Config must be of bool type")
                else:
                    self.__configs[config] = value
            elif config == "max_row_display":
                if not isinstance(value, int):
                    raise ValueError("Config must be of int type")
                else:
                    self.__configs[config] = value
        else:
            raise ValueError("Invalid configuration " + str(config))

    def get_data(self) -> list:
        return self.__data

    def get_header(self) -> list:
        return self.__header

    def set_header(self, header):
        if self.__includes_header:
            msg = "Manual header configuration is disabled. "
            msg += "To enable, use includes_header=False in constructor."
            raise Exception(msg)
        else:
            if not isinstance(header, list):
                msg = "Incorrect format detected for header. "
                msg += "Please configure as a list of strings."
                raise Exception(msg)

            self.__header = header

    def _get_primary_column_name(self) -> str:
        return str(self.__primary_column_name)

    def get_primary(self) -> str:
        return self._get_primary_column_name()

    def _set_primary_column_name(self, column_name):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        if str(column_name) not in self.__header:
            raise ValueError("Column " + str(column_name) + " does not exist")
            
        num_of_rows = self.dimension()["rows"]
        if len(self.unique_values(str(column_name))) == num_of_rows:   
            self.__primary_column_name = str(column_name)
        else:
            msg = "Duplicate values detected. "
            msg = "Primary column cannot have duplicate values"
            raise Exception(msg)

    def _get_prepared(self) -> bool:
        return self.__prepared

    def _get_includes_header(self) -> bool:
        return self.__includes_header

    def _manual_load_csv_for_testing(self):
        csv_file = open(self.__filepath, mode="r", encoding="utf-8")
        self.__csv_file = csv_file

    def _manual_close_file_for_testing(self):
        if not self.file_is_closed():
            self.__csv_file.close()

    def assign_primary(self, column_name):
        self._set_primary_column_name(column_name)

    def dimension(self) -> dict:
        return {"columns": len(self.__header), "rows": len(self.__data)}

    def _extract_header_from_file(self) -> list:
        header_line = self.__csv_file.readline()
        header = header_line.split(self.__delimiter)
        header[-1] = header[-1].replace("\n", "")
        return header

    def _extract_data_from_file(self) -> list:
        data = []
        line = self.__csv_file.readline()

        while line:
            line = line.split(self.__delimiter)
            line[-1] = line[-1].replace("\n", "")
            data.append(line)
            line = self.__csv_file.readline()

        return data

    def prepare(self):
        if not self.__prepared:
            csv_file = open(self.__filepath, mode="r", encoding="utf-8")
            self.__csv_file = csv_file

            if self.__includes_header:
                self.__header = self._extract_header_from_file()
            else:
                if len(self.__header) == 0 or self.__header is None:
                    msg = "No header detected. "
                    msg += "Please manually set a header before prepare call."
                    self.__csv_file.close()
                    raise Exception(msg)

            self.__data = self._extract_data_from_file()

            self.__csv_file.close()
            self.__prepared = True
            if self.__configs["success_messages"]:
                print("Preparation complete")
        else:
            self.__csv_file.close()
            raise Exception("Redundant preparation call detected")

    def _to_json(self) -> dict:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        json = {"headers": self.__header, "data": []}
        for row in self.__data:
            json_obj = {}

            for i, h in enumerate(self.__header):
                json_obj[h] = row[i]

            json["data"].append(json_obj)
            
        self.__json = json

    def get_json(self) -> dict:
        self._to_json()
        return self.__json

    def _join_with_delimiter(self, a_list, delimiter=",") -> str:
        return str(delimiter.join(a_list))

    def save_as_csv(self, file_path=None, delimiter=","):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        if file_path is None:
            file_path = "data.csv"

        with open(file_path, "w") as csv_file:
            header_string = self._join_with_delimiter(self.__header, delimiter)
            header_string += "\n"
            csv_file.write(header_string)

            for row in self.__data:
                row_string = self._join_with_delimiter(row, delimiter)
                row_string += "\n"
                csv_file.write(row_string)

        if self.__configs["success_messages"]:
            print("Export completed at " + file_path)

    def save_as_json(self, file_path=None):
        if not self.__json or self.__json is None:
            self._to_json()
        
        if file_path is None:
            file_path = "data.json"

        with open(file_path, "w") as json_file:
            json.dump(self.__json, json_file)

        if self.__configs["success_messages"]:
            print("Export completed at " + file_path)

    def file_is_closed(self) -> bool:
        return self.__csv_file.closed

    def append(self, column_name, str_to_append):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        try:
            str_to_append = str(str_to_append)
        except ValueError:
            raise ValueError("Argument cannot be converted to String")

        for i in range(len(self.__data)):
            self.__data[i][column_idx] += str_to_append

        if self.__configs["success_messages"]:
            print("Value append completed.")

    def replace(self, column_name, substr, replace_with):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        try:
            substr = str(substr)
            replace_with = str(replace_with)
        except:
            raise ValueError("Arguments cannot be converted to String")

        for i in range(len(self.__data)):
            if substr.lower() in self.__data[i][column_idx].lower():
                temp = self.__data[i][column_idx].lower()
                self.__data[i][column_idx] = temp.replace(substr, replace_with)

        if self.__configs["success_messages"]:
            print("Value replace completed.")

    def change(
        self, 
        column_name, 
        changing, 
        change_to, 
        case_matters=False
        ):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        try:
            changing = str(changing)
            change_to = str(change_to)
        except:
            raise ValueError("Arguments cannot be converted to String")

        for i in range(len(self.__data)):
            if case_matters:
                if self.__data[i][column_idx] == changing:
                    self.__data[i][column_idx] = change_to
            else:
                if self.__data[i][column_idx].lower() == changing.lower():
                    self.__data[i][column_idx] = change_to

        if self.__configs["success_messages"]:
            print("Value change completed.")

    def strip(self, column_name, side="both"):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        if not isinstance(side, str):
            msg = "Invalid argument side. Must be 'both', 'right', or 'left'"
            raise ValueError(msg)

        if side == "both":
            for i in range(len(self.__data)):
                self.__data[i][column_idx] = self.__data[i][column_idx].strip()
        elif side == "right":
            for i in range(len(self.__data)):
                self.__data[i][column_idx] = self.__data[i][column_idx].rstrip()
        elif side == "left":
            for i in range(len(self.__data)):
                self.__data[i][column_idx] = self.__data[i][column_idx].lstrip()
        else:
            raise ValueError("Argument side must be 'both', 'right', or 'left'")

        if self.__configs["success_messages"]:
            print("Column strip completed.")

    def has_empty(self, column_name) -> bool:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try:
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        for i in range(len(self.__data)):
            if not self.__data[i][column_idx]:
                return True

        return False

    def fill_empty(self, column_name, fill_with):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try:
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        try:
            replace_with = str(fill_with)
        except ValueError:
            raise ValueError("Argument cannot be converted to String")

        count = 0
        for i in range(len(self.__data)):
            if not self.__data[i][column_idx]:
                if fill_with:
                    self.__data[i][column_idx] = fill_with
                else:
                    self.__data[i][column_idx] = "None"
                count += 1
        
        if self.__configs["success_messages"]:
            print("Fill Count: " + str(count))

    def sum(self, column_name, ignore_na=False) -> float:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        result = 0
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                result += num
            except ValueError:
                if not ignore_na:
                    msg = "Value at row " + str(i)
                    msg += " cannot be converted to Float. "
                    msg += "To ignore, use ignore_na=True"
                    raise ValueError(msg)
                else:
                    continue
                
        return result

    def median(self, column_name, ignore_na=False) -> float:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        converted_list = []
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                converted_list.append(num)
            except ValueError:
                if not ignore_na:
                    msg = "Value at row " + str(i)
                    msg += " cannot be converted to Float. "
                    msg += "To ignore, use ignore_na=True"
                    raise ValueError(msg)
                else:
                    continue

        converted_list.sort()
                
        return statistics.median(converted_list)

    def mean(self, column_name, ignore_na=False) -> float:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        column_values = []
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                column_values.append(num)
            except ValueError:
                if not ignore_na:
                    msg = "Value at row " + str(i)
                    msg += " cannot be converted to Float. "
                    msg += "To ignore, use ignore_na=True"
                    raise ValueError(msg)
                else:
                    continue

        return statistics.mean(column_values)

    def stdev(self, column_name, ignore_na=False) -> float:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        column_values = []
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                column_values.append(num)
            except ValueError:
                if not ignore_na:
                    msg = "Value at row " + str(i)
                    msg += " cannot be converted to Float. "
                    msg += "To ignore, use ignore_na=True"
                    raise ValueError(msg)
                else:
                    continue

        return statistics.stdev(column_values)

    def minimum(self, column_name):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        column_values = []
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                column_values.append(num)
            except ValueError:
                continue

        return min(column_values)

    def maximum(self, column_name):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        column_values = []
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                column_values.append(num)
            except ValueError:
                continue

        return max(column_values)

    def value_counts(self, column_name) -> dict:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        counts = {}
        for i in range(len(self.__data)):
            value = str(self.__data[i][column_idx])
            
            if value not in counts:
                counts[value] = 1
            else:
                counts[value] += 1

        return counts

    def unique_values(self, column_name) -> list:
        return list(self.value_counts(column_name).keys())

    def column_values(self, column_name) -> list:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        values = []
        for i in range(len(self.__data)):
            values.append(self.__data[i][column_idx])

        return values

    def change_column_name(self, column_name, change_to):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try:
            change_to = str(change_to)
        except ValueError:
            raise ValueError("Argument change_to must be a str")

        try: 
            column_idx = self.__header.index(str(column_name))
            self.__header[column_idx] = change_to

            if self.__primary_column_name == str(column_name):
                self.__primary_column_name = change_to

        except ValueError:
            print("Column does not exist")

    def add_column(self, column_name, data):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        self.__header.append(str(column_name))
        
        if not isinstance(data, list):
            raise TypeError("Data must be a list")

        if len(data) != self.dimension()["rows"]:
            raise ValueError("Length of data does not match number of rows")

        for i in range(len(self.__data)):
            self.__data[i].append(str(data[i]))

    def delete_column(self, column_name):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        for i in range(len(self.__data)):
            self.__data[i].pop(column_idx)

        self.__header.pop(column_idx)

    def rearrange_columns(self, column_names):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        if len(column_names) != len(self.__header):
            raise ValueError("Argument must be of same length as header")

        column_indices = []
        for column_name in column_names:
            try: 
                column_idx = self.__header.index(str(column_name))
                column_indices.append(column_idx)
            except ValueError:
                msg = "Column " + str(column_name) + " does not exist"
                raise ValueError(msg)

        for i in range(len(self.__data)):
            rearranged_values = [0] * len(self.__header)

            for j in range(len(self.__header)):
                rearranged_values[j] = self.__data[i][column_indices[j]]

            self.__data[i] = rearranged_values 

        if self.__configs["success_messages"]:
            print("Column rearrangement completed.")

    def switch_columns(self, x_column_name, y_column_name):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_x_idx = self.__header.index(str(x_column_name))
        except ValueError:
            raise ValueError("Column " + str(x_column_name) +" does not exist")

        try: 
            column_y_idx = self.__header.index(str(y_column_name))
        except ValueError:
            raise ValueError("Column " + str(y_column_name) +" does not exist")

        for i in range(len(self.__data)):
            value_holder = self.__data[i][column_x_idx]
            self.__data[i][column_x_idx] = self.__data[i][column_y_idx]
            self.__data[i][column_y_idx] = value_holder

        value_holder = self.__header[column_x_idx]
        self.__header[column_x_idx] = self.__header[column_y_idx]
        self.__header[column_y_idx] = value_holder

        if self.__configs["success_messages"]:
            msg = "Column " + x_column_name + " switched with " + y_column_name
            print(msg)

    def sort_by_column(self, column_name, reverse=False):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        if self.has_empty(column_name):
            raise Exception("Empty row detected. All rows must have value")

        try:
            value = float(self.__data[42][column_idx])
            numerical_column_detected = True
        except ValueError:
            numerical_column_detected = False

        data_copy = None
        if numerical_column_detected:
            if reverse:
                data_copy = sorted(
                    self.__data, 
                    key=lambda x: float(x[column_idx]))[::-1]
            else:
                data_copy = sorted(
                    self.__data, 
                    key=lambda x: float(x[column_idx]))
        else:
            if reverse:
                data_copy = sorted(
                    self.__data, 
                    key=lambda x: x[column_idx])[::-1]
            else:
                data_copy = sorted(
                    self.__data, 
                    key=lambda x: x[column_idx])

        self.__data = data_copy

        if self.__configs["success_messages"]:
            print("Sort completed")


    def column_stats(self, column_name, ignore_na=False) -> dict:
        return {
            "column_name": str(column_name),
            "mean": self.mean(column_name, ignore_na=ignore_na),
            "median": self.median(column_name, ignore_na=ignore_na),
            "stdev": self.stdev(column_name, ignore_na=ignore_na),
            "sum": self.sum(column_name, ignore_na=ignore_na),
            "minimum": self.minimum(column_name),
            "maximum": self.maximum(column_name)
        }

    def find_row(self, primary_column_value) -> int:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        if self.__primary_column_name is None:
            raise Exception("No primary column detected. Set a primary column")

        primary_column_idx = self.__header.index(self.__primary_column_name)

        row_idx = None
        for i in range(len(self.__data)):
            if self.__data[i][primary_column_idx] == str(primary_column_value):
                row_idx = i
                break
        
        if row_idx is None:
            raise Exception("Could not find row")

        return row_idx

    def find_rows(self, primary_column_values) -> list[int]:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        if self.__primary_column_name is None:
            raise Exception("No primary column detected. Set a primary column")

        if not isinstance(primary_column_values, list):
            raise Exception("Incorrect param type detected. Must be a list")

        try:
            for i in range(len(primary_column_values)):
                primary_column_values[i] = str(primary_column_values[i])
        except ValueError:
            raise ValueError("Argument cannot be converted to String")

        primary_column_idx = self.__header.index(self.__primary_column_name)

        row_indices = []
        found_matches_for = []
        for i in range(len(self.__data)):
            if self.__data[i][primary_column_idx] in primary_column_values:
                row_indices.append(i)
                found_matches_for.append(self.__data[i][primary_column_idx])

                if len(row_indices) == len(primary_column_values):
                    break

        no_matches_for = []
        if len(row_indices) != len(primary_column_values):
            for value in primary_column_values:
                if value not in found_matches_for:
                    no_matches_for.append(value)

            for non_match in no_matches_for:
                print("No match was found for primary value " + str(non_match))

        return row_indices

    def delete_row(self, row_idx) -> list[str]:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        if not isinstance(row_idx, int):
            raise ValueError("Invalid argument type. Must be integer")
        
        popped = self.__data.pop(row_idx)
        return popped

    def delete_rows(self, row_indices):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        if not isinstance(row_indices, list):
            raise ValueError("Invalid argument type. Must be a list")

        row_indices.sort(reverse=True)

        for idx in row_indices:
            self.__data.pop(idx)

        if self.__configs["success_messages"]:
            print("Successfully deleted " + str(len(row_indices)) + " rows")

    def add_row(self, data):
        if not isinstance(data, list):
            raise Exception("Incorrect param type detected. Must be a list")

        if len(data) != len(self.__header):
            raise Exception("Length of row must match the number of columns")

        self.__data.append(data)

        if self.__configs["success_messages"]:
            print("Successfully added row")

    def get(self, idx, column_names=[]) -> dict:
        if not isinstance(idx, int):
            raise ValueError("Invalid argument type idx. Must be integer")

        if not isinstance(column_names, list):
            msg = "Invalid argument type column_names. Must be list"
            raise ValueError(msg)

        result = {}
        if not column_names:
            for i in range(len(self.__header)):
                result[self.__header[i]] = self.__data[idx][i]
        else:
            column_indices = []
            for column_name in column_names:
                try: 
                    column_idx = self.__header.index(str(column_name))
                    column_indices.append(column_idx)
                except ValueError:
                    msg = "Column " + str(column_name) + " does not exist"
                    raise ValueError(msg)

            for i in range(len(column_indices)):
                result[column_names[i]] = self.__data[idx][column_indices[i]]

        return result

    def get_row_values(self, idx) -> list:
        if not isinstance(idx, int):
            raise ValueError("Invalid argument type idx. Must be integer")
            
        return self.get_data()[idx]