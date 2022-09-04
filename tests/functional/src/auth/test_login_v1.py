from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_login_v1(make_post_request):
    # act
    response = await make_post_request(
        url="http://localhost:5000/users/v1/login",
        body={"email": "test_user@gmail.com", "password": "password_test_user"},
    )

    # assert
    assert response.status == HTTPStatus.CREATED
