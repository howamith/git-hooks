#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""commit-msg Git hook script."""
from abc import ABC, abstractmethod
import sys
from typing import List, Optional, Type


class InvalidCommitMessage(Exception):
    """An exception that is raised if a commit message is invalid."""

    pass


class CommitMessageValidator(ABC):
    """An abstract base class for commit message validators."""

    def validate(self, message: str) -> None:
        """Validate a commit message.

        Args:
            message: The commit message to validate.

        Raises:
            InvalidCommitMessage: If the commit message is invalid.
        """
        # Split out the message into subject and body - which will be separated
        # by a double newline.
        parts = message.split("\n\n")
        subject, body = parts[0], parts[1] if len(parts) > 1 else None

        self._validate_subject_and_body(subject, body)

    @abstractmethod
    def _validate_subject_and_body(
        self, subject: str, body: Optional[str]
    ) -> None:
        """Validate a commit message's subject and body.

        This method MUST be implemented by `CommitMessageValidator`
        derivatives.

        Args:
            subject: The subject of the commit message to validate.
            body: The body of the commit message to validate.

        Raises:
            InvalidCommitMessage: If the commit message is invalid.
        """
        pass


class CommitMessageLengthValidator(CommitMessageValidator):
    """`CommitMessageValidator` that checks commit messages length."""

    def _validate_subject_and_body(
        self, subject: str, body: Optional[str]
    ) -> None:
        """Validate a commit message's subject and body.

        Ensures that the commit messages is no longer than 72 characters in
        length.

        Args:
            subject: The subject of the commit message to validate.
            body: The body of the commit message to validate.

        Raises:
            InvalidCommitMessage: If the commit message is invalid.
        """
        self._validate_length(
            text=subject,
            max_len=72,
            desc="Commit message" if not body else "Subject line",
        )

        if body:
            # No hard-and-fast rule for the body, but each line should be
            # limited to 80 characters.
            for line in body.split("\n"):
                self._validate_length(
                    text=line, max_len=80, desc="Line in body"
                )

    def _validate_length(self, text: str, max_len: int, desc: str) -> None:
        """Validate the length of part of a commit message.

        Args:
            text: The text to validate.
            max_len: The maximum that `text` should be.
            desc: The description of the text we're validating.
        """
        length = len(text)
        if length > max_len:
            n = length - max_len
            raise InvalidCommitMessage(
                f"{desc} longer than {max_len} characters by {n} characters."
            )


class ConventionCommitMessageValidator(CommitMessageValidator):
    """`CommitMessageValidator` that ensures commit messages are conventional.

    See https://www.conventionalcommits.org/
    """

    CONVENTION_TYPES = [
        "fix",
        "fix!",
        "feat",
        "feat!",
        "chore",
        "docs",
        "build",
        "ci",
        "style",
        "refactor",
        "test",
    ]

    def _validate_subject_and_body(
        self, subject: str, body: Optional[str]
    ) -> None:
        """Validate a commit message's subject and body.

        Ensures that the commit messages conforms to the conventional commit
        specification.

        Args:
            subject: The subject of the commit message to validate.
            body: The body of the commit message to validate.

        Raises:
            InvalidCommitMessage: If the commit message is invalid.
        """
        for ct in self.CONVENTION_TYPES:
            if subject.startswith(f"{ct}:"):
                return

        raise InvalidCommitMessage("Commit message is not conventional.")


def get_commit_message() -> str:
    """Fetch the commit message.

    Returns:
        The commit message.
    """
    commit_message_path = sys.argv[1]
    with open(commit_message_path) as f:
        return f.read()


def validate_commit_message(
    message: str, validators: List[Type[CommitMessageValidator]]
) -> None:
    """Validate a commit message.

    Args:
        message: The commit message to validate.
        validators: A list of `CommitMessageValidator` derivatives to validate
            the message with.
    """
    for v in validators:
        v().validate(message)


def main(message: str) -> int:
    """Main entry point.

    Args:
        message: The commit message to process.

    Returns:
        Exit status code (0 on success).
    """
    exit_code = 1
    try:
        validate_commit_message(
            message=message,
            validators=[
                CommitMessageLengthValidator,
                ConventionCommitMessageValidator,
            ],
        )
        exit_code = 0
    except InvalidCommitMessage as e:
        print(f"Invalid commit message: {str(e)}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main(get_commit_message()))
