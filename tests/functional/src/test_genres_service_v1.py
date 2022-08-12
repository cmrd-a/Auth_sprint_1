from http import HTTPStatus

import pytest
from testdata.genres import genres


@pytest.mark.asyncio
async def test_genres_list__genres_present__return_genres(make_get_request, create_genres):
    # act
    response = await make_get_request("/v1/genres")

    # assert
    assert response.body["genres"] == genres


@pytest.mark.asyncio
async def test_genres_list__no_genres__return_status_404(make_get_request):
    # act
    response = await make_get_request("/v1/genres")

    # assert
    assert response.body["detail"] == "genres not found"
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_genre_details__genres_present__return_genre(make_get_request, create_genres):
    # act
    response = await make_get_request("/v1/genres/1")

    # assert
    assert response.body == genres[0]


@pytest.mark.asyncio
async def test_genre_details__no_genre__return_status_404(make_get_request, create_genres):
    # act
    response = await make_get_request("/v1/genres/100")

    # assert
    assert response.body["detail"] == "genre not found"
    assert response.status == HTTPStatus.NOT_FOUND
