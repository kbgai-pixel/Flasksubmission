from main import app


def test_home_page():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200


def test_contact_page():
    client = app.test_client()
    res = client.get('/contact')
    assert res.status_code == 200


def test_user_submission_flow():
    client = app.test_client()
    res = client.post(
        '/submit-form',
        data={
            'full_name': 'Alice Example',
            'email': 'alice@example.com',
            'age': '28',
            'city': 'Cairo',
            'country': 'Egypt',
            'occupation': 'Developer',
            'hobby': 'Reading',
            'programming_language': 'Python',
            'online_hours': '5',
            'entertainment': 'Movies',
        },
    )
    assert res.status_code == 200
    assert 'Submission successful' in res.get_data(as_text=True)

    users_page = client.get('/users')
    assert users_page.status_code == 200
    assert 'Alice Example' in users_page.get_data(as_text=True)
