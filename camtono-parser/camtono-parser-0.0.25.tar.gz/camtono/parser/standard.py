def format_query(query_ast: dict) -> str:
    from .format import BaseFormatter
    return BaseFormatter().format(query_ast)


def parse_query(query: str) -> dict:
    from .parse import Parser
    return Parser().parse(query)
