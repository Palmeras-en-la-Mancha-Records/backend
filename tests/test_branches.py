# Test Branch Operations
def test_create_branch_happy_path(client):
    """
    Happy Path Test:
    Verifies that providing valid branch information:
    1. Returns HTTP status code 201 (CREATED).
    2. Returns matching data along with the generated unique id.
    3. Persists the record accessible via GET /branches/{id}.
    4. Updates the branch with optional fields via PUT /branches/{id}.
    5. Cleans up the created record via DELETE /branches/{id}.
    """
    payload = {
        "name": "Palmeras Records - Centro",
        "address": "Calle Mayor 12, Ciudad Real",
        "phone": "+34 926 000 111"
    }

    # 1. Create branch (POST)
    response = client.post("/branches/", json=payload)
    assert response.status_code == 201, f"Failed to create branch: {response.text}"

    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["address"] == payload["address"]
    assert data["phone"] == payload["phone"]

    created_id = data["id"]

    # 2. Verify persistence (GET)
    get_res = client.get(f"/branches/{created_id}")
    assert get_res.status_code == 200, f"Failed to retrieve branch: {get_res.text}"
    assert get_res.json()["name"] == payload["name"]

    # 3. Partial update via PUT
    update_payload = {
        "name": "Palmeras Records - Central"
    }

    put_res = client.put(
        f"/branches/{created_id}",
        json=update_payload
    )

    assert put_res.status_code == 200, f"Failed to update branch: {put_res.text}"
    assert put_res.json()["name"] == "Palmeras Records - Central"
    assert put_res.json()["address"] == payload["address"]
    assert put_res.json()["phone"] == payload["phone"]

    # 4. Clean up created record (DELETE)
    del_res = client.delete(f"/branches/{created_id}")
    assert del_res.status_code == 200


def test_get_branches(client):
    
    
    response = client.get("/branches/")
    assert response.status_code == 200, f"Failed to retrieve branches: {response.text}"

    data = response.json()
    assert isinstance(data, list)


def test_get_branch_by_id(client):
    
    payload = {
        "name": "Test Branch",
        "address": "Test Address",
        "phone": "+34 900 000 000"
    }

    
    create_res = client.post("/branches/", json=payload)
    assert create_res.status_code == 201, f"Failed to create branch: {create_res.text}"

    created_id = create_res.json()["id"]

    
    response = client.get(f"/branches/{created_id}")
    assert response.status_code == 200, f"Failed to retrieve branch: {response.text}"
    assert response.json()["id"] == created_id
    assert response.json()["name"] == payload["name"]

    
    del_res = client.delete(f"/branches/{created_id}")
    assert del_res.status_code == 200


def test_update_branch(client):
   
    payload = {
        "name": "Original Branch",
        "address": "Original Address",
        "phone": "+34 900 111 222"
    }

    
    create_res = client.post("/branches/", json=payload)
    assert create_res.status_code == 201, f"Failed to create branch: {create_res.text}"

    created_id = create_res.json()["id"]

    update_payload = {
        "name": "Updated Branch",
        "address": "Updated Address",
        "phone": "+34 900 333 444"
    }

    
    response = client.put(
        f"/branches/{created_id}",
        json=update_payload
    )

    assert response.status_code == 200, f"Failed to update branch: {response.text}"

    data = response.json()
    assert data["name"] == update_payload["name"]
    assert data["address"] == update_payload["address"]
    assert data["phone"] == update_payload["phone"]

    
    del_res = client.delete(f"/branches/{created_id}")
    assert del_res.status_code == 200


def test_delete_branch(client):
    
    payload = {
        "name": "Branch To Delete",
        "address": "Delete Address",
        "phone": "+34 900 555 666"
    }

    
    create_res = client.post("/branches/", json=payload)
    assert create_res.status_code == 201, f"Failed to create branch: {create_res.text}"

    created_id = create_res.json()["id"]

    
    del_res = client.delete(f"/branches/{created_id}")
    assert del_res.status_code == 200, f"Failed to delete branch: {del_res.text}"
    assert del_res.json()["message"] == "Branch successfully deleted"

    
    get_res = client.get(f"/branches/{created_id}")
    assert get_res.status_code == 404


def test_get_nonexistent_branch(client):
    
    
    response = client.get("/branches/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"


def test_update_nonexistent_branch(client):
    
    payload = {
        "name": "Updated Branch"
    }

    
    response = client.put(
        "/branches/999999",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"


def test_delete_nonexistent_branch(client):
    
    
    response = client.delete("/branches/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Branch not found"


def test_trim_branch_data(client):
    
    payload = {
        "name": "   Trimmed Branch   ",
        "address": "   Trimmed Address   ",
        "phone": "   +34 900 777 888   "
    }

    
    response = client.post("/branches/", json=payload)
    assert response.status_code == 201, f"Failed to create branch: {response.text}"

    data = response.json()

    assert data["name"] == "Trimmed Branch"
    assert data["address"] == "Trimmed Address"
    assert data["phone"] == "+34 900 777 888"

    
    del_res = client.delete(f"/branches/{data['id']}")
    assert del_res.status_code == 200


def test_branch_name_only_spaces(client):
    
    payload = {
        "name": "   ",
        "address": "Test Address",
        "phone": "+34 900 000 000"
    }

   
    response = client.post("/branches/", json=payload)

    assert response.status_code == 422


def test_branch_address_only_spaces(client):
    
    payload = {
        "name": "Test Branch",
        "address": "   ",
        "phone": "+34 900 000 000"
    }

    
    response = client.post("/branches/", json=payload)

    assert response.status_code == 422


def test_branch_phone_only_spaces(client):
    
    payload = {
        "name": "Test Branch",
        "address": "Test Address",
        "phone": "   "
    }

    
    response = client.post("/branches/", json=payload)

    assert response.status_code == 422


def test_branch_name_too_long(client):
    
    payload = {
        "name": "A" * 101,
        "address": "Test Address",
        "phone": "+34 900 000 000"
    }

    
    response = client.post("/branches/", json=payload)

    assert response.status_code == 422


def test_branch_address_too_long(client):
    
    payload = {
        "name": "Test Branch",
        "address": "A" * 256,
        "phone": "+34 900 000 000"
    }

    
    response = client.post("/branches/", json=payload)

    assert response.status_code == 422


def test_branch_phone_too_long(client):
    
    payload = {
        "name": "Test Branch",
        "address": "Test Address",
        "phone": "1" * 31
    }

    
    response = client.post("/branches/", json=payload)

    assert response.status_code == 422