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
    assert get_res.status_code == 200
    assert get_res.json()["name"] == payload["name"]

    # 3. Partial update via PUT
    update_payload = {"name": "Palmeras Records - Central"}
    put_res = client.put(f"/branches/{created_id}", json=update_payload)
    assert put_res.status_code == 200
    assert put_res.json()["name"] == "Palmeras Records - Central"
    assert put_res.json()["address"] == payload["address"]

    # 4. Clean up created record (DELETE)
    del_res = client.delete(f"/branches/{created_id}")
    assert del_res.status_code == 200
