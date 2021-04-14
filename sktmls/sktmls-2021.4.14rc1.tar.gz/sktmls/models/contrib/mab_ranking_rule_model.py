import calendar
import hashlib
from datetime import datetime
from typing import Any, Dict, List

import numpy as np
from pytz import timezone

from sktmls import MLSRuntimeENV
from sktmls.apis import MLSProfileAPIClient
from sktmls.models import MLSRuleModel

TZ = timezone("Asia/Seoul")
SEED_FORMAT = {
    "hourly": "%Y%m%d%H",
    "daily": "%Y%m%d",
    "weekly": "%Y%W",
    "monthly": "%Y%m",
    "yearly": "%Y",
    "none": "%c%f",
}


class MABRankingRuleModel(MLSRuleModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 클래스입니다.

    Thompson Sampling 기반의 score를 `props` 내에 정렬하여 전달하는 모델입니다.
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        feature: str,
        mab_item_profile_info: Dict[str, str],
        item_info: Dict[str, str],
        num_pick: int = 0,
        random_cycle: str = "daily",
        tday: str = None,
    ):
        """
        ## Args

        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전
        - feature: (str) 아이템 프로파일 테이블의 `item_id`를 전달 받을 feature 이름
        - mab_item_profile_info: (dict) MAB Thompson Sampling 파라미터가 저장된 아이템 프로파일 정보 (아래 예시 참조)
            - profile_id: (str) 조회할 아이템 프로파일 profile_id
            - key: (str) MAB 파라미터를 담고 있는 아이템 프로파일 key
        - item_info: (dict) 결과에 표기할 정보 (아래 예시 참조)
            - id: (str) 결과의 `id`에 표기할 값
            - name: (str) 결과의 `name`에 표기할 값
            - type: (str) 결과의 `type`에 표기할 값
            - props_key: (str) 랭킹을 전달할 `props` 내 키 값
        - num_pick: (optional) (int) 상위 score 추출 개수 (0인 경우 전체) (기본값: 0)
        - random_cycle: (optional) (str) 랜덤 시드 초기화 주기 (`hourly`|`daily`|`weekly`|`monthly`|`yearly`|`none`) (기본값: `daily`)
            - `none`의 경우 매 호출마다 초기화합니다.
        - tday: (optional) (str) T데이에 priority를 가지는 ranking candidate의 이름 (None이거나 빈값인 경우 T데이 미고려) (기본값: None)

        ## Example

        ```python
        my_model_v1 = MABRankingRuleModel(
            model_name="my_model",
            model_version="v1",
            feature="seg_id",
            mab_item_profile_info={
                "profile_id": "my_profile",
                "key": "card_ranking",
            },
            item_info={
                "id": "mp_point_card_ranking_seg",
                "name": "포인트탭카드랭킹",
                "type": "mp_point_card_ranking_seg",
                "props_key": "ranking",
            },
            num_pick=0,
            random_cycle="daily",
            tday="mp_point_tday_seg",
        )

        result = my_model_v1.predict(["seg_id"])
        ```
        """
        assert isinstance(feature, str) and len(feature) > 0, "`feature`는 유효한 문자열이어야 합니다."
        assert isinstance(mab_item_profile_info, dict), "`mab_item_profile_info`는 dict 타입이어야 합니다."
        assert "profile_id" in mab_item_profile_info, "`mab_item_profile_info`에 `profile_id` 값이 없습니다."
        assert "key" in mab_item_profile_info, "`mab_item_profile_info`에 `key` 값이 없습니다."
        assert isinstance(item_info, dict), "`item_info`는 dict 타입이어야 합니다."
        assert "id" in item_info, "`item_info`에 `id` 값이 없습니다."
        assert "name" in item_info, "`item_info`에 `name` 값이 없습니다."
        assert "type" in item_info, "`item_info`에 `type` 값이 없습니다."
        assert "props_key" in item_info, "`item_info`에 `props_key` 값이 없습니다."
        assert isinstance(num_pick, int) and num_pick >= 0, "`num_pick`이 유효하지 않습니다. 반드시 0 또는 양의 정수를 가져야 합니다."
        assert random_cycle in SEED_FORMAT, "허용되지 않는 `random_cycle`값입니다."
        assert tday is None or isinstance(tday, str) and len(tday) > 0, "`tday`는 None 또는 유효한 문자열이어야 합니다."

        super().__init__(model_name, model_version, [feature])

        self.mab_item_profile_info = mab_item_profile_info
        self.item_info = item_info
        self.num_pick = num_pick
        self.random_cycle = random_cycle
        self.tday = tday

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        pf_client = kwargs.get("pf_client") or MLSProfileAPIClient(runtime_env=MLSRuntimeENV.MMS)

        profile_id = self.mab_item_profile_info["profile_id"]
        item_id = x[0]
        key = self.mab_item_profile_info["key"]

        item_profile = pf_client.get_item_profile(profile_id=profile_id, item_id=item_id, keys=[key])
        mab_params = item_profile[key]

        now = datetime.now(TZ)
        seed = f"{item_id}{now.strftime(SEED_FORMAT[self.random_cycle])}"
        np.random.seed(int(hashlib.sha256(seed.encode()).hexdigest(), 16) % 10000)

        scores = {}
        for k, v in mab_params.items():
            try:
                scores[k] = np.random.beta(v[0], v[1])
            except (IndexError, TypeError):
                scores[k] = np.random.beta(1, 1)

        if self.tday:
            weeks = calendar.monthcalendar(now.year, now.month)
            first_full_week = weeks[0] if weeks[0][0] == 1 else weeks[1]
            if now.weekday() == 2 or now.day in first_full_week:
                scores[self.tday] = 1.0

        scores = sorted(list(scores.items()), key=lambda x: x[1], reverse=True)
        num_pick = min(self.num_pick, len(scores)) if self.num_pick > 0 else len(scores)

        return {
            "items": [
                {
                    "id": self.item_info["id"],
                    "name": self.item_info["name"],
                    "type": self.item_info["type"],
                    "props": {self.item_info["props_key"]: [k[0] for k in scores[:num_pick]]},
                }
            ]
        }
