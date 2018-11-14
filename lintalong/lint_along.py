import json
import os
import random
import subprocess
import pkg_resources
from typing import Dict
from git import Repo, Commit
from lintalong.song import Song


class LinterDoesNotExistException(Exception):
    def __init__(self, message, command: Dict):
        message = "Linting command \"{0}\" does not exist".format(" ".join(command))

        super().__init(message)


class NoChangedFilesException(Exception):
    pass


class LintAlong:
    def __init__(self, config: Dict, repo: Repo):
        self.config = config
        self.repo = repo

    def lint(self):
        try:
            with open(os.devnull, 'w') as FNULL:
                subprocess.run(self.config['linter'], stdout=FNULL, stderr=subprocess.STDOUT, check=True)
        except subprocess.CalledProcessError as error:
            if error.returncode == 2:
                raise LinterDoesNotExistException(command=self.config['linter'])
            raise error

    def stage_files(self):
        changed_files = self.repo.untracked_files
        changed_files += [item.a_path for item in self.repo.index.diff(None)]

        if len(changed_files) == 0:
            raise NoChangedFilesException

        for file in changed_files:
            self.repo.index.add([file])

    def commit_files(self) -> Commit:
        song = self._fetch_random_song()
        message = ":musical_note: {0}\r\n\r\nBy {1} [{2}]".format(song.lyrics, song.artist, song.yt_link)

        return self.repo.index.commit(message=message)

    def format_commit(self, commit: Commit) -> str:
        totals = commit.stats.total

        return "[{0} {1}] {2}\r\n{3} file(s) changed, {4} insertions(+), {5} deletions(-)".format(
            self.repo.active_branch,
            str(commit),
            commit.summary,
            totals['files'],
            totals['insertions'],
            totals['deletions']
        )

    def _fetch_random_song(self) -> Song:
        song = json.loads(pkg_resources.resource_string(__name__, 'lyrics_pool.json'))['pool']
        return Song.new(random.choice(song))
