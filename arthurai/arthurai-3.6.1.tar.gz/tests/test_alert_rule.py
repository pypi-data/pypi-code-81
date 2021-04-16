import pytest

from arthurai.core.models import ArthurModel
from arthurai.core.alerts import AlertRule, AlertRuleBound, AlertMetric, AlertRuleSeverity
from arthurai.client.base import BaseApiClient
from tests import MockResponse


alert_rule_object = AlertRule(
    bound=AlertRuleBound.Upper,
    threshold=0.5,
    metric=AlertMetric.AveragePrediction,
    severity=AlertRuleSeverity.Warning
)

alert_rule_dict = {
    "bound": "upper",
    "threshold": 0.5,
    "metric": "Average Prediction",
    "severity": "warning",
    "enabled": True
}


def patch_alert_rule_post(*args, **kwargs):
    assert kwargs['data'] == alert_rule_dict
    alert_rule_object.id = "123456789"
    return MockResponse(alert_rule_object, 200)


def path_alert_rule_get(*args, **kwargs):
    alert_rule_list = {
      "data": [
        {
          "metric": "Total Inference Count By Class",
          "attribute_name": "dog",
          "threshold": 200,
          "bound": "lower",
          "severity": "warning",
          "lookback_period": 360,
          "subsequent_alert_wait_time": 720,
          "enabled": True,
          "id": "2905da23-fa72-4299-92d6-40007d3a2a03",
          "attribute_id": "37c8a2cb-b607-4b77-9a89-9d34ee6e3516"
        },
        {
          "metric": "Total Inference Count By Class",
          "attribute_name": "dog",
          "threshold": 200,
          "bound": "lower",
          "severity": "warning",
          "lookback_period": 360,
          "subsequent_alert_wait_time": 720,
          "enabled": True,
          "id": "2905da23-fa72-4299-92d6-40007d3a2a03",
          "attribute_id": "37c8a2cb-b607-4b77-9a89-9d34ee6e3516"
        }
      ],
      "page": 1,
      "page_size": 20,
      "total_pages": 1,
      "total_count": 20
    }
    return MockResponse(alert_rule_list, 200)


def patch_alert_rule_patch(*args, **kwargs):
    alert_rule_dict["id"] = "123456789"
    return MockResponse(alert_rule_dict, 200)


class TestAlertRule:

    def test_alert_rule_create(self, monkeypatch, mock_cred_env_vars, binary_classification_model: ArthurModel):
        # test successful creation of alert rule
        monkeypatch.setattr(BaseApiClient, "post", patch_alert_rule_post)
        res = binary_classification_model.create_alert_rule(**alert_rule_dict)
        assert res == alert_rule_object

        # test creating alert rule using an AlertRule object
        res = binary_classification_model.create_alert_rule(alert_rule=alert_rule_object)
        assert res == alert_rule_object

    def test_get_alert_rules(self, monkeypatch, mock_cred_env_vars, binary_classification_model: ArthurModel):
        monkeypatch.setattr(BaseApiClient, "get", path_alert_rule_get)
        res = binary_classification_model.get_model_alert_rules()
        assert len(res) == 2
        for alert_rule in res:
            assert isinstance(alert_rule, AlertRule)

    def test_alert_rule_patch(self, monkeypatch, mock_cred_env_vars, binary_classification_model: ArthurModel):
        # test updating alert rule passing id separately
        monkeypatch.setattr(BaseApiClient, "patch", patch_alert_rule_patch)
        res = binary_classification_model.update_alert_rule(alert_rule_object, "123456789")
        alert_rule_object.id = "123456789"
        assert res == alert_rule_object

        # test creating alert rule using an AlertRule object
        res = binary_classification_model.update_alert_rule(alert_rule=alert_rule_object)
        alert_rule_object.id = "123456789"
        assert res == alert_rule_object

        # ensure an error is thrown if an alert rule id is not provided
        alert_rule_object.id = None
        with pytest.raises(Exception) as context:
            binary_classification_model.update_alert_rule(alert_rule_object)

        assert "alert_rule_to_update must have a valid id" in context.value.args[0]



