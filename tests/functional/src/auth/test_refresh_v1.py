from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_register_v1(make_post_request):
    # act
    response = await make_post_request(
        url="http://localhost:5000/users/v1/refresh",
    )

    # assert
    assert response.status == HTTPStatus.OK