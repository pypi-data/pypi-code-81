import refinitiv.dataplatform as rdp


def test(open_session):
    session = open_session

    endpoint_params = rdp.Endpoint.Params(
        session=session,
        url='/data/historical-pricing/v1/views/events/{universe}'
    )
    request_params = rdp.Endpoint.Request.Params(
        method="GET",
        path_params={"universe": "VOD.L"},
    )
    endpoint = rdp.DeliveryFactory.create_end_point_with_params(endpoint_params)

    result = endpoint.send_request_with_params(request_params)

    assert result
    assert result.data
    assert result.data.raw
    assert result.data.df is None
