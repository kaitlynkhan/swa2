def test_student_hours_flow(client, app):
    
    create_response = client.post('/newstudent', json={"name": "John"})
    assert create_response.status_code in (200, 201), f"Expected 200/201 for student creation, got {create_response.status_code}"

    hours_response = client.post('/1/reqHours', json={"staffID": 1, "hours": 5})
    assert hours_response.status_code in (200, 201), f"Expected 200/201 for hours request, got {hours_response.status_code}"

    json_data = hours_response.get_json()
    assert json_data is not None, "Response should contain JSON data"
