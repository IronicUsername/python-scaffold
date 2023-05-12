# python-scaffold

This template repository aims to document a full development, planning, reviewing and deployment cycle of a python service.

For more information read up on the [`docs`](./docs) section.

## development

In order to have the best development experience with this boilerplate project, its recommended to use [Visual Studio Code](https://code.visualstudio.com/) as your main text editor.
Of corse other editors and IDEs work as well, we just have pre-configured settings to make development as easy as possible with VSCode since its the most used text editor out there.

## tools

We use [`Docker`](https://www.docker.com/) for our deployment and local dev environment.
The benefit from this is, we can simulate locally while developing a real world case and are as close as possible to the production deployment.

To start the pre-requisites for local development and testing run

```
docker-compose -f docker-compose.dev.yml up --build --force-recreate
```

This starts a Postgres database together with the `python_scaffold` service running specifically for local test environment.
(It basically has more open logging, exposes the postgres port and tells python to run in dev-mode.)

To start the service in production mode one just has to run:

```
docker-compose -f docker-compose.yml up --build --force-recreate
```
