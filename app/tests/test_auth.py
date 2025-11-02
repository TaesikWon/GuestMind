# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine

client = TestClient(app)

# ✅ 테스트용 DB 초기화
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_signup_success():
    """회원가입 성공 테스트"""
    response = client.post("/auth/signup", params={"username": "testuser", "password": "1234"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


def test_signup_duplicate():
    """중복 회원가입 테스트"""
    client.post("/auth/signup", params={"username": "testuser2", "password": "1234"})
    response = client.post("/auth/signup", params={"username": "testuser2", "password": "1234"})
    assert response.status_code == 400
    assert "exists" in response.json()["detail"].lower()


def test_login_success():
    """로그인 성공 테스트 (JWT 쿠키 포함 확인)"""
    client.post("/auth/signup", params={"username": "loginuser", "password": "1234"})
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "1234"},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_login_fail():
    """잘못된 비밀번호로 로그인 실패"""
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "wrong"},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert "Invalid" in response.json()["detail"]


def test_refresh_token():
    """Refresh Token으로 새 Access Token 발급"""
    client.post("/auth/signup", params={"username": "refreshuser", "password": "1234"})
    login = client.post(
        "/auth/login",
        data={"username": "refreshuser", "password": "1234"},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    refresh_cookie = login.cookies.get("refresh_token")

    response = client.post("/auth/refresh", cookies={"refresh_token": refresh_cookie})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_logout():
    """로그아웃 → 쿠키 제거 확인"""
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"
