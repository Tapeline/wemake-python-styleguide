"""Contains command implementation."""

from wemake_python_styleguide.cli.commands.base import AbstractCommand
from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
    violation_loader,
)
from wemake_python_styleguide.cli.output import print_stderr, print_stdout


def _clean_violation_code(violation_str: str) -> int:
    """Get int violation code from str violation code."""
    violation_str = violation_str.removeprefix('WPS')
    try:
        return int(violation_str)
    except ValueError:
        return -1


class ExplainCommand(AbstractCommand):
    """Explain command impl."""

    def run(self, args) -> int:
        """Run command."""
        code = _clean_violation_code(args.violation_code)
        violation = violation_loader.get_violation(code)
        if violation is None:
            print_stderr(f'Violation "{args.violation_code}" not found')
            return 1
        message = message_formatter.format_violation(violation)
        print_stdout(message)
        return 0
