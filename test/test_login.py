def test_login_success(client):
    response = client.post("/v1/user/account/login", json={
        "username": "admin", "password": "12345678"
    })
    assert response.json()["message"] == "登陆成功😄"


def test_login_wrong_password(client):
    response = client.post("/v1/user/account/login", json={
        "username": "admin", "password": "00000000"
    })
    assert "用户名或密码错误" in response.json()["message"]


def test_user_info_no_token(client):
    response = client.get("/v1/admin/user/info")
    assert response.status_code == 401


def test_user_info_with_token(client):
    # 先登录
    client.post("/v1/user/account/login", json={
        "username": "admin", "password": "12345678"
    })
    token = client.cookies.get("X-token")
    # 再访问
    response = client.get("/v1/admin/user/info", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()["data"]["username"] == "admin"


def test_login_validation_error(client):
    response = client.post("/v1/user/account/login", json={
        "username": "ab", "password": "123"
    })
    assert response.status_code == 422


def test_delete_user_not_found(client):
    # 先登录
    client.post("/v1/user/account/login", json={
        "username": "admin", "password": "12345678"
    })
    token = client.cookies.get("X-token")
    # 删不存在的
    response = client.delete("/v1/admin/user/del?user_id=99999", headers={"Authorization": token})
    assert "删除失败" in response.json()["message"]