# settings for vscode

This section of the documentation lays out the settings for some extensions for a nicer workflow within VScode.

### index:

- [python docstrings templates with](#python-docstrings-templates-with-autodocstring)

## python docstrings templates with `autoDocstring`

For generating uniform python docstrings in VScode, one can make use of the `autoDocstring` extension.
In order to have a uniform codebase we provide a [`python-docstring-template.mustache`](./python-docstring-template.mustache) template file for python docstrings.

### manual setup

To incorporate this in your VSCode instance, you have to

- got to `Settings` -> `Extensions` -> `Python Docstring Generator configuration` -> `Auto Docstring: Custom Template Path`
- set the value there to: `../docs/settings/vscode/python-docstring-template.mustache`

> **Note**
>
> Make sure you are within the `Workspace` tab in the settings to not change your personal settings!

### quick-start

One also has the option to start the own VSCode instance with our reconfigured environment for it by just simply opening the `python-scaffold.code-workspace` file.

It comes with linting, auto formatting and test/debugging out of the box to make the development experience smoother.
