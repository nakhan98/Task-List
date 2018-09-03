Task List App
-------------

A coding test I did a while back. Puting it her for posterity.

General info
============
- Developed on Debian Jessie with Python 2.7.9 and Django (1.7.11).
- Bootstrap and jQuery used for front end.

Setup
=====
- Setup a python2 virtualenv and activate it (see http://docs.python-guide.org/en/latest/dev/virtualenvs/).
- Install required dependencies: ```pip install -r requirements.txt```.
- Run dev server: ```python manage.py runserver```.
- Browse to http://localhost:8000/task_list/ .
- To run tests: ```python manage.py test -v2```.

Docker
=====
- Alternatively, run `start.sh` which dockerifies everything.
    - By default, app will listen on port 48080.


Instructions
============
- Create an account by clicking on 'Register' in the top menu.
- Login using credentials.
- To add a task click on "Add Task" and fill in both Title and Description
  fields and submit.
- To close a task click on the "Not Done" badge on the right hand sight of task
  in the table.
- To find out who closed a particular task, hover over the "Done" badge of a
  finished task (tooltip should provide username).
- To edit a task click on the pencil glyph.
- To delete a task click on the cross glyph.
