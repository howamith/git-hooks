# Git Hooks

This repository contains a series of Git hooks that (hopefully) will increase
productivity.

The currently available hooks are:

* `commit-msg`: Check that commit messages confirm to
  [the conventional commits specification](https://www.conventionalcommits.org/),
  and do not break the 72:80/line length rule.


# Installing a hook

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
