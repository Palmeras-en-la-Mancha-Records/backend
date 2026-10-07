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


def test_get_albums(client):
    
    
    response = client.get("/albums/")
    assert response.status_code == 200, f"Failed to retrieve albums: {response.text}"

    data = response.json()
    assert isinstance(data, list)


def test_get_album_by_id(client):
    
    payload = {
        "title": "Test Album",
        "artist": "Test Artist",
        "release_year": 2024,
        "genre": "Rock",
        "record_label": "Test Label",
        "price": 19.99,
        "stock": 10,
        "format_id": 1,
        "cover_image_url": "https://example.com/test-cover.jpg"
    }

    
    create_res = client.post("/albums/", json=payload)
    assert create_res.status_code == 201, f"Failed to create album: {create_res.text}"

    created_id = create_res.json()["id"]

    
    response = client.get(f"/albums/{created_id}")
    assert response.status_code == 200, f"Failed to retrieve album: {response.text}"
    assert response.json()["id"] == created_id

    
    del_res = client.delete(f"/albums/{created_id}")
    assert del_res.status_code == 200


def test_update_album(client):
    
    payload = {
        "title": "Test Album",
        "artist": "Test Artist",
        "release_year": 2024,
        "genre": "Rock",
        "record_label": "Test Label",
        "price": 19.99,
        "stock": 10,
        "format_id": 1,
        "cover_image_url": "https://example.com/test-cover.jpg"
    }

    
    create_res = client.post("/albums/", json=payload)
    assert create_res.status_code == 201, f"Failed to create album: {create_res.text}"

    created_id = create_res.json()["id"]

    update_payload = {
        "title": "Updated Album",
        "artist": "Updated Artist",
        "price": 29.99,
        "stock": 20
    }

    
    response = client.put(
        f"/albums/{created_id}",
        json=update_payload
    )
    assert response.status_code == 200, f"Failed to update album: {response.text}"

    data = response.json()
    assert data["title"] == update_payload["title"]
    assert data["artist"] == update_payload["artist"]
    assert data["price"] == update_payload["price"]
    assert data["stock"] == update_payload["stock"]

    
    del_res = client.delete(f"/albums/{created_id}")
    assert del_res.status_code == 200


def test_delete_album(client):
    
    payload = {
        "title": "Test Album",
        "artist": "Test Artist",
        "release_year": 2024,
        "genre": "Rock",
        "record_label": "Test Label",
        "price": 19.99,
        "stock": 10,
        "format_id": 1,
        "cover_image_url": "https://example.com/test-cover.jpg"
    }

    
    create_res = client.post("/albums/", json=payload)
    assert create_res.status_code == 201, f"Failed to create album: {create_res.text}"

    created_id = create_res.json()["id"]

    
    del_res = client.delete(f"/albums/{created_id}")
    assert del_res.status_code == 200, f"Failed to delete album: {del_res.text}"
    assert del_res.json()["message"] == "Album successfully deleted"

    
    get_res = client.get(f"/albums/{created_id}")
    assert get_res.status_code == 404


def test_get_nonexistent_album(client):
    
    
    response = client.get("/albums/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Album not found"


def test_update_nonexistent_album(client):
    
    payload = {
        "title": "Updated Album"
    }

    
    response = client.put(
        "/albums/999999",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Album not found"


def test_delete_nonexistent_album(client):
    
    
    response = client.delete("/albums/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Album not found"


def test_search_album_by_title(client):
    
    payload = {
        "title": "Unique Search Album",
        "artist": "Test Artist",
        "release_year": 2024,
        "genre": "Rock",
        "record_label": "Test Label",
        "price": 19.99,
        "stock": 10,
        "format_id": 1,
        "cover_image_url": None
    }

    
    create_res = client.post("/albums/", json=payload)
    assert create_res.status_code == 201, f"Failed to create album: {create_res.text}"

    created_id = create_res.json()["id"]

    
    response = client.get(
        "/albums/",
        params={"search": "Unique Search Album"}
    )

    assert response.status_code == 200
    assert any(album["id"] == created_id for album in response.json())

    
    del_res = client.delete(f"/albums/{created_id}")
    assert del_res.status_code == 200


def test_search_album_by_artist(client):
    
    payload = {
        "title": "Test Album",
        "artist": "Unique Search Artist",
        "release_year": 2024,
        "genre": "Rock",
        "record_label": "Test Label",
        "price": 19.99,
        "stock": 10,
        "format_id": 1,
        "cover_image_url": None
    }

    
    create_res = client.post("/albums/", json=payload)
    assert create_res.status_code == 201, f"Failed to create album: {create_res.text}"

    created_id = create_res.json()["id"]

    
    response = client.get(
        "/albums/",
        params={"search": "Unique Search Artist"}
    )

    assert response.status_code == 200
    assert any(album["id"] == created_id for album in response.json())

    
    del_res = client.delete(f"/albums/{created_id}")
    assert del_res.status_code == 200


def test_filter_album_by_genre(client):
    
    payload = {
        "title": "Genre Test Album",
        "artist": "Test Artist",
        "release_year": 2024,
        "genre": "Unique Rock Genre",
        "record_label": "Test Label",
        "price": 19.99,
        "stock": 10,
        "format_id": 1,
        "cover_image_url": None
    }

    
    create_res = client.post("/albums/", json=payload)
    assert create_res.status_code == 201, f"Failed to create album: {create_res.text}"

    created_id = create_res.json()["id"]

    
    response = client.get(
        "/albums/",
        params={"genre": "Unique Rock Genre"}
    )

    assert response.status_code == 200
    assert any(album["id"] == created_id for album in response.json())

    
    del_res = client.delete(f"/albums/{created_id}")
    assert del_res.status_code == 200


def test_trim_album_title_and_artist(client):
    
    payload = {
        "title": "   Trimmed Album   ",
        "artist": "   Trimmed Artist   "
    }

    
    response = client.post("/albums/", json=payload)
    assert response.status_code == 201, f"Failed to create album: {response.text}"

    data = response.json()
    assert data["title"] == "Trimmed Album"
    assert data["artist"] == "Trimmed Artist"

    
    del_res = client.delete(f"/albums/{data['id']}")
    assert del_res.status_code == 200


def test_album_title_only_spaces(client):
    
    payload = {
        "title": "   ",
        "artist": "Test Artist"
    }

    
    response = client.post("/albums/", json=payload)

    assert response.status_code == 422


def test_album_artist_only_spaces(client):
    
    payload = {
        "title": "Test Album",
        "artist": "   "
    }

    
    response = client.post("/albums/", json=payload)

    assert response.status_code == 422


def test_album_negative_price(client):
    
    payload = {
        "title": "Test Album",
        "artist": "Test Artist",
        "price": -10
    }

    
    response = client.post("/albums/", json=payload)

    assert response.status_code == 422


def test_album_negative_stock(client):
    
    payload = {
        "title": "Test Album",
        "artist": "Test Artist",
        "stock": -1
    }

    
    response = client.post("/albums/", json=payload)

    assert response.status_code == 422


def test_album_release_year_below_minimum(client):
    
    payload = {
        "title": "Test Album",
        "artist": "Test Artist",
        "release_year": 1899
    }

    
    response = client.post("/albums/", json=payload)

    assert response.status_code == 422


def test_album_release_year_above_maximum(client):
    
    payload = {
        "title": "Test Album",
        "artist": "Test Artist",
        "release_year": 2101
    }

    
    response = client.post("/albums/", json=payload)

    assert response.status_code == 422