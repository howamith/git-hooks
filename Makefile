.PHONY: test


install:
	@if [ "$(all)" == "true" ] || [ "$(commit-msg)" == "true" ]; then \
		ln -s $(realpath hooks)/commit_msg.py \
			  $(realpath ${dest})/.git/hooks/commit-msg; \
	fi

venv:
	@test -d venv || ( \
		python3 -m venv venv \
		&& . venv/bin/activate \
		&& pip install -r requirements.txt \
	)

test: flake8 black mypy pytest

flake8:
	@flake8 --ignore=E203 --docstring-convention google hooks tests

black:
	@black --line-length 79 --check hooks tests

mypy:
	@mypy --ignore-missing-imports hooks tests

pytest:
	@pytest -vv --failed-first --durations=10 $(test)
