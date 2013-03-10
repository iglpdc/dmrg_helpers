Skeleton of a project in python
===============================

Use the structure in this directory to create a new project in python. 

Instructions to create a new project
------------------------------------

Follow these instructions to create a new project and put it in a Git repo:

- Choose a name for your project. This will be the name of the Git repo and
  also the name of the folder in your local machine. Assume the name is
`py_proj`.

        $ mkdir $WORK_DIR/src/codes/py_proj
        $ cd $WORK_DIR/src/codes/py_proj

- Copy the contents of this skeleton there:

        $ cp $WORK_DIR/src/codes/python_skel .

- Make the directories to hold the code itself:

        $ mkdir -p py_proj/core
        $ mkdir -p py_proj/utils

- Create empty `__init__.py`files in each of the code directories:

        $ touch __init__.py
        $ cp __init__.py py_proj/core
        $ cp __init__.py py_proj/utils

- Edit the file `setup.py` as described in the file.
- Edit the file `tests/__init__.py` as described in the file.
- Edit this file to describe the project.
- Call sphinx to create the docs:

        $ cd docs
        $ sphix-quickstart

- Make it a Git repo and commit:

        $ git init
        $ git commit -a "Initial commit"

Instructions to make a virtual env and start coding
-----------------------------------------------------

You should create a virtualenv to develop your new project and track properly
its dependencies. The name of the virtualenv is going to be the same as the
project name.

- Create the virtual env, and activate it

        $ mkvirtualenv NAME
        $ workon NAME

- You probably want to install some stuff now:

        $ pip install nose, pydoc, yolk

- You probably want to use some packages from your system that cannot be
  pip-installed (e.g. numpy, scipy, and matplotlib). For those you just create
softlinks. You need to do this when the virtualenv is _active_.

        $ ln -s /System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/ $VIRTUAL_ENV/lib/python*/site-packages

Things to do
------------

- I think you can clone an enviroment using `cpvirtualenv`. So envs that are
  really close to each other could use this trick.


