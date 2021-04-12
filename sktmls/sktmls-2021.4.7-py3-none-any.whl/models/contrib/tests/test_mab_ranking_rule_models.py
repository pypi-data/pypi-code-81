from sktmls.models.contrib import MABRankingRuleModel


class TestMABRankingRuleModel:
    def test_000_mab_valid_without_tday(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "card_ranking": {
                    "mp_point_popular_seg": [10, 10],
                    "mp_point_new_seg": [20, 15],
                    "mp_point_context_seg": [10, 3],
                }
            },
        )
        mocker.patch("numpy.random.beta", side_effect=[0.3, 0.4, 0.1])

        mrrm = MABRankingRuleModel(
            model_name="test_model",
            model_version="test_version",
            feature="seg_id",
            mab_item_profile_info={"profile_id": "test_profile", "key": "card_ranking"},
            item_info={"id": "test_id", "name": "test_name", "type": "test_type", "props_key": "ranking"},
            num_pick=0,
            random_cycle="daily",
        )
        results = mrrm.predict(["test_seg"])

        assert len(results["items"]) == 1
        assert results["items"][0]["id"] == "test_id"
        assert results["items"][0]["name"] == "test_name"
        assert results["items"][0]["type"] == "test_type"
        assert results["items"][0]["props"] == {
            "ranking": ["mp_point_new_seg", "mp_point_popular_seg", "mp_point_context_seg"]
        }

    def test_001_mab_valid_num_pick(self, mocker):
        mocker.patch(
            "sktmls.apis.MLSProfileAPIClient.get_item_profile",
            return_value={
                "card_ranking": {
                    "mp_point_popular_seg": [10, 10],
                    "mp_point_new_seg": [20, 15],
                    "mp_point_context_seg": [10, 3],
                }
            },
        )
        mocker.patch("numpy.random.beta", side_effect=[0.1, 0.2, 0.3])

        mrrm = MABRankingRuleModel(
            model_name="test_model",
            model_version="test_version",
            feature="seg_id",
            mab_item_profile_info={"profile_id": "test_profile", "key": "card_ranking"},
            item_info={"id": "test_id", "name": "test_name", "type": "test_type", "props_key": "ranking"},
            num_pick=2,
            random_cycle="daily",
        )
        results = mrrm.predict(["test_seg"])

        assert len(results["items"]) == 1
        assert results["items"][0]["id"] == "test_id"
        assert results["items"][0]["name"] == "test_name"
        assert results["items"][0]["type"] == "test_type"
        assert results["items"][0]["props"] == {"ranking": ["mp_point_context_seg", "mp_point_new_seg"]}
