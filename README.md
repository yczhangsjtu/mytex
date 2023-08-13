# The mytex Tool
LaTeX project management tool. Provides functionalities including:

- Automatically create new LaTeX projects using given templates. This tool already includes some templates such as Beamer, LNCS, ACM.
- Switch a project to a different template.
- Manage the self-defined latex commands.
- Define custom grammar and replace automatically.
- Detect citations in tex files and manage the bib file, select which fields to include in the bib items.

All the configuration files will be stored in a `.mytex` folder inside the project directory. The configuration files are in yaml format.

## Initialize the tool

If `mytex` has never been executed before, executing it the first time will create a `mytex` directory in the `$HOME/.config` folder. The folder structure will be as follows, where the contents of the templates are omitted for clarity.

```
$HOME/.config/mytex
- config.yaml
- templates/
  - article/
  - acm/
  - beamer/
  - lncs/
```

## Create a new project

Execute the following command where you want to place the project.

```bash
mytex create
```

The program will ask a few questions.

```
Project name: Hello
Select template:
(1) Empty article
(2) LNCS
(3) ACM
(4) Beamer
Your choice: 1
Title: Hello World
```

Then create a directory with a `.mytex` folder in it, and the template is already applied. The new project will have the following structure.

```
Hello
- .mytex/
	- config.yaml
- main.tex
- packages.tex
- definitions.tex
- body.tex
```

## Configuration file

The default configuration file will look as follows.

```yaml
- name: Hello
- template: article
- title: Hello World
- subtitle: None
- date: May 1, 2023
- authors: None
- keywords: None
```

## Switch template

Execute the following command inside the project.

```
mytex template
```

The program will try to find a `.mytex` folder in the current directory, or ancestor directories. If succeeds, it asks the user to choose a template, then replaces all the template files with those in the selected template.
