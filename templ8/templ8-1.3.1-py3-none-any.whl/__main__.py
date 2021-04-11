from .models.reporter import Reporter
from .models.state import State
from .services.cli import cli
from .services.generate import generate
from .utils.paths import abs_from_root


def main() -> None:
    args = cli.parse_args()

    reporter = Reporter(
        args.verbose,
        args.schema,
        args.silent,
    )

    state = State.load(args.input)
    state.inspect(reporter)

    generate(
        args.dry_run,
        abs_from_root(args.input, state.inputs.output_dir),
        state,
        reporter,
    )


if __name__ == "__main__":
    main()
