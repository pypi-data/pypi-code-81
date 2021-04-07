"""
    lager.ble.commands

    Commands for BLE
"""
import re
import click
from texttable import Texttable
from ..context import get_default_gateway

@click.group(name='ble')
def ble():
    """
        Lager BLE commands
    """
    pass

ADDRESS_NAME_RE = re.compile(r'\A([0-9A-F]{2}-){5}[0-9A-F]{2}\Z')

def check_name(device):
    return 0 if ADDRESS_NAME_RE.search(device[1]) else 1

@ble.command('scan')
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected')
def scan(ctx, gateway):
    """
        Scan for BLE devices
    """
    if gateway is None:
        gateway = get_default_gateway(ctx)

    session = ctx.obj.session
    resp = session.ble_scan(gateway)

    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 'i'])
    table.set_cols_align(["l", "r"])
    table.add_row(['Name', 'Address'])

    devices = sorted(resp.json().items(), key=check_name, reverse=True)

    for address, name in devices:
        table.add_row([name, address])
    click.echo(table.draw())
