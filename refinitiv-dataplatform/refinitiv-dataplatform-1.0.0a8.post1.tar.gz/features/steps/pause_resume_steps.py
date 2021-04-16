from behave import *
import refinitiv.dataplatform as rdp

use_step_matcher("re")


@step("(?P<stream_name>.+) created")
def step_impl(context, stream_name):
    """
    :type context: behave.runner.Context
    :type stream_name: str
    """
    session = context.platform_session
    if stream_name == "ItemStream":
        context.stream = rdp.OMMItemStream(session=session, name="0#.ALL/P1D")
    elif stream_name == "StreamingPrices":
        context.stream = rdp.StreamingPrices(universe=["GBP="], session=session)
    elif stream_name == "StreamingChain":
        context.stream = rdp.StreamingChain(name="0#.DJII",
                                            session=session)


@when("User set stream to pause")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.stream.pause()


@then("stream paused")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.stream.is_pause()


@step("stream paused")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.stream.pause()


@when("User resume stream")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.stream.resume()


@then("stream resumed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert not context.stream.is_pause()


@step("I close session")
def close_session(context):
    session = context.platform_session
    session.close()
