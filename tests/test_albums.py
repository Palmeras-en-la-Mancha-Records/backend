# Test Album Operations
def test_create_album_happy_path(client):
    """
    Happy Path Test:
    Verifies that providing valid album information:
    1. Returns HTTP status code 201 (CREATED).
    2. Returns matching data along with the generated unique id.
    3. Persists the record accessible via GET /albums/{id}.
    4. Cleans up the created record via DELETE /albums/{id}.
    """
    payload = {
        "title": "El Madrileño",
        "artist": "C. Tangana",
        "release_year": 2021,
        "genre": "Pop / Fusión",
        "record_label": "Sony Music Spain",
        "price": 24.99,
        "stock": 10,
        "format_id": 1,
        "cover_image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500"
    }

    # 1. Create album (POST)
    response = client.post("/albums/", json=payload)
    assert response.status_code == 201, f"Failed to create album: {response.text}"

    data = response.json()
    assert "id" in data
    assert data["title"] == payload["title"]
    assert data["artist"] == payload["artist"]
    assert data["release_year"] == payload["release_year"]
    assert data["genre"] == payload["genre"]
    assert data["record_label"] == payload["record_label"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]
    assert data["format_id"] == payload["format_id"]
    assert data["cover_image_url"] == payload["cover_image_url"]

    created_id = data["id"]

    # 2. Verify persistence (GET)
    get_res = client.get(f"/albums/{created_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == payload["title"]

    # 3. Clean up created record (DELETE)
    del_res = client.delete(f"/albums/{created_id}")
    assert del_res.status_code == 200
