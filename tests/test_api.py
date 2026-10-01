from fastapi.testclient import TestClient
from civic_media.api import app

def test_editorial_review(monkeypatch, tmp_path):
    monkeypatch.setenv("CIVIC_MEDIA_DB", str(tmp_path / "media.db"))
    monkeypatch.setenv("CIVIC_MEDIA_TOKEN", "test-token")
    client = TestClient(app)
    headers = {"x-operator-token":"test-token"}
    brief = {"id":"b1","outlet_id":"science","headline":"Example",
             "editorial_class":"news","evidence":[{"packet_id":"p1","revision":1}]}
    assert client.post("/v1/editorial", json=brief).status_code == 401
    assert client.post("/v1/editorial", json=brief, headers=headers).status_code == 201
    assert client.post("/v1/editorial/b1/approve", json={"reviewer":"A","note":"Reviewed"}, headers=headers).status_code == 409
    assert client.post("/v1/editorial/b1/submit", headers=headers).json()["status"] == "pending_review"
    assert client.post("/v1/editorial/b1/approve", json={"reviewer":"A","note":"Reviewed"}, headers=headers).json()["status"] == "approved"
    assert len(client.get("/v1/editorial/b1/audit", headers=headers).json()) == 3
