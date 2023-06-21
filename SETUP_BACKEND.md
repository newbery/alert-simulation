
# Backend for Alert Simulation App

This is an app built upon the FastAPI server, Celery, and Redis.

The intent is to provide multiple backend implementations to try out a few different
variations and to demonstrate some design patterns.


## Prerequisites

This is a Python application with several third-party library requirements.
As is usual in such cases, it's strongly recommended to install the requirements
in a Python virtualenv (or a Docker image). There are several ways to do this
but I'll just describe my preferred mechanism using Poetry (https://python-poetry.org/)

First, make sure you have Python 3.11 available on your system. You might be
able to get away with another version but I've only tested this on Python 3.11.
At the very least, I suggest Python 3.8+

If you need to install multiple versions of Python for any reason,
I suggest using pyenv (https://github.com/pyenv/pyenv)

Poetry also needs to be available. I suggest installing via pipx (https://pypa.github.io/pipx/)
which is a handy way to install multiple python command line scripts with dependencies
that might conflict with each other.

`pipx install poetry`


## Services

This application requires Redis. It might also require other services depending
on which implementation is enabled.

See README.md for instructions on how to install these services.


## Quickstart

Install requirements into a poetry-managed virtualenv:

`poetry install`

Activate the virtualenv:

`poetry shell`

Launch the app:

`uvicorn backend.main:app`

Visit the app in a web browser at http://localhost:8000/

