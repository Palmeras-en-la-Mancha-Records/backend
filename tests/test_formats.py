def test_create_format_happy_path(client):
    
    payload = {
        "name": "Test Vinyl",
        "description": "Test vinyl format"
    }

    
    response = client.post("/formats/", json=payload)
    assert response.status_code == 201, f"Failed to create format: {response.text}"

    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

    created_id = data["id"]

    
    get_res = client.get(f"/formats/{created_id}")
    assert get_res.status_code == 200, f"Failed to retrieve format: {get_res.text}"
    assert get_res.json()["name"] == payload["name"]

    
    del_res = client.delete(f"/formats/{created_id}")
    assert del_res.status_code == 200


def test_get_formats(client):
    
    
    response = client.get("/formats/")
    assert response.status_code == 200, f"Failed to retrieve formats: {response.text}"

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_format_by_id(client):
    
    payload = {
        "name": "Test Format",
        "description": "Format created for testing"
    }

    
    create_res = client.post("/formats/", json=payload)
    assert create_res.status_code == 201, f"Failed to create format: {create_res.text}"

    created_id = create_res.json()["id"]

    
    response = client.get(f"/formats/{created_id}")
    assert response.status_code == 200, f"Failed to retrieve format: {response.text}"
    assert response.json()["id"] == created_id
    assert response.json()["name"] == payload["name"]

    
    del_res = client.delete(f"/formats/{created_id}")
    assert del_res.status_code == 200


def test_update_format(client):
    
    payload = {
        "name": "Original Format",
        "description": "Original description"
    }

    
    create_res = client.post("/formats/", json=payload)
    assert create_res.status_code == 201, f"Failed to create format: {create_res.text}"

    created_id = create_res.json()["id"]

    update_payload = {
        "name": "Updated Format",
        "description": "Updated description"
    }

    
    response = client.put(
        f"/formats/{created_id}",
        json=update_payload
    )
    assert response.status_code == 200, f"Failed to update format: {response.text}"

    data = response.json()
    assert data["name"] == update_payload["name"]
    assert data["description"] == update_payload["description"]

    
    del_res = client.delete(f"/formats/{created_id}")
    assert del_res.status_code == 200


def test_delete_format(client):
    
    payload = {
        "name": "Format To Delete",
        "description": "Format that will be deleted"
    }

    
    create_res = client.post("/formats/", json=payload)
    assert create_res.status_code == 201, f"Failed to create format: {create_res.text}"

    created_id = create_res.json()["id"]

    
    del_res = client.delete(f"/formats/{created_id}")
    assert del_res.status_code == 200, f"Failed to delete format: {del_res.text}"
    assert del_res.json()["message"] == "Format deleted successfully"

    
    get_res = client.get(f"/formats/{created_id}")
    assert get_res.status_code == 404


def test_get_nonexistent_format(client):
    
    
    response = client.get("/formats/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Format not found"


def test_update_nonexistent_format(client):
    
    payload = {
        "name": "Updated Format"
    }

    
    response = client.put(
        "/formats/999999",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Format not found"


def test_delete_nonexistent_format(client):
    
    
    response = client.delete("/formats/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Format not found"


def test_create_duplicate_format(client):
    
    payload = {
        "name": "Vinilo LP",
        "description": "Duplicate format test"
    }

    
    response = client.post("/formats/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "A format with this name already exists"


def test_update_format_with_duplicate_name(client):
    
    first_payload = {
        "name": "First Test Format",
        "description": "First format"
    }

    second_payload = {
        "name": "Second Test Format",
        "description": "Second format"
    }

    
    first_res = client.post("/formats/", json=first_payload)
    assert first_res.status_code == 201, f"Failed to create first format: {first_res.text}"

    first_id = first_res.json()["id"]

    
    second_res = client.post("/formats/", json=second_payload)
    assert second_res.status_code == 201, f"Failed to create second format: {second_res.text}"

    second_id = second_res.json()["id"]

    
    response = client.put(
        f"/formats/{second_id}",
        json={"name": first_payload["name"]}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "A format with this name already exists"

    
    del_first = client.delete(f"/formats/{first_id}")
    assert del_first.status_code == 200

    del_second = client.delete(f"/formats/{second_id}")
    assert del_second.status_code == 200


def test_trim_format_name(client):
    
    payload = {
        "name": "   Test Trim Format   ",
        "description": "Test description"
    }

    
    response = client.post("/formats/", json=payload)
    assert response.status_code == 201, f"Failed to create format: {response.text}"

    data = response.json()
    assert data["name"] == "Test Trim Format"

    
    del_res = client.delete(f"/formats/{data['id']}")
    assert del_res.status_code == 200


def test_format_name_only_spaces(client):
    
    payload = {
        "name": "   "
    }

    
    response = client.post("/formats/", json=payload)

    assert response.status_code == 422


def test_format_name_too_short(client):
    
    payload = {
        "name": "A"
    }

    
    response = client.post("/formats/", json=payload)

    assert response.status_code == 422


def test_format_name_too_long(client):
    
    payload = {
        "name": "A" * 101
    }

    
    response = client.post("/formats/", json=payload)

    assert response.status_code == 422


def test_format_description_too_long(client):
    
    payload = {
        "name": "Test Format",
        "description": "A" * 256
    }

    
    response = client.post("/formats/", json=payload)

    assert response.status_code == 422