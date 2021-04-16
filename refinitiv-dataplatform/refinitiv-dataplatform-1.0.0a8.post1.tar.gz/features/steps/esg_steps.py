import asyncio

from behave import given, when
from behave.api.async_step import run_until_complete

import refinitiv.dataplatform as rdp


@given(u'code is "{universe}"')
def step_impl(context, universe):
    context.universe = universe


@given(u'range is "{start}":"{end}"')
def step_impl(context, start, end):
    context.start = start
    context.end = end


@when(u'User performs get list of instruments')
def step_impl(context):
    response = rdp.ESG.get_universe(
        session=context.platform_session)
    context.response = response


def get_arguments_from(context):
    universe = getattr(context, "universe", None)
    start = getattr(context, "start", None)
    end = getattr(context, "end", None)
    return end, start, universe


@when(u'User performs get basic view')
def step_impl(context):
    *_, universe = get_arguments_from(context)

    response = None
    try:
        response = rdp.ESG.get_basic_overview(
            universe=universe,
            session=context.platform_session)
    except Exception as err:
        print(err)
        context.error = err

    context.response = response


@when(u'User performs get scores-standard view')
def step_impl(context):
    end, start, universe = get_arguments_from(context)

    response = None
    try:
        response = rdp.ESG.get_standard_scores(
            universe=universe,
            start=start,
            end=end,
            session=context.platform_session)
    except Exception as err:
        context.error = err
        print(err)
    context.response = response


@when(u'User performs get measures-standard view')
def step_impl(context):
    end, start, universe = get_arguments_from(context)

    response = None
    try:
        response = rdp.ESG.get_standard_measures(
            universe=universe,
            start=start,
            end=end,
            session=context.platform_session)
    except Exception as err:
        context.error = err
        print(err)
    context.response = response


@when(u'User performs get measures-full view')
def step_impl(context):
    end, start, universe = get_arguments_from(context)

    response = None
    try:
        response = rdp.ESG.get_full_measures(
            universe=universe,
            start=start,
            end=end,
            session=context.platform_session)
    except Exception as err:
        context.error = err
        print(err)

    context.response = response


@when(u'User performs get scores-full view in callback')
@run_until_complete
async def step_impl(context):
    fut = asyncio.Future()

    def on_response(esg, response):
        context.response = response
        fut.set_result(True)

    end, start, universe = get_arguments_from(context)

    try:
        rdp.ESG.get_full_scores(
            universe=universe,
            start=start,
            end=end,
            session=context.platform_session,
            on_response=on_response)
    except Exception as err:
        print(err)
        fut.set_result(True)
        context.error = err

    await fut
