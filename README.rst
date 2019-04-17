rd2weekly
=========

Scrapes the CBS fantasy baseball site to generate a weekly summary for export to reddit

Installation
============

You'll probably want to use a python ``virtualenv``.

.. code-block:: bash

    $ venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ npm install

Remember to deactivate your virtualenv before proceeding with other projects.

Running
=======

The executable lives at ``<project_home>/summary/main.py``. In theory the help information
that comes with the CLI is enough to decipher the options you should use.

Output is printed to the terminal for consumption. Something fancier may be on the way,
but for now get ready to copy-paste.

*NOTE*: The All Star summary will print out all unique optimal lineups. Human intervention
may be necessary to create a final lineup for the summary, but all the information you
need will be provided in the CLI output

