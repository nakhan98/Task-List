from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        # Create a client
        self.client = Client()

        # Create test users
        self.user_1 = User.objects.create_user(username="test_user_1",
                                               password="abc")
        self.user_2 = User.objects.create_user(username="test_user_2",
                                               password="abc")

        # Create test tasks
        self.task_1 = Task.objects.create(user=self.user_1, title="Task 1",
                                          description="Description 1")
        self.task_2 = Task.objects.create(user=self.user_2, title="Task 2",
                                          description="Description 2")

    def test_about_page(self):
        """Test about page"""
        response = self.client.post("/task_list/about/")
        self.assertEquals(response.status_code, 200, "Unexpected status code")

    def test_login_get(self):
        """Test login page render"""
        response = self.client.get("/task_list/login/")
        self.assertEquals(response.status_code, 200, "Unexpected status code")

    def test_login_fail(self):
        """Test login functionality (failure)"""
        response = self.client.post("/task_list/login/",
                                    {"username": "abc", "password": "xyz"})
        self.assertEquals(response.status_code, 401, "Unexpected status code")
        self.assertEquals(response.content, "Login failed!",
                          "Unexpected content")

    def test_login_ok(self):
        """Test login functionality (success)"""
        response = self.client.post("/task_list/login/",
                                    {"username": "test_user_1",
                                     "password": "abc"})
        self.assertEquals(response.status_code, 302, "Unexpected status code")

    def test_register_get(self):
        """Test registration page render"""
        response = self.client.get("/task_list/register/")
        self.assertEquals(response.status_code, 200, "Unexpected status code")

    def test_register_ok(self):
        """Test registration functionality (success)"""
        response = self.client.post("/task_list/register/",
                                    {"username": "xxx", "email": "xxx@yyy.com",
                                     "password": "abc"})
        self.assertEquals(response.status_code, 200, "Unexpected status code")
        self.assertTrue(response.context["registered"],
                        "Unexpected value for 'registered' attribute")
        self.assertIsNone(response.context["form_errors"], "Unexpected form errors")

    def test_register_fail(self):
        """Test registration functionality (email validation failure)"""
        response = self.client.post("/task_list/register/",
                                    {"username": "xxx", "email": "xxx",
                                     "password": "123"})
        self.assertFalse(response.context["registered"],
                         "Unexpected value for 'registered' attribute")
        self.assertIn("Enter a valid email address.",
                      response.context["form_errors"],
                      "Unexpected form error")

    def test_task_list_render(self):
        """Test task list render (no filtering)"""
        self.client.login(username="test_user_1",
                          password="abc")
        response = self.client.get("/task_list/")

        # check http status code
        self.assertEquals(response.status_code, 200, "Unexpected status code")

        # Check user
        self.assertEquals(response.context["user_tasks"][0]["user"],
                          self.user_1, "Unexpected user")

        # Check task
        self.assertEquals(list(response.context["user_tasks"][0]["tasks"]),
                          [self.task_1], "Unexpected tasks")

    def test_task_list_filter(self):
        """Test task list render (with filtering)"""
        self.client.login(username="test_user_1",
                          password="abc")
        self.task_1.is_done = True
        self.task_1.save()
        response = self.client.get("/task_list/?hide_completed=1")

        # check http status code
        self.assertEquals(response.status_code, 200, "Unexpected status code")

        # user_1's task should be filtered out
        self.assertEquals(response.context["user_tasks"][0]["user"],
                          self.user_1, "Unexpected user")
        self.assertEquals(list(response.context["user_tasks"][0]["tasks"]),
                          [], "Unexpected tasks")

        # user_2's task should not be filtered out
        self.assertEquals(response.context["user_tasks"][1]["user"],
                          self.user_2, "Unexpected user")
        self.assertEquals(list(response.context["user_tasks"][1]["tasks"]),
                          [self.task_2], "Unexpected tasks")

    def test_add_task_ok(self):
        """Test adding a task (success)"""
        self.client.login(username="test_user_1",
                          password="abc")
        response = self.client.post("/task_list/add_task/",
                                    {"title": "new test task",
                                     "description": "new description"})
        # check http status code
        self.assertEquals(response.status_code, 200, "Unexpected status code")

        new_task = Task.objects.get(id=3)
        self.assertEqual(new_task.title, "new test task",
                         "Unexpected task title")
        self.assertEqual(new_task.description, "new description",
                         "Unexpected task description")

    def test_add_task_fail(self):
        """Test add task failure (due to not including title field)"""
        self.client.login(username="test_user_1",
                          password="abc")
        response = self.client.post("/task_list/add_task/",
                                    {"title": "",
                                     "description": "new description"})

        # Check no new task has been created
        self.assertFalse(Task.objects.filter(id=3), "Unexpected tasks")

        # Check form errors
        self.assertIn('title<ul class="errorlist"><li>This field is required',
                      response.context["form_errors"],
                      "Unexpected form errors")

    def test_delete_task_ok(self):
        """Test deleting a task (success)"""
        self.client.login(username="test_user_1",
                          password="abc")
        self.client.get("/task_list/delete_task/1")

        # user_1's task should be deleted
        self.assertFalse(Task.objects.filter(user=self.user_1),
                         "Unexpected tasks")

    def test_delete_task_fail(self):
        """Test deleting another user's task (should raise 403 error)"""
        self.client.login(username="test_user_1",
                          password="abc")
        response = self.client.get("/task_list/delete_task/2")

        # check http status code
        self.assertEquals(response.status_code, 403, "Unexpected status code")

        # user_1's task should not be deleted
        self.assertTrue(Task.objects.filter(user=self.user_1),
                        "Unexpected tasks")

    def test_edit_task_ok(self):
        """Test editing a task (success)"""
        self.client.login(username="test_user_1",
                          password="abc")
        response = self.client.post("/task_list/edit_task/1",
                                    {"title": "new title",
                                     "description": "new description",
                                     "task_status": 1})

        # check http status code
        self.assertEquals(response.status_code, 200, "Unexpected status code")

        # This is needed as refresh_from_db not implemented yet in django 1.7
        self.task_1 = Task.objects.get(id=1)

        # Check that title, description and status was changed
        self.assertEquals(self.task_1.title, "new title", "Unexpected title")
        self.assertEquals(self.task_1.description, "new description",
                          "Unexpected title")
        self.assertEquals(self.task_1.is_done, True,
                          "Unexpected task status")

    def test_edit_task_fail(self):
        """Test editing a task failure (missing title field)"""
        self.client.login(username="test_user_1",
                          password="abc")
        response = self.client.post("/task_list/edit_task/1",
                                    {"title": "",
                                     "description": "new description",
                                     "task_status": 1})

        # This is needed as refresh_from_db not implemented yet in django 1.7
        self.task_1 = Task.objects.get(id=1)

        # Check that title, description and status was not changed
        self.assertEquals(self.task_1.title, "Task 1", "Unexpected title")
        self.assertEquals(self.task_1.description, "Description 1",
                          "Unexpected description")
        self.assertEquals(self.task_1.is_done, False,
                          "Unexpected task status")

        # Check form_errors
        self.assertIn('title<ul class="errorlist"><li>This field is required',
                      response.context["form_errors"],
                      "Unexpected form errors"
                      )

    def test_close_task(self):
        """Test closing task (as different user to creator of task)"""
        self.client.login(username="test_user_1",
                          password="abc")
        response = self.client.get("/task_list/close_task/2")

        # check http status code
        self.assertEquals(response.status_code, 302, "Unexpected status code")

        # This is needed as refresh_from_db not implemented yet in django 1.7
        self.task_2 = Task.objects.get(id=2)

        # Check that task was closed
        self.assertEquals(self.task_2.is_done, True, "Unexpected status")
        self.assertEquals(self.task_2.status_changed_by, self.user_1,
                          "Unexpected user")
