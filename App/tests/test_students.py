def test_create_student(client, app):

    data = {"name": "Jane"}

    response = client.post('/newstudent', json=data)

    assert response.status_code in (200, 201), f"Expected 200 or 201, got {response.status_code}"

    json_data = response.get_json()
    assert json_data is not None, "Response should contain JSON data"
    assert "name" in json_data or "error" in json_data, "Expected 'name' or 'error' key in response"
