rd2weekly
=========

Scrapes the CBS fantasy baseball site to generate a weekly summary for
export to reddit

Requirements
------------

  - Python 3 installed and on your PATH. This project is written in
    Python.

      - `pip` installed for your version of python 3. This is
        installed by default in more recent versions but may not be for
        older versions of python. `pip` is a (crappy) package manager
        for python and is used to download all the dependencies you
        might need for the project.

  - Firefox. This scraper uses `selenium` to read CBS, and `geckodriver`
    to drive that functionality. The driver only works with Firefox.

  - `npm` installed. Usually one installs this when installing `node`.
    This is necessary to download a version of the `geckodriver`.

  - Not Windows. I don't know enough about Windows to make this work
    there. I feel bad about this but for the time being, please only use
    a UNIX-based operating system.

Installation
------------

All steps listed here only have to be run once. Skip this section if
you've already performed these steps.

The first thing you'll want to do is clone a copy of the repository.

.. code-block:: bash

    # with https
    $ git clone https://github.com/swanysimon/rd2weekly.git

    # with ssh
    $ git clone git@github.com:swanysimon/rd2weekly.git

Then enter the repository:

.. code-block:: bash

    $ cd rd2weekly/

You'll almost certainly want to use a python virtual environment.
Depending on your version of python this may look slightly different,
but a quick google will show you the way if this doesn't work. This
creates a special directory in the project called `env/`, but you can
name it whatever you want.

.. code-block:: bash

    $ python3 -m venv env

Now grab all the dependencies for the project.

.. code-block:: bash

    # activate the virtual environment: remember to deactivate before
    # moving to other projects
    $ source env/bin/activate

    # download the python dependencies
    $ pip install -r requirements.txt

    # download the web driver
    $ npm install

Remember to deactivate your virtualenv before proceeding with other
projects.

Running
-------

First, activate your virtual environment:

.. code-block:: bash

    $ source env/bin/activate

The run the scraper. It will launch an instance of Firefox and navigate
around various parts of CBS. Do not move your mouse over any part of the
browser while the scraper is running! Sometimes tooltips will pop up and
prevent the driver from clicking on elements.

Passing the `-c <cbs_username> <cbs_password>` flag is purely optional.
If you do not supply it as a command line argument, the program will
prompt you for that information. None of this information is written;
it is only used for the current run of the program.

.. code-block:: bash

    # generate a summary for period 3, providing a password
    $ ./summary/main.py -p 3 -c nomiswanson@gmail.com my_password

    # generate a summary for period 15, get prompted for a password
    $ ./summary/main.py -p 15

Interpreting the Output
-----------------------

This tool prints out a read-to-copy-paste summary of the given scoring
period, formatted in the RedditDynasty2 standard summary format.

An important note: the summary provided may include multiple all star
sections: deduplicating optimal lineups is very difficult to do
programmatically and so _all_ optimal lineups are printed out. Please
use your human brain to provide only a single lineup in the reddit
post.

