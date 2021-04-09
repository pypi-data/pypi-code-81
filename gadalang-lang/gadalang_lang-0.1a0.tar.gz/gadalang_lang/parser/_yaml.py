import sys
import asyncio
import yaml
import pygada_runtime


def main(argv, *args, **kwargs):
    async def run():
        # Read node input
        params = await pygada_runtime.read_json(sys.stdin)
        data = params.get("data", {})

        # Read from input file
        input = params.get("input", None)
        if input:
            with open(input, "r") as f:
                data = yaml.safe_load(f.read())

        # Write to output file
        output = params.get("output", None)
        if output:
            with open(output, "w+") as f:
                f.write(yaml.safe_dump(data))

        # Write node output
        pygada_runtime.write_json(sys.stdout, {"data": data})

    asyncio.run(run())
