def test_healthz(client):
    assert client.get("/healthz").json() == {"status": "ok"}


def test_config_exposes_branding(client):
    data = client.get("/api/config").json()
    assert set(data) == {"name", "description", "disclaimer"}


def test_create_group_requires_auth(client):
    assert client.post("/api/groups", json={"name": "No Auth"}).status_code == 401


def test_group_crud(client, auth):
    created = client.post(
        "/api/groups",
        json={"name": "Web Devs", "description": "grupo", "url": "https://example.com"},
        headers=auth,
    )
    assert created.status_code == 200
    group = created.json()
    assert group["tags"] == []
    assert any(g["id"] == group["id"] for g in client.get("/api/groups").json())

    updated = client.put(
        "/api/groups",
        json={"id": group["id"], "name": "Web Developers", "description": "", "url": ""},
        headers=auth,
    )
    assert updated.json()["group"]["name"] == "Web Developers"

    assert client.delete(f"/api/groups/{group['id']}", headers=auth).json()["success"] is True
    assert client.get(f"/api/groups/{group['id']}").status_code == 404


def test_group_url_must_be_http(client, auth):
    response = client.post(
        "/api/groups", json={"name": "Evil", "url": "javascript:alert(1)"}, headers=auth
    )
    assert response.status_code == 422


def test_fuzzy_search_tolerates_typos(client, auth):
    client.post("/api/groups", json={"name": "Programacion"}, headers=auth)
    client.post("/api/groups", json={"name": "Matematica"}, headers=auth)

    results = client.get("/api/groups", params={"q": "programasion"}).json()
    assert [g["name"] for g in results] == ["Programacion"]


def test_tag_lifecycle(client, auth):
    group_id = client.post("/api/groups", json={"name": "Tagged"}, headers=auth).json()["id"]

    tag = client.post("/api/tags", json={"name": "Mates"}, headers=auth)
    assert tag.status_code == 200
    tag_id = tag.json()["id"]

    assigned = client.post(f"/api/groups/{group_id}/tags", json={"tag_id": tag_id}, headers=auth)
    assert assigned.status_code == 200
    assert client.get(f"/api/groups/{group_id}").json()["tags"] == [{"id": tag_id, "name": "Mates"}]

    client.delete(f"/api/groups/{group_id}/tags/{tag_id}", headers=auth)
    assert client.get(f"/api/groups/{group_id}").json()["tags"] == []


def test_duplicate_tag_is_rejected(client, auth):
    client.post("/api/tags", json={"name": "Dup"}, headers=auth)
    assert client.post("/api/tags", json={"name": "Dup"}, headers=auth).status_code == 400


def test_login_lockout_after_three_attempts(client):
    for _ in range(2):
        assert client.post("/api/admin/login", json={"password": "wrong"}).status_code == 401
    assert client.post("/api/admin/login", json={"password": "wrong"}).status_code == 403
    assert client.get("/api/admin/status").json()["locked"] is True


def test_unknown_api_route_returns_404(client):
    assert client.get("/api/does-not-exist").status_code == 404


def test_important_links_crud(client, auth):
    created = client.post(
        "/api/important-links",
        json={"title": "Reglamento", "description": "normas", "url": "https://example.com"},
        headers=auth,
    )
    assert created.status_code == 200
    link_id = created.json()["id"]

    links = client.get("/api/important-links").json()
    assert any(link["id"] == link_id for link in links)

    assert client.delete(f"/api/important-links/{link_id}", headers=auth).status_code == 200
