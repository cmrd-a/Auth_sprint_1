from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_logout_v1(make_post_request):
    # act
    response = await make_post_request(
        url="http://localhost:5000/users/v1/change-password",
    )

    # assert
    assert response.status == HTTPStatus.OK