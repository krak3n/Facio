# Skeletor #

Skeletor is a tool for building project skeleton templates. Primarily based on Django projects you could use Skeletor for other kinds of projects such as flat HTML templates or other frameworks.

## Status ##

Skeletor is currently at Alpha and should be considered as a stable piece of software, please use at your own risk :)

**Version:** 1.0 Alpha

## Features ##

* Custom templates
* Git support for remote templates 
* Template place holders
* Python virtualenv creation
* Automatic develop installation to python path
* Configurables using ~/.skeletor.cfg

## Installation ##

For `skeletor` to be available system wide you must install as root:

* **Pip:**

    ```
    $ sudo pip install -e git@github.com:krak3n/Skeletor.git#egg=skeletor
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

To create a new project it's simple, cd into the directory you want your new project to live, Skeletor will create the directory for you so you don't need to make it, for example:

    $ cd /home/me/projects
    $ skeletor -n hello_world

This will create a new hello_world directory at `/home/me/projects` and inside the default Skeletor template will have been created.

## Default Template ##

Skeletors default project template is a basic Django project skeleton we use quite often at [Poke London](http://www.pokelondon.com/) but if you don't like or want to use your own thats cool, just give Skeletor the git path or just a path to template on your local machine.

[Skeletor Default Template on Github](https://github.com/krak3n/Skeletor-Default-Template).

To use your own template:

    $ skeletor -n hello_world -t /path/to/my/project/template

And if you want to use a git repository use pip style syntax:

    $ skeletor -n hello_world -t git+git@github.com/path/to/repo.git

Of-course it doesn't have to be a Github repository, it can be any.

## Advanced Usage ##

Skeletor is flexible, and you can hopefully tailor it how you build out project skeletons.

### Command Line Options ###

 * **-n / --name**: Your projects name.
 * **-i / --install**: If the project template includes a setup.py file this command will attempt to run `python setup.py develop` to install your new project to the python path, if you are creating a virtual environment along with your project it will install it here instead of to the root.
 * **-t / --template**: Path to a custom template, use `git+` to denote the path is to a git repository.
 * **-s / --template_settings_dir**: Custom settings directory name, see more info about this in the skeletor.cfg section.
 * **-E / --venv_create**: Create a python virtual environment for this project.
 * **-P / --venv_path**: Path to virtual environments home e.g `/home/me/.virtualenvs`.
 * **-S / --venv_use_site_packages**: By default Skeletor creates the virtual environment with the `--no-site-packages` argument to make a clean virtual environment, but if you don't want it do that use this argument and it will be omitted.
 * **-x / --venv_prefix**: If you want to prefix your virtual environments name with something then use this option, e.g `skeletor -n world -E -x hello-` will create a virtual environment called hello-world.
 * **-h / --help**: Show help

 **NOTE:** There are also database options defined, however these are not currently used, but will be in the near future.

### Config File ###

Most things you can specify as command line options are also configurable in a `skeletor.cfg` file, this should live in your home directory and be prefixed with a `.`.

    $ touch ~/.skeletor.cfg

#### Example Config ####

    [misc]
    install=0

    [virutalenv]
    venv_create=1
    venv_path=/home/me/.virtualenvs/

    [template]
    template_path=/home/me/my_custom_template/

Above is an example `.skeletor.cfg` file and contains a `[misc]`, `[virtualenv]`, and `[template]` sections. These sections and their allowed options allow you set defaults so when you run Skeletor form the command line you need to keep specifying things like template path and virtual environment creation.

#### Available Options ####

* `[misc]`
    * **install**: 0 or 1 - Run setup.py to install project onto python path using `setup.py develop`
* `[virtualenv]`
    * **venv_create**: 0 or 1 - Create python virtual environment
    * **venv_path**: Path to python virtual environments home, e.g `/home/me/.virtualenvs/
* `[template]`
    * **template_path**: Path to your custom project template, prefix with `git+` to define git repository path.
    * **template_settings_dir**: This is oreintated around Django but if you have a settings directory for each environment the project runs on yor can set this to be your name or something more meaningfull, take a look at the default template. e.g `template_settings_dir=chris`.
* `[database]` **(coming soon)**
    * **db_create**: 0 or 1 - Auto create database
    * **db_root_user**: Your local dev database root user name
    * **db_root_pass**: Your local dev database root password

## To Do ##

Skeletor is still in early development and there is still a lot to do, this list is in order or priority:

 * Write Tests
 * Customisable Template Placeholders
 * Database Creation Support
 * Support for mercural and svn template repositories

## Contributing ##

Fancy helping out? Fork, commit, issue pull request :)
This project uses git flow, if you are not familiar please see [Git Flow](https://github.com/nvie/gitflow). Under Git Flow master is the most stable brach, develop is where active development occures so please contribute using the develop branch.

## Thanks To ##

The Tech Team at [Poke London](http://www.pokelondon.com/) and the awesome [GitPython library](https://github.com/gitpython-developers/GitPython).

## License ##

See LICENSE file in the repository.
