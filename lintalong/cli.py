import json
import click
import os
import pkg_resources
import random
import subprocess
import yaml
from array import array
from pathlib import Path
from git import Repo, Commit
from lintalong.no_changed_files_exception import NoChangedFilesException
from lintalong.song import Song


@click.command()
def cli():
    config = load_config()

    try:
        run_linter(config['linter'])
    except subprocess.CalledProcessError as error:
        if error.returncode == 2:
            click.echo("Linting command \"{0}\" does not exist".format(" ".join(error.cmd)))
        return

    repo = Repo(os.getcwd())

    try:
        stage_linted_files(repo)
    except NoChangedFilesException:
        click.echo("Nothing to lint along")
        return

    song = fetch_random_song()
    commit = commit_linted_files(song=song, repo=repo)

    totals = commit.stats.total

    result_message = "[{0} {1}] {2}\r\n{3} file(s) changed, {4} insertions(+), {5} deletions(-)".format(
        repo.active_branch,
        str(commit),
        commit.summary,
        totals['files'],
        totals['insertions'],
        totals['deletions']
    )

    click.echo(message=result_message)


def load_config():
    config = yaml.safe_load(pkg_resources.resource_string(__name__, 'config.yml'))

    if Path("~/.lint-along.yml").is_file():
        with open("~/.lint-along.yml", "r") as handle:
            config.update(yaml.safe_load(handle.read()))

    if Path(".lint-along.yml").is_file():
        with open(".lint-along.yml", "r") as handle:
            config.update(yaml.safe_load(handle.read()))

    return config


def run_linter(linter_cmd: array):
    with open(os.devnull, 'w') as FNULL:
        subprocess.run(linter_cmd, stdout=FNULL, stderr=subprocess.STDOUT, check=True)


def stage_linted_files(repo: Repo):
    changed_files = repo.untracked_files
    changed_files += [item.a_path for item in repo.index.diff(None)]

    if len(changed_files) == 0:
        raise NoChangedFilesException

    index = repo.index
    for file in changed_files:
        index.add([file])


def commit_linted_files(song: Song, repo: Repo) -> Commit:
    message = ":musical_note: {0}\r\n\r\nBy {1} [{2}]".format(song.lyrics, song.artist, song.yt_link)
    commit = repo.index.commit(message=message)

    return commit


def fetch_random_song() -> Song:
    song = json.loads(pkg_resources.resource_string(__name__, 'lyrics_pool.json'))['pool']
    return Song.new(random.choice(song))


if __name__ == '__main__':
    cli()
