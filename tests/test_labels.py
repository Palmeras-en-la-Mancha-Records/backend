# Test Label Operations
def test_create_label_happy_path(client):
    """
    Happy Path Test:
    Verifies that providing valid label information:
    1. Returns HTTP status code 201 (CREATED).
    2. Returns matching data along with the generated unique id.
    3. Persists the record accessible via GET /labels/{id}.
    4. Updates the record via PUT /labels/{id}.
    5. Cleans up the created record via DELETE /labels/{id}.
    """
    payload = {
        "name": "Discos Palmeras",
        "country": "Espana",
        "website": "https://palmeras.example.com"
    }

    # 1. Create label (POST)
    response = client.post("/labels/", json=payload)
    assert response.status_code == 201, f"Failed to create label: {response.text}"

    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["country"] == payload["country"]
    assert data["website"] == payload["website"]

    created_id = data["id"]

    # 2. Verify persistence (GET)
    get_res = client.get(f"/labels/{created_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == payload["name"]

    # 3. Update via PUT
    update_payload = {"name": "Discos Palmeras Ediciones"}
    put_res = client.put(f"/labels/{created_id}", json=update_payload)
    assert put_res.status_code == 200
    assert put_res.json()["name"] == "Discos Palmeras Ediciones"
    assert put_res.json()["country"] == payload["country"]

    # 4. Clean up created record (DELETE)
    del_res = client.delete(f"/labels/{created_id}")
    assert del_res.status_code == 200


def test_create_label_duplicate_name_rejected(client):
    """
    Validation Test:
    Verifies that creating two labels with the same name:
    1. Returns HTTP status code 201 for the first one.
    2. Returns HTTP status code 400 for the duplicate.
    3. Returns 404 when fetching a label that does not exist.
    """
    payload = {"name": "Label Duplicada"}

    first = client.post("/labels/", json=payload)
    assert first.status_code == 201, f"Failed to create label: {first.text}"

    duplicate = client.post("/labels/", json=payload)
    assert duplicate.status_code == 400
    assert "already exists" in duplicate.json()["detail"]

    missing = client.get("/labels/999999")
    assert missing.status_code == 404

    client.delete(f"/labels/{first.json()['id']}")
