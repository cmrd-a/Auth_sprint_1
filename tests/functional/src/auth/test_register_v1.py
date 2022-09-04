from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_register_v1(make_post_request):
    # act
    response = await make_post_request(
        url="http://localhost:5000/users/v1/register",
        body={"email": "test_user@gmail.com", "password": "password_test_user"},
    )

    # assert
    assert response.status == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_register_v1__no_films__return_status_400(make_post_request):
    # arrange

    # act
    response = await make_post_request(
        url="http://localhost:5000/users/v1/register",
        body={"email": "test_user@gmail.com", "password": "password_test_user"},
    )

    # assert
    assert response.body["detail"] == "Bad username or password"
    assert response.status == HTTPStatus.BAD_REQUEST