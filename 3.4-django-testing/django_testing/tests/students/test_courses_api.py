# def test_example():
#     assert False, "Just test example"

import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course

API_PATH = '/api/v1/courses/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory()

    response = client.get(API_PATH)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert course.name == data[0]['name']


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(API_PATH)

    assert response.status_code == 200
    data = response.json()
    assert len(courses) == len(data)


@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(f'{API_PATH}?id={courses[0].id}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert courses[0].name == data[0]['name']


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(f'{API_PATH}?name={courses[0].name}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert courses[0].id == data[0]['id']


@pytest.mark.django_db
def test_create_course(client):
    data = {'name': 'course1'}

    response = client.post(API_PATH, data)

    assert response.status_code == 201
    assert response.json()['name'] == data['name']


@pytest.mark.django_db
def test_update_course(client,course_factory):
    course = course_factory()
    data = {'name': 'course1'}

    response = client.patch(f'{API_PATH}{course.id}/', data)

    assert response.status_code == 200
    assert response.json()['name'] == data['name']


@pytest.mark.django_db
def test_delete_course(client,course_factory):
    course = course_factory()

    response = client.delete(f'{API_PATH}{course.id}/')

    assert response.status_code == 204
