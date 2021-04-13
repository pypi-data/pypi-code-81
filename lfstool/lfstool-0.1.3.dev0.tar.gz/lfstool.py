#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" FS tool to update LittleFS from the local directory
    Usage:
    lfstool.py -s /absolute_path/source -t /xxx/tmp/fs.bin --block_size=4096 --block_count 512 -v
"""
import sys

from littlefs import LittleFS
import hashlib
import os
import os.path
from os import path
import argparse
import io
import shutil

__version__ = "0.1.3-dev"
DEFAULT_DB_FILE = "lfstool.db"


if 'IDF_PATH' in os.environ:
    """It is useful on Windows to comparision paths in case-insensitive manner.
    On Unix and Mac OS X it works as `os.path.realpath()` only.
    """
    esptool_path = os.path.normcase(os.path.realpath(
        os.environ['IDF_PATH'])) + "/components/esptool_py/esptool"
    sys.path.append(esptool_path)
    # Be sure esptool from IDF_PATH is the first
    sys.path.reverse()
    print(f"WARNING: esptool taken from IDF_PATH {esptool_path}")
    import esptool
    del esptool_path
else:
    import esptool


class StorageContext:

    def __init__(self, **kwargs) -> None:
        if kwargs.get("buffer_size", 0) > 0:
            self.buffer = bytearray([0xFF] * kwargs.get("buffer_size"))
        elif isinstance(kwargs.get("buffer"), bytes):
            self.buffer = bytearray(kwargs.get("buffer"))
        else:
            raise ValueError("Missing buffer or buffer_size")
        self.prog_commands = []
        self.erase_commands = []
        self.trace_prog = kwargs.get("trace_prog", False)

    def read(self, cfg: 'LFSConfig', block: int, off: int, size: int) -> bytearray:
        start = block * cfg.block_size + off
        end = start + size
        return self.buffer[start:end]

    def prog(self, cfg: 'LFSConfig', block: int, off: int, data: bytes) -> int:
        start = block * cfg.block_size + off
        end = start + len(data)
        if self.trace_prog:
            print('LFS Prog : Block: %d, Offset: %d, Data=%r bytes' %
                  (block, off, len(data)))
            print('Address on flash: 0x%08x...' % (args.address + start))
        self.prog_commands.append({args.address + start, io.BytesIO(data)})
        self.buffer[start:end] = data
        return 0

    def erase(self, cfg: 'LFSConfig', block: int) -> int:
        start = block * cfg.block_size
        end = start + cfg.block_size
        self.erase_commands.append({args.address + start, cfg.block_size})
        self.buffer[start:end] = [0xFF] * cfg.block_size
        return 0

    def sync(self, cfg: 'LFSConfig') -> int:
        return 0


def get_esp(port, baud, connect_mode, chip='auto', skip_connect=False):
    print(f"{port}, {baud}, {connect_mode}")
    if chip not in ['auto', 'esp32', 'esp32s2', 'esp32s3beta2', 'esp32c3']:
        raise esptool.FatalError("get_esp: Unsupported chip (%s)" % chip)
    if chip == 'auto' and not skip_connect:
        _esp = esptool.ESPLoader.detect_chip(
            port, baud, connect_mode, trace_enabled=args.verbose)
    else:
        _esp = {
            'esp32': esptool.ESP32ROM,
            'esp32s2': esptool.ESP32S2ROM,
            'esp32s3beta2': esptool.ESP32S3BETA2ROM,
            'esp32c3': esptool.ESP32C3ROM,
        }.get(chip, esptool.ESP32ROM)(port, baud)
        if not skip_connect:
            _esp.connect(connect_mode)
    return _esp


def _create_littlefs_from_os_fs(folder):
    fs = LittleFS(context=StorageContext(buffer_size=args.block_size * args.block_count, trace_prog=False),
                  block_size=args.block_size, block_count=args.block_count,
                  read_size=args.read_size, prog_size=args.prog_size,
                  lookahead_size=args.lookahead_size)
    for root, dirs, files in os.walk(folder):
        for one_dir in dirs:
            fs.mkdir('/'.join((_remove_prefix(root, folder), one_dir)))
        for name in files:
            full_file_path = '/'.join((root, name))
            if full_file_path == args.local_mirror or full_file_path == args.temp_local_mirror:
                print(f"File {full_file_path} will be skipped from syncing.")
            else:
                with open(full_file_path, mode='rb') as file:  # b is important -> binary
                    with fs.open('/'.join((_remove_prefix(root, folder), name)), 'w') as fh:
                        fh.write(file.read())
    return fs


def _remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def _calculate_checksum(data: bytes) -> str:
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


def _walk_fs(fs):
    file_checksum_dict = {}
    for root, dirs, files in fs.walk('/'):
        for name in files:
            full_file_path = '/'.join((root, name))
            with fs.open(full_file_path, mode='r') as file:  # b not required, default is binary
                size = fs.stat(full_file_path).size
                digest = _calculate_checksum(file.read(size))
                if root != "/":
                    file_checksum_dict[full_file_path] = digest
                else:
                    file_checksum_dict[''.join((root, name))] = digest
    return file_checksum_dict


def _write_fs_to_file(fs, file_path):
    with open(file_path, 'wb') as fh:
        fh.write(fs.context.buffer)


def _get_extra_keys_on_left(left: dict, right: dict):
    new_items = []
    updated_items = []
    for key, value in left.items():
        if key not in right:
            print(f"File {key} missing on right side.")
            new_items.append(key)
        elif right[key] != value:
            print(f"File {key} on both sides, but differs.")
            updated_items.append(key)
    return new_items, updated_items


def _load_existing_fs(fs_path):
    with open(fs_path, mode='rb') as file:  # b is important -> binary
        return LittleFS(context=StorageContext(buffer=file.read(), trace_prog=args.verbose),
                        block_size=args.block_size, block_count=args.block_count,
                        read_size=args.read_size, prog_size=args.prog_size,
                        lookahead_size=args.lookahead_size)


def _delete_from_fs(fs: LittleFS, files_2_delete):
    for file in files_2_delete:
        fs.remove(file)


def _create_on_fs(fs: LittleFS, files_2_delete):
    for file in files_2_delete:
        source_file_path = '/'.join((args.source, file))
        with open(source_file_path, mode='rb') as source_file:  # b is important -> binary
            fs.makedirs(os.path.dirname(file), exist_ok=True)
            with fs.open(file, 'w') as fh:
                fh.write(source_file.read())


def sync_fs(esp):
    global args
    source_fs = _create_littlefs_from_os_fs(args.source)
    if path.isfile(args.local_mirror):
        local_mirror_fs = _load_existing_fs(args.local_mirror)
        source_fs_info = _walk_fs(source_fs)
        if args.verbose:
            print(f"Source fs to be synced: {source_fs_info}")
        local_mirror_fs_info = _walk_fs(local_mirror_fs)
        if args.verbose:
            print(f"local_mirror fs to be synced: {local_mirror_fs_info}")
        files_2_create, files_2_update = _get_extra_keys_on_left(
            source_fs_info, local_mirror_fs_info)
        files_2_delete, _ = _get_extra_keys_on_left(
            local_mirror_fs_info, source_fs_info)
        print(f"Files to be created: {files_2_create}")
        print(f"Files to be updated: {files_2_update}")
        print(f"Files to be deleted {files_2_delete}")
        _delete_from_fs(local_mirror_fs, files_2_delete)
        _delete_from_fs(local_mirror_fs, files_2_update)
        _create_on_fs(local_mirror_fs, files_2_create)
        _create_on_fs(local_mirror_fs, files_2_update)
        # FIXME ESP32 ROM does not support function erase_region.
        for address, size in local_mirror_fs.context.erase_commands:
            args.address = address
            args.size = size
            esptool.erase_region(esp, args)
        if len(local_mirror_fs.context.prog_commands) > 0:
            args.addr_filename = local_mirror_fs.context.prog_commands
            esptool.write_flash(esp, args)
        _write_fs_to_file(local_mirror_fs, args.temp_local_mirror)
    elif args.create:
        local_mirror_fs = source_fs
        _write_fs_to_file(local_mirror_fs, args.temp_local_mirror)
        with open(args.temp_local_mirror, mode='rb') as local_mirror_file:
            args.addr_filename = [{args.address, local_mirror_file}]
            esptool.write_flash(esp, args)
    else:
        raise FileNotFoundError(
            f"local_mirror file {args.local_mirror} does not exist.")

    _write_fs_to_file(local_mirror_fs, args.temp_local_mirror)
    print("FS successfully synced.")


class MyESP32StubLoader(esptool.ESP32ROM):
    """ Access class for ESP32 stub loader, runs on top of ROM.
    """
    FLASH_WRITE_SIZE = 0x400  # matches MAX_WRITE_BLOCK in stub_loader.c
    STATUS_BYTES_LENGTH = 2  # same as ESP8266, different to ESP32 ROM
    IS_STUB = True

    def __init__(self, rom_loader):
        self.secure_download_mode = rom_loader.secure_download_mode
        self._port = rom_loader._port
        self._trace_enabled = rom_loader._trace_enabled
        self.flush_input()  # resets _slip_reader


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LFSTool')
    parser.add_argument(
        '--source', '-s', help="Source path to update from", default=os.getcwd())
    parser.add_argument('--local_mirror', '-t',
                        help="Local mirror of the remote FS", default=f"{os.getcwd()}/{DEFAULT_DB_FILE}")
    parser.add_argument('--create', action='store_true',
                        help="Create local mirror fs if the file does not exist")
    parser.add_argument(
        '--no-stub',
        help="Disable launching the flasher stub, only talk to ROM bootloader. Some features will not be available.",
        action='store_true')
    parser.add_argument('--block_size', '-bs', type=int,
                        default='4096', help="Block size")
    parser.add_argument('--block_count', '-bc', type=int, help="Block count", default=os.environ.get('LFSTOOL_BLOCKCOUNT', 512))
    parser.add_argument('--read_size', '-rs', type=int,
                        default='4096', help="Read size buffer")
    parser.add_argument('--prog_size', '-ps', type=int,
                        default='4096', help="Prog size buffer")
    parser.add_argument('--lookahead_size', '-ls', type=int,
                        default='4096', help="Look ahead size")
    parser.add_argument('--chip', '-c',
                        help='Target chip type',
                        choices=['auto', 'esp32', 'esp32s2',
                                 'esp32s3beta2', 'esp32c3'],
                        default=os.environ.get('ESPTOOL_CHIP', 'auto'))
    parser.add_argument('--baud', '-b',
                        help='Serial port baud rate used when flashing/reading',
                        type=esptool.arg_auto_int,
                        default=os.environ.get('ESPTOOL_BAUD', 460800))

    parser.add_argument('--port', '-p',
                        help=f'Serial port device, could be taken from env ESPTOOL_PORT, if not default to {esptool.ESPLoader.DEFAULT_PORT}',
                        default=os.environ.get('ESPTOOL_PORT', esptool.ESPLoader.DEFAULT_PORT))

    parser.add_argument('--before',
                        help='What to do before connecting to the chip',
                        choices=['default_reset', 'no_reset',
                                 'esp32r1', 'no_reset_no_sync'],
                        default='default_reset')
    parser.add_argument(
        '--after', '-a',
        help='What to do after esptool.py is finished',
        choices=['hard_reset', 'soft_reset', 'no_reset'],
        default=os.environ.get('ESPTOOL_AFTER', 'hard_reset'))
    parser.add_argument('--address', help="Data partition start address", default=os.environ.get('LFSTOOL_ADDRESS'))
    compress_args = parser.add_mutually_exclusive_group(required=False)
    compress_args.add_argument('--compress', '-z',
                               help='Compress data in transfer (default unless --no-stub is specified)',
                               action="store_true", default=None)
    compress_args.add_argument('--no-compress', '-u',
                               help='Disable data compression during transfer (default if --no-stub is specified)',
                               action="store_true")
    parser.add_argument('--erase-all', '-e',
                        help='Erase all regions of flash (not just write areas) before programming',
                        action="store_true")

    """ Add common parser arguments for SPI flash properties """
    extra_keep_args = ['keep']

    parser.add_argument('--flash_freq', '-ff', help='SPI Flash frequency',
                        choices=extra_keep_args + ['40m', '26m', '20m', '80m'],
                        default=os.environ.get('ESPTOOL_FF', 'keep'))
    parser.add_argument('--flash_mode', '-fm', help='SPI Flash mode',
                        choices=extra_keep_args +
                        ['qio', 'qout', 'dio', 'dout'],
                        default=os.environ.get('ESPTOOL_FM', 'keep'))
    parser.add_argument('--flash_size', '-fs', help='SPI Flash size in MegaBytes (1MB, 2MB, 4MB, 8MB, 16M)'
                                                    ' plus ESP8266-only (256KB, 512KB, 2MB-c1, 4MB-c1), detect, or keep',
                        default=os.environ.get('ESPTOOL_FS', 'keep'))

    parser.add_argument('--spi-connection', '-sc', help='ESP32-only argument. Override default SPI Flash connection. '
                                                        'Value can be SPI, HSPI or a comma-separated list of 5 I/O numbers to use for SPI flash (CLK,Q,D,HD,CS).',
                        action=esptool.SpiConnectionAction)
    parser.add_argument('--verify', help='Verify just-written data on flash '
                                         '(mostly superfluous, data is read back during flashing)', action='store_true')
    parser.add_argument('--verbose', '-v', help='Enable verbose logging',
                        action="store_true", default=False)
    parser.add_argument('--force', help='Delete local mirror and sync all files to remote again.',
                        action="store_true", default=False)

    args = parser.parse_args()
    args.encrypt = False
    args.encrypt_files = None
    args.trace = True
    args.temp_local_mirror = args.local_mirror + ".tmp"

    if args.force and path.isfile(args.local_mirror):
        os.remove(args.local_mirror)
        # Create a new local mirror if removed
        args.create = True

    if path.isfile(args.local_mirror):
        print(
            f"Creating backup from local mirror {args.local_mirror} to {args.temp_local_mirror}")
        shutil.copy2(args.local_mirror, args.temp_local_mirror)

    if args.address:
        args.address = int(args.address, 0)
    else:
        raise ValueError("Missing address parameter")

    if args.before != "no_reset_no_sync":
        initial_baud = min(esptool.ESPLoader.ESP_ROM_BAUD,
                           args.baud)  # don't sync faster than the default baud rate
    else:
        initial_baud = args.baud
    esp = get_esp(args.port, initial_baud, args.before, args.chip)

    if esp.secure_download_mode:
        print("Chip is %s in Secure Download Mode" % esp.CHIP_NAME)
    else:
        print("Chip is %s" % (esp.get_chip_description()))
        print("Features: %s" % ", ".join(esp.get_chip_features()))
        print("Crystal is %dMHz" % esp.get_crystal_freq())
        esptool.read_mac(esp, args)

    if not args.no_stub:
        if esp.secure_download_mode:
            print(
                "WARNING: Stub loader is not supported in Secure Download Mode, setting --no-stub")
            args.no_stub = True
        else:
            esptool.ESP32ROM.STUB_CLASS = MyESP32StubLoader
            esp = esp.run_stub()

    if args.baud > initial_baud:
        try:
            esp.change_baud(args.baud)
        except esptool.NotImplementedInROMError:
            print(
                "WARNING: ROM doesn't support changing baud rate. Keeping initial baud rate %d" % initial_baud)
    if args.no_stub:
        print("Enabling default SPI flash mode...")
        # ROM loader doesn't enable flash unless we explicitly do it
        esp.flash_spi_attach(0)

    # override common SPI flash parameter stuff if configured to do so
    if hasattr(args, "spi_connection") and args.spi_connection is not None:
        if esp.CHIP_NAME != "ESP32":
            raise esptool.FatalError(
                "Chip %s does not support --spi-connection option." % esp.CHIP_NAME)
        print("Configuring SPI flash mode...")
        esp.flash_spi_attach(args.spi_connection)
    elif args.no_stub:
        print("Enabling default SPI flash mode...")
        # ROM loader doesn't enable flash unless we explicitly do it
        esp.flash_spi_attach(0)

    if hasattr(args, "flash_size"):
        print("Configuring flash size...")
        esptool.detect_flash_size(esp, args)
        if args.flash_size != 'keep':  # TODO: should set this even with 'keep'
            esp.flash_set_parameters(
                esptool.flash_size_bytes(args.flash_size))

    sync_fs(esp)

    if args.after == 'hard_reset':
        print('Hard resetting via RTS pin...')
        esp.hard_reset()
    elif args.after == 'soft_reset':
        print('Soft resetting...')
        # flash_finish will trigger a soft reset
        esp.soft_reset(False)
    else:
        print('Staying in bootloader.')
        if esp.IS_STUB:
            esp.soft_reset(True)  # exit stub back to ROM loader

    esp._port.close()

    print(
        f"Everything seems ok, writing temp file {args.temp_local_mirror} backup to local mirror {args.local_mirror}")
    shutil.move(args.temp_local_mirror, args.local_mirror)
