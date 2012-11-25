# Skeletor #

http://en.wikipedia.org/wiki/Skeletor

## What is it? ##

Lets say you work in a company that turns around many different projects within a year but you use the same basic template for each project. You might copy and paste this around, it might fall out of date, things may get changes and improved but lost.

Skeletor gives you the ability to create a standard template (or templates) for your projects so you can bootstrap in one single command.

Originally developed for [Django](https://www.djangoproject.com/) projects you can use Skeletor for any type of project.

## Status - Beta##

Skeletor is currently at Beta and should be considered as an unstable piece of software, please use at your own risk :)

**Version:** 1.0 Beta

### Build Status ###

Skeletor is on the excellent [Travis CI](https://travis-ci.org/krak3n/Skeletor) service.

[![Build Status](https://secure.travis-ci.org/krak3n/Skeletor.png?branch=master)](https://travis-ci.org/krak3n/Skeletor) - Master Branch (Most Stable Release)

[![Build Status](https://secure.travis-ci.org/krak3n/Skeletor.png?branch=develop)](https://travis-ci.org/krak3n/Skeletor) - Develop (Under Development)

## Stable Features ##

* Custom templates
* Git support for remote templates
* Multiple templates
* [Jinja2](http://jinja.pocoo.org/docs/) used for processing templates
* Python virtualenv creation
* Configurables using ~/.skeletor.cfg

## Experimental Features ##

* Python virtual environment creation
* Python package installing (``python setup.py develop``)

## Installation ##

For ``skeletor`` to be available system wide you must install as root:


* **Easy Install:**

```
$ sudo easy_install install skeletor
```

* **Pip:**

```
$ sudo pip install skeletor
```

* **Manual:**

```
$ git clone git@github.com:krak3n/Skeletor.git
$ cd Skeletor
$ sudo python setup.py install
```

## Basic Usage ##

Skeletor used via the command line, after installation you should have a Skeletor command available. Use help to see the options available.

    $ skeletor -h

To create a new project its simple, cd into the directory you want your new project to live, Skeletor will create the directory for you so you don't need to make it, for example:

    $ cd /home/me/projects
    $ skeletor -n hello_world

This will create a new hello_world directory at `/home/me/projects` and inside the default Skeletor template will have been created.

## Templates ##

### Default Template ###

The default template is a Django based template that [lives on GitHub here](https://github.com/krak3n/Skeletor-Default-Template). It is not recommended you use use this template in production. You should create your own template that best suites your needes for your project. This template is just for illustration uses to see how you could use Skeletor.

[Skeletor Default Template on Github](https://github.com/krak3n/Skeletor-Default-Template).

### Custom Templates ###

First create your own template somewhere on your file system. To use it just tell Skeletor about it by passing the ``-t`` or ``--template`` flag with the path to your template, for example:

```
$ skeletor -n hello_world -t /path/to/my/project/template
```

And if you want to use a git repository use pip style syntax:

```
$ skeletor -n hello_world -t git+git@github.com/path/to/repo.git
```

Of-course it doesn't have to be a Github repository, it can be any.

## Advanced Usage ##

Skeletor is flexible, and you can hopefully tailor it how you build out project skeletons.

### Command Line Options ###

**Stable**
 * ``-n / --name``: Your projects name.
 * ``-t / --template``: Path to a custom template, use `git+` to denote the path is to a git repository.
 * ``-c / --choose_template``: If you define multiple templates in the .skeletor.cfg use this flag to trigger a selection prompt instead of using the default template
 * ``-s / --template_settings_dir``: Custom settings directory name, see more info about this in the skeletor.cfg section.
 * ``--vars``: Custom variables for your templates, comma seperated var=value pairs, e.g: --vars var1=x,var2=y, would be accessed in teplates as {{ var1 }} and in dirs / file names as __var1__ / __var1__.ext (see section on this below)
 * ``-h / --help``: Show help

**Expermental**
 * ``-E / --venv_create``: Create a python virtual environment for this project.
 * ``-P / --venv_path``: Path to virtual environments home e.g `/home/me/.virtualenvs`.
 * ``-S / --venv_use_site_packages``: By default Skeletor creates the virtual environment with the `--no-site-packages` argument to make a clean virtual environment, but if you don't want it do that use this argument and it will be omitted.
 * ``-x / --venv_prefix``: If you want to prefix your virtual environments name with something then use this option, e.g `skeletor -n world -E -x hello-` will create a virtual environment called hello-world.

### Config File ###

Most things you can specify as command line options are also configurable in a `skeletor.cfg` file, this should live in your home directory and be prefixed with a `.`.

```
$ touch ~/.skeletor.cfg
```

#### Example Config ####

```
[template]
# The Default Template to user (can be a git repp, prefix with git+url_to_repo
default=/home/me/my_custom_template/
# Add other templates here, for example:
experimental_template: /my/new/template/
flask: git+git@github.com/my_flask_template.git

[misc]
install=0 # Experimental

# Experimental
[virutalenv]
venv_create=1
venv_path=/home/me/.virtualenvs/
```

Above is an example `.skeletor.cfg` file and contains a `[misc]`, `[virtualenv]`, and `[template]` sections. These sections and their allowed options allow you set defaults so when you run Skeletor form the command line you need to keep specifying things like template path and virtual environment creation.

#### Available Options ####

* ``[template]``
    * **default**: Path to your custom template, prefix with `git+` to define git repository path.
    * **other_template**: Path to other template
* ``[misc]``
    * **install**: 0 or 1 - Run ``setup.py`` to install project onto python path using `setup.py develop`
* ``[virtualenv]``
    * **venv_create**: 0 or 1 - Create python virtual environment
    * **venv_path**: Path to python virtual environments home, e.g `/home/me/.virtualenvs/

## Extra Variables ##

### In templates ###
Of course project name is not always enough and in these situations you can send extra variables to Skeletor to use in the template processing. For example:

```
$ skeletor -n hello_world --vars foo=bar
```

and in a template:

```
Hello World
foo={{ foo }}
```

As Jinja2 is used to render the templates, you can use conditons, and other Jinja2 functionality, for example:

```
{% if foo=='bar' %}
Foo is bar
{% else %}
Foo is not bar
{% endif %}
```

See the [Jinja2 Documentation](http://jinja.pocoo.org/docs/).

### Renaming Files / Directories ###
You can even rename a directory and/or file by using double underscores around the variable name, for example:

```
- /path/to/template/
  - __foo__/
    - another.txt
  - __foo__.txt
  - some_file.txt
  - some_other_file.tx
```

The resulting structure would be:

```
- /path/to/template/
  - bar/
    - another.txt
  - bar.txt
  - some_file.txt
  - some_other_file.tx
```

## To Do ##

Skeletor is still in early development and there is still a lot to do, this list is in order or priority:

 * Support for Mercurial and SVN repositories
 * Write more tests
 * Read the Docs Documentation
 
## License ##

See LICENSE file.

## Authors ##

See AUTHORS file.

## Special Thanks ##

To the Tech Team at [Poke London](http://www.pokelondon.com/) and the awesome [GitPython library](https://github.com/gitpython-developers/GitPython) and [Jinja2](http://jinja.pocoo.org/docs/) libraries.

## Contributing ##

Fancy helping out? Fork, commit, issue pull request :) Also please write some tests to prove your new bit of code works.

This project uses git flow, if you are not familiar please see [Git Flow](https://github.com/nvie/gitflow). Under Git Flow master is the most stable brach, develop is where active development occurs so please contribute using the develop branch.