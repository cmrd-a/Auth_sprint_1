from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_register_v1(make_post_request):
    # act
    response = make_post_request(
        method="http://localhost:6379/user/v1/register",
        body={"email": "test_user@gmail.com", "password": "password_test_user"},
    )

    # assert
    assert response.status == HTTPStatus.OK
