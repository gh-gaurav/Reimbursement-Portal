# import json

# def test_create_department(test_client):
#     # Define the data to be sent in the POST request
#     data = {'departmentName': 'HR'}

#     # Send POST request to create a new department
#     response = test_client.post('/department/create', data=json.dumps(data), content_type='application/json')

#     # Assert that the response status code is 201 (Created)
#     assert response.status_code == 201

#     # Assert that the response message is 'Department created successfully'
#     assert response.get_json() == {'message': 'Department created successfully'}

# def test_create_department_without_name(test_client):
#     # Define the data without department name
#     data = {}

#     # Send POST request to create a new department without name
#     response = test_client.post('/department/create', data=json.dumps(data), content_type='application/json')

#     # Assert that the response status code is 400 (Bad Request)
#     assert response.status_code == 400

#     # Assert that the response message is 'Department name is required'
#     assert response.get_json() == {'message': 'Department name is required'}

# def test_get_departments(test_client):
#     # Send GET request to retrieve all departments
#     response = test_client.get('/department/')

#     # Assert that the response status code is 200 (OK)
#     assert response.status_code == 200

#     # Assert that the response contains the created department
#     data = response.get_json()
#     assert len(data) == 1
#     assert data[0]['name'] == 'HR'

# def test_delete_department(test_client):
#     # Send DELETE request to remove the department
#     response = test_client.delete('/department/1')

#     # Assert that the response status code is 200 (OK)
#     assert response.status_code == 200

#     # Assert that the response message is 'Department deleted successfully'
#     assert response.get_json() == {'message': 'Department deleted successfully'}

# def test_delete_nonexistent_department(test_client):
#     # Send DELETE request to remove a non-existent department
#     response = test_client.delete('/department/2')

#     # Assert that the response status code is 404 (Not Found)
#     assert response.status_code == 404

#     # Assert that the response message is 'Department not found'
#     assert response.get_json() == {'message': 'Department not found'}
