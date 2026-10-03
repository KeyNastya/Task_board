from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_create_task(monkeypatch):
    # В тесте не отправляем реальный вебхук
    monkeypatch.setattr(main, "send_webhook", lambda task: True)

    response = client.post(
        "/api/tasks",
        json={"title": "Тест", "description": "Описание"}
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Тест"
    assert data["description"] == "Описание"
    assert data["status"] == "new"
    assert "id" in data
    assert "created_at" in data
