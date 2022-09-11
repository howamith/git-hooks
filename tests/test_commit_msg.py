"""Test for the commit-msg hook."""
import pytest

from hooks import commit_msg


@pytest.mark.parametrize(
    ("commit_message", "exit_code"),
    [
        # Just subject line - success
        ("fix: Fix a thing", 0),
        ("fix!: Fix a thing in a way that isn't backwards compatible", 0),
        ("feat: Implement a thing", 0),
        (
            "feat!: Implement a thing in a way that isn't backards compatible",
            0,
        ),
        ("chore: Do some house-keeping/ admin", 0),
        ("docs: Document some stuff", 0),
        ("build: Something to do with building a service or app", 0),
        ("ci: Please, not CodeShip", 0),
        ("style: Any colour you like", 0),
        ("refactor: Refactor some code", 0),
        ("test: All the tests", 0),
        # Subject and body - success
        (
            "feat: Implement complex thing.\n\n"
            "So we need a little more information to explain things.",
            0,
        ),
        (
            "feat: Implement a reallycomplex thing.\n\n"
            "So we need even more information to explain things, and ensure "
            "that readers of\nthe commit history understand what we've done.",
            0,
        ),
        # Just subject line - failure
        ("This isn't conventional", 1),
        (
            "fix: This _is_ conventional, but it's rather long and will "
            "result in GitHub wrapping the message when it displays it",
            1,
        ),
        (
            "This is very long _and_ it isn't conventional, so this is a "
            "double whammy of nope",
            1,
        ),
        # Subject line and body - failure
        ("This isn't conventional\n\nBut it's lengths are fine.", 1),
        (
            "fix: This _is_ conventional, but it's rather long and will "
            "result in GitHub wrapping the message when it displays it\n\n"
            "But its body is fine.",
            1,
        ),
        (
            "This is very long _and_ it isn't conventional, so this is a "
            "double whammy of nope\n\nBut its body is fine.",
            1,
        ),
        (
            "fix: This _is_ conventional\n\n"
            "And it's subject is the right length, however it's body is "
            "longer than the required 80 character limit",
            1,
        ),
        (
            "fix: This _is_ conventional, but it's rather long and will "
            "result in GitHub wrapping the message when it displays it\n\n"
            "And its body is also too long as it breaks our convention of "
            "each line being shorter than 80 characters.",
            1,
        ),
        (
            "This is very long _and_ it isn't conventional, so this is a "
            "double whammy of nope\n\n"
            "In fact its body is also too long so it's less double whammy, "
            "and more triple uh-oh",
            1,
        ),
    ],
)
def test_commit_msg(commit_message: str, exit_code: int) -> None:
    """Test that the commit-msg hook works as expected."""
    assert commit_msg.main(commit_message) == exit_code
