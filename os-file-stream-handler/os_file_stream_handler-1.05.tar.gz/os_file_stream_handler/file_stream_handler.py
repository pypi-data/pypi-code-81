####################################################
# this is just a simple file stream handling script#
####################################################


# will read a file from a path
def read_text_file(file_path, drop_new_lines=False):
    with open(file_path, 'r') as fd:
        reader = fd.readlines()
    lines = list(reader)
    if drop_new_lines:
        for i in range(0, len(lines)):
            lines[i] = lines[i].replace('\n', '')
    return lines


# will read a binary file (usually file which contains bytes)
def read_binary_file(file_path, bytes_count=None):
    in_file = open(file_path, "rb")
    if bytes_count:
        data = in_file.read(bytes_count)
    else:
        data = in_file.read()
    in_file.close()
    return data


# will write bytes to a file
def write_bytes_to_file(data, output_path):
    from os_file_handler import file_handler as fh
    if not fh.is_dir_exists(fh.get_parent_path(output_path)):
        fh.create_dir(fh.get_parent_path(output_path))
    with open(output_path, 'wb') as output:
        output.write(data)


# for text files you should look for the right initials
def compress_data_to_file(dst_file, data, write_type='wb'):
    import gzip

    with gzip.open(dst_file, write_type) as f:
        f.write(data)


def compress_text_file_to_file(src_file, dst_file):
    data = "".join(read_text_file(src_file)).encode("utf8")
    compress_data_to_file(dst_file, data, write_type='wb')


# will read a compressed file. rb stands for 'read binary'
# for text files you should look for the right initials
def read_compressed_file(file_path, read_type='rb'):
    import gzip

    with gzip.open(file_path, read_type) as f:
        return f.read()


# will write a content to a file (str or array of strings)
def write_file(file_path, content):
    with open(file_path, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_path)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        if isinstance(content, str):
            f.write(content)
        if isinstance(content, list):
            for line in content:
                if not str(line).endswith('\n'):
                    line += '\n'
                f.write(line)


# will replace a bunch of chars in a file
def replace_text_in_file(file_src, file_dst, old_expression, new_expression, replace_whole_line=False, cancel_if_exists=False):
    lines = read_text_file(file_src, drop_new_lines=True)

    if cancel_if_exists and is_line_exists_in_text(new_expression, lines=lines):
        return
    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for line in lines:

            if old_expression in line:
                if replace_whole_line:
                    if new_expression == '':
                        continue
                    else:
                        line = new_expression
                else:
                    line = line.replace(old_expression, new_expression)
            f.write(f'{line}\n')


# will delete a line contains an expression from a text
def delete_line_in_file(file_src, file_dst, expression):
    replace_text_in_file(file_src, file_src, expression, '', True)


# will add text below some other text in a file
def append_text_below_line_in_file(file_src, file_dst, below_line, new_expression, cancel_if_exists=False):
    lines = read_text_file(file_src, drop_new_lines=True)

    if cancel_if_exists and is_line_exists_in_text(new_expression, lines=lines):
        return
    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for i in range(0, len(lines)):
            f.write(f'{lines[i]}\n')
            if below_line in lines[i]:
                f.write(f'{new_expression}\n')


# will add text above some other text in a file
def append_text_above_line_in_file(file_src, file_dst, above_line, new_expression, cancel_if_exists=False):
    lines = read_text_file(file_src, drop_new_lines=True)
    if cancel_if_exists and is_line_exists_in_text(new_expression, lines=lines):
        return

    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for i in range(0, len(lines)):
            if above_line in lines[i]:
                f.write(f'{new_expression}\n')
            f.write(f'{lines[i]}\n')


# will check if line exists in a file
def is_line_exists_in_text(line_to_find, file_src=None, lines=None):
    if file_src:
        lines = read_text_file(file_src)
    for line in lines:
        if line_to_find in line:
            return True
    return False


# will delete a text in a range
def delete_text_range_in_file(file_src, file_dst, from_text, to_text, include_bundaries=False):
    lines = read_text_file(file_src, drop_new_lines=True)

    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        from_text_found = False
        done = False
        for i in range(0, len(lines)):
            if done:
                f.write(f'{lines[i]}\n')
                continue
            if from_text in lines[i]:
                from_text_found = True
                if include_bundaries:
                    f.write(f'{lines[i]}\n')
            if from_text_found and to_text in lines[i]:
                done = True
                if include_bundaries:
                    f.write(f'{lines[i]}\n')
            if not from_text_found:
                f.write(f'{lines[i]}\n')


def clear_text_from_last(lines, text):
    for i in reversed(range(0, len(lines))):
        found = False
        if text in lines[i]:
            found = True
        lines.pop(-1)
        if found:
            return lines
