import nox

PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]

nox.options.reuse_existing_virtualenvs = True

nox.options.sessions = [
    "lint",
    "pytest",
]


@nox.session(python=PYTHON_VERSIONS)
def lint(session: nox.Session):
    session.install("-e", ".")
    session.run("make", "lint", external=True)


@nox.session(python=PYTHON_VERSIONS)
def pytest(session: nox.Session):
    session.install("-e", ".")
    session.install("pytest")
    session.run("pip", "check")

    session.run("pytest", "tests", "src")
