import yaml
from jinja2 import Environment
from uuid import uuid4
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from threedi_api_client.threedi_api_client import ThreediApiClient

from threedi_cmd.models import WRAPPERS
from threedi_cmd.models.scenario import Scenario
from threedi_cmd.commands.settings import WebSocketSettings


class ScenarioParser:
    """
    Parses a YAML file into a Scenario object
    """

    def __init__(self, filepath: str, context: Dict):
        """
        :param filepath: The filepath to the YAML file
        :param context: The context to use for rendering the YAML (Jinja2) file
        """
        self.filepath = Path(filepath)
        self.context = context

    def get_context(self) -> Dict:
        """
        Get default context
        """
        context = {
            "simulation_name": "run_" + uuid4().hex,
            "datetime_now": datetime.utcnow().isoformat(),
        }
        context.update(self.context)
        return context

    def _render_template(self) -> str:
        """
        Render the template using the given context
        """
        with open(self.filepath.as_posix()) as f:
            env = Environment(extensions=["jinja2_time.TimeExtension"])
            env.datetime_format = "%Y-%m-%dT%H:%M:%S"
            data = env.from_string(f.read()).render(self.get_context())
        return data

    def parse(
        self,
        threedi_api_client: ThreediApiClient,
        websocket_settings: WebSocketSettings,
        base_path: Optional[Path] = None,
    ) -> Scenario:
        """
        Parse the YAML file.

        :param threedi_api_client: Injected into the Scenario,
                                   allowing to execute API calls.

        :returns: Scenario instance
        """
        template = self._render_template()
        data = yaml.load(template, Loader=yaml.FullLoader)
        return Scenario(
            data=data,
            threedi_api_client=threedi_api_client,
            wrappers=WRAPPERS,
            websocket_settings=websocket_settings,
            base_path=base_path,
        )
