import os

from dpp.core import Context
from dpp.core.plugin import PluginBuilder


def run_plugin(plugin_name, arguments):
    app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dpp")
    print(app_path)
    context = Context("net.bytebutcher.decoder_plus_plus", app_path, namespace=[])
    config = {
        "name": '_'.join(plugin_name.split("_")[:-1]),
        "type": plugin_name.split("_")[-1],
        "config": {}
    }
    output = PluginBuilder(context).build(config).run(*arguments)
    print(output)
    return output

