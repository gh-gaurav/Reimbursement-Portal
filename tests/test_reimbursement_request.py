# tests/test_reimbursement_request.py

import pytest

@pytest.fixture
def client(test_client):
    return test_client

# def test_create_reimbursement_request(client):
#     response = client.post('/rr/', data={
#         'amount': '100.0',
#         'date': '2024-05-31',
#         'description': 'Test reimbursement request',
#         'category': 'Travelling',
#         'employee_id': '1'
#     }, content_type='multipart/form-data')
    
#     assert response.status_code == 201
#     assert response.json['success'] == True

# def test_get_reimbursement_requests(client):
#     response = client.get('/rr/get_reimbursement_requests')
    
#     assert response.status_code == 200
#     assert isinstance(response.json, list)



# def test_get_reimbursement_requests_manager(client):
#     response = client.get('/rr/get_reimbursement_requests_manager?manager_id=7')
#     assert response.status_code == 200
#     assert isinstance(response.json, list)


