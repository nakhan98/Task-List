Task List App
-------------

A coding test I did a while back. Putting it up here and improving it.

Setup
=====
- Setup a python2 virtualenv and activate it (see http://docs.python-guide.org/en/latest/dev/virtualenvs/).
- Install required dependencies: ```pip install -r requirements.txt```.
- Run dev server: ```python manage.py runserver```.
- Browse to http://localhost:8000/task_list/ .
- To run tests: ```python manage.py test -v2```.

Docker
=====
- Run docker-compose as usual (TODO: modify to remove ssl stuff)

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
