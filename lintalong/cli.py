import click
import os
import pkg_resources
import subprocess
import yaml
from typing import Dict
from pathlib import Path
from git import Repo
from lintalong.lint_along import LintAlong
from lintalong.no_changed_files_exception import NoChangedFilesException


@click.command()
def cli():
    lint_along = LintAlong(load_config(), Repo(os.getcwd()))

    try:
        lint_along.lint()
    except subprocess.CalledProcessError as error:
        if error.returncode == 2:
            click.echo("Linting command \"{0}\" does not exist".format(" ".join(error.cmd)))
        raise error

    try:
        lint_along.stage_files()
    except NoChangedFilesException:
        click.echo("Nothing to lint along")
        return

    commit = lint_along.commit_files()

    click.echo(message=lint_along.format_commit(commit))


def load_config() -> Dict:
    config = yaml.safe_load(pkg_resources.resource_string(__name__, 'config.yml'))

    if Path("~/.lint-along.yml").is_file():
        with open("~/.lint-along.yml", "r") as handle:
            config.update(yaml.safe_load(handle.read()))

    if Path(".lint-along.yml").is_file():
        with open(".lint-along.yml", "r") as handle:
            config.update(yaml.safe_load(handle.read()))

    return config


if __name__ == '__main__':
    cli()
