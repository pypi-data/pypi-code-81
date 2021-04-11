from .models.reporter import Reporter
from .services.cli import cli
from .services.generate import generate
from .services.inspect import inspect_state
from .services.state import load_state
from .utils.paths import abs_from_root


def main() -> None:
    args = cli.parse_args()

    reporter = Reporter(
        args.verbose,
        args.schema,
        args.silent,
    )

    inputs, collections, schema, render_context = load_state(
        args.input
    )

    inspect_state(
        inputs, collections, schema, render_context, reporter
    )

    generate(
        args.dry_run,
        abs_from_root(args.input, inputs.output_dir),
        inputs.clear_top_level,
        inputs.protected,
        collections,
        render_context,
        [abs_from_root(args.input, i) for i in inputs.loader_paths],
        reporter,
    )


if __name__ == "__main__":
    main()
