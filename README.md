# Tracking Plan Kit

A set of tools and packages to used for data governance at Buffer.

## Installation

Using [pipenv](https://github.com/pypa/pipenv) is recommended.

    pipenv install -e "git+https://github.com/bufferapp/tracking-plan-kit.git#egg=tracking-plan-kit"

## CLI

The `tracking-plan` command line is the main UI for working with this package.

To dump a Segment tracking plan into a yaml formatted project:

    tracking-plan dump <root-dir>

To update a tracking plan from the yaml formatted project:

    tracking-plan update <project-dir>

## Development

First you need to set up a development env.

    make init

### Running the tests

    make test