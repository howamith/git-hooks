# Git Hooks

![CI](https://github.com/howamith/git-hooks/actions/workflows/ci.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


This repository contains a series of Git hooks that (hopefully) will increase
productivity.

The currently available hooks are:

* `commit-msg`: Check that commit messages confirm to
  [the conventional commits specification](https://www.conventionalcommits.org/),
  and do not break the 72:80/line length rule.


## Installing a hook

To install a hook simply run `make install` with the name of the hook you want
to install passed as a variable set to `true`, along with a `dest` variable set
to the path of the repo to install the hook in.

For example, to install `commit-msg` in a repo located at `/path/to/repo`,
you would do:

```shell
make install commit-msg=true dest=/path/to/my/repo
```

After which there would be a symlink from the commit message hook script in
_this_ repository, to `/path/to/repo/.git/hooks/commit-msg`.

Note that if you want to simply install **all** of the available hooks then you
can do `make install all=true dest=/path/to/repo`


## Testing hooks

Hooks will be tested on all pushes to `main`, however these tests can also be
run locally.

To install everything that's required to run the tests, there is a `venv` `make`
command that creates a virtual Python environment and installs everything that's
required in there. After this you can source that `venv` and run the tests:

```shell
make venv
. venv/bin/activate
make tests
```

Note that you can run a particular type of test in isolation, rather than
running them all at once should you want too - these are available as the
following `make` commands, with the underlying tests used corresponding to the
command name:

* `flake8`
* `black`
* `mypy`
* `pytest`
