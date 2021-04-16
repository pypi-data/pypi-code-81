from tests.client_fixtures import simulation_overview
from threedi_settings.pretty.output.http import ResponseTree


# smoke test
def test_response_tree(simulation_overview):
    rt = ResponseTree(simulation_overview)
    rt.show()
