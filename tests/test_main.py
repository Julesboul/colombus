from tests import test_client


def test_health_check():
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == "ok"
