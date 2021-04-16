from behave import when
import refinitiv.dataplatform as rdp


@when(u'User performs convert symbol "{symbol}" from "{from_symbol_type}" type to "{to_symbol_type}"')
def step_impl(context, symbol, from_symbol_type, to_symbol_type):
    if "All" in to_symbol_type:
        to_symbol_type = None
    response = rdp.Symbology.convert(symbol, from_symbol_type=from_symbol_type, to_symbol_types=to_symbol_type)
    context.response = response


@when(u'User performs convert symbol "{symbol}"')
def step_impl(context, symbol):
    response = None
    try:
        response = rdp.Symbology.convert(symbol)
    except Exception as err:
        print(err)
        context.error = err
    context.response = response
