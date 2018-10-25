lint-along
===============

Lint and commit with an adjusted linting song as message.


Why?
----

I always make some stupid mistakes against the style guide, and because I never bothered to fix my half-baked linter
setup for VIM and I apparently feel too smart for githooks, I always end up linting my code after I made it into a PR.

So instead of giving those commits a bland message I opted for some music inspired titles, and lint-along was born.


Installation
------------

pip:

.. code:: bash

    pip install lint-along

From source:

.. code:: bash

    python setup.py install

Usage
-----

Execute `lint-along` in a git enabled directory.

.. code:: bash

    lint-along


Playlist
--------

The hits that make bland linting commits :sparkles:

`Spotify <https://open.spotify.com/user/tobi.beernaert/playlist/7e3T6T18e4JVl01Vasgf3m?si=qvLwEknoQqSD5kMabwxoEA>`_

Todo
====

- Pass the linter command via [yet another] config file.
- Some documentation would be nice
- Some tests would also be nice
- Add more songs




disclaimer: probably really buggy, so use with cautious.
