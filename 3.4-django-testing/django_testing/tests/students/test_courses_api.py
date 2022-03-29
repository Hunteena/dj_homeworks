import random
import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student

API_PATH = '/api/v1/courses/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory(student_factory):
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory, student_factory):
    students_set = student_factory(_quantity=10)
    course = course_factory(students=students_set)

    response = client.get(f'{API_PATH}{course.id}/')

    assert response.status_code == 200
    data = response.json()
    assert course.name == data['name']
    assert len(data['students']) == len(students_set)
    assert set(data['students']) == set([student.pk for student in students_set])


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(API_PATH)

    assert response.status_code == 200
    data = response.json()
    assert len(courses) == len(data)
    for i, c in enumerate(data):
        assert courses[i].name == c['name']


@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    courses = course_factory(_quantity=5)
    random_course = random.choice(courses)

    response = client.get(f'{API_PATH}?id={random_course.id}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert random_course.name == data[0]['name']


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    courses = course_factory(_quantity=5)
    random_course = random.choice(courses)

    response = client.get(f'{API_PATH}?name={random_course.name}')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert random_course.id == data[0]['id']


@pytest.mark.django_db
def test_create_course(client):
    data = {'name': 'course1'}

    response = client.post(API_PATH, data)

    assert response.status_code == 201
    assert response.json()['name'] == data['name']


@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    course = course_factory()
    students = student_factory(_quantity=10)
    student_ids = [student.id for student in students]
    data = {'name': 'course1', 'students': student_ids}

    response = client.patch(f'{API_PATH}{course.id}/', data)

    response_data = response.json()
    assert response.status_code == 200
    assert response_data['name'] == data['name']
    assert len(response_data['students']) == len(students)


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()

    response = client.delete(f'{API_PATH}{course.id}/')

    assert response.status_code == 204


@pytest.mark.parametrize(
    'max_count, students_count, response_status',
    [(2, 4, 400), (2, 1, 200)]
)
@pytest.mark.django_db
def test_max_students(settings, client,
                      course_factory, student_factory,
                      max_count, students_count, response_status):
    settings.MAX_STUDENTS_PER_COURSE = max_count
    course = course_factory()
    students = student_factory(_quantity=students_count)
    student_ids = [student.id for student in students]

    data = {'students': student_ids}

    response = client.patch(f'{API_PATH}{course.id}/', data)

    assert response.status_code == response_status
