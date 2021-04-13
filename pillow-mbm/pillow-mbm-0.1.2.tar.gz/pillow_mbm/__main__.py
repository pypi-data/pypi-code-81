import pathlib
import os
import click
from typing import List
from PIL import Image
import pillow_mbm


def get_decoded_extensions(feature: str = 'open') -> List[str]:
    """Gets a list of extensions for Pillow formats supporting a supplied feature"""
    Image.init()
    extensions = Image.EXTENSION
    formats = getattr(Image, feature.upper()).keys()

    return [ext for ext, fmt in extensions.items() if fmt in formats]


decoded_extensions = get_decoded_extensions('save')


# noinspection PyUnusedLocal
def validate_decoded_extension(ctx, param, value) -> str:
    """Check if an extension for a decoded image is valid"""
    if value[0] != '.':
        value = '.' + value

    if value not in decoded_extensions:
        raise click.BadParameter(f'Invalid extension for decoded file. Valid extensions are:\n{decoded_extensions}')

    return value


def path_pairs(inputs, output, suffix, extension):
    if len(inputs) < 1:
        raise click.BadArgumentUsage('No input files were provided.')

    inpaths = [pathlib.Path(i) for i in inputs]

    if not output:
        # decode in place
        return [(inpath, inpath.with_name(inpath.stem + suffix + extension)) for inpath in inpaths]

    else:
        outpath = pathlib.Path(output)
        if outpath.is_file():
            # decode to a file
            if len(inputs) > 1:
                raise click.BadOptionUsage('output', 'Output is a single file, but multiple input files were provided.')
            if outpath.suffix not in decoded_extensions:
                raise click.BadOptionUsage('output', f'File has incorrect extension for decoded file. Valid extensions are:\n{decoded_extensions}')

            return [(inpath, outpath) for inpath in inpaths]
        else:
            # decode to directory
            return [(inpath, outpath / (inpath.stem + suffix + extension)) for inpath in inpaths]


@click.command()
@click.option('-f/-F', '--flip/--no-flip', default=True, show_default=False, help="Vertically flip image after converting.")
@click.option('-r', '--remove', is_flag=True, help="Remove input images after converting.")
@click.option('-s', '--suffix', type=str, default='', help="Suffix to append to output file(s). Ignored if output is a single file.")
@click.option('-x', '--extension',
              callback=validate_decoded_extension,
              type=str, default='.png', show_default=True,
              help="Extension to use for output. Ignored if output is a single file. Output filetype is deduced from this")
@click.option('-o', '--output',
              type=click.Path(writable=True), default=None,
              help="Output file or directory. If outputting to a file, input filenames must be only a single item. By default, files are decoded in place.")
@click.option('-v', '--verbose', is_flag=True, help="print more information")
@click.argument('filenames', nargs=-1, type=click.Path(exists=True, readable=True, dir_okay=False))
@click.version_option(version=pillow_mbm.__version__)
def convert_mbm(flip, remove, suffix, extension, output, verbose, filenames):
    """Decode Kerbal Space Program MBM files"""

    pairs = path_pairs(filenames, output, suffix, extension)

    with click.progressbar(pairs, show_eta=False, show_pos=True, item_show_func=lambda x: f'{x[0]}->{x[1]}' if x else '') as bar:
        if verbose:
            bar.is_hidden = True

        for inpath, outpath in bar:
            image = Image.open(inpath)

            if flip:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)

            image.save(outpath)

            if remove:
                os.remove(inpath)

            if verbose:
                print(f'Converting: {inpath} -> {outpath}')

    if verbose:
        print(f'Done: converted {len(pairs)} files')


if __name__ == '__main__':
    convert_mbm()
