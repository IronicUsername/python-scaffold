# about

This project aims to solve 2 problems:

- 3rd party dependence
- quick project start

## the basis

The `python-scaffold` resembles 1 contained microservice that is able to:

- connect to a database
- connect to an api
- connect to an SSH/SFTP server

If one checks within the `python-scaffold/src/python_scaffold` application one sees different directories.
The directories resemble 1 logically separated functionality within the microservice.
As of now the functionality included by default are:

- `api`: Utilizes `fast-api` to serve a API
- `database`: Makes use of `SqlAlchemy` and gives us a connection and database models for a database we want to connect to
- `sftp`: a `paramiko` SSH/SFTP client to connect to given SSFTP servers.

For more detailed information on the default implemented functions, head to the [`cook-book`](./cook-book/) section of this documentation.

## uninstall default functions

If a service is not needed, it can optimally be uninstalled by removing:

- the service in `python-scaffolds/src/python_scaffold/<FUNCTIONALITY_THAT_SHOULD_BE_DELETED>`
- the corresponding tests in `python-scaffold/tests/test_python_scaffold/<FUNCTIONALITY_THAT_SHOULD_BE_DELETED>`
- and other possible occurrences of the functionality.

## etc

For further reading we have:

- a [`cook-book`](./cook-book/) section that shows how to have certain features in a step-to-step manner
- [`guides-and-tips.md`](./guides-and-tips/) which is a collection of best practices to work efficiently within a multi-authored software project
- [`settings.md`](./settings/) to document a few settings for specific tools within this project
