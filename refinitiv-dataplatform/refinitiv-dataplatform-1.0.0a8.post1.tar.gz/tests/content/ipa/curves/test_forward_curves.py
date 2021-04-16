from refinitiv.dataplatform.content import ipa
import response_tests


def test_curves(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "curveDefinition": {
            "currency": "EUR",
            "indexName": "EURIBOR",
            "discountingTenor": "OIS"
          },
          "forwardCurveDefinitions": [
            {
              "indexTenor": "3M",
              "forwardCurveTag": "ForwardTag",
              "forwardStartDate": "2021-02-01",
              "forwardCurveTenors": [
                "0D",
                "1D",
                "2D",
                "3M",
                "6M",
                "9M",
                "1Y",
                "2Y",
                "3Y",
                "4Y",
                "5Y",
                "6Y",
                "7Y",
                "8Y",
                "9Y",
                "10Y",
                "15Y",
                "20Y",
                "25Y"
              ]
            }
          ]
        }
      ]
    }
    """
    response = ipa.curve.Curves().get_curve(
        universe=[
            ipa.curve.ForwardCurve(
                curve_definition=ipa.curve.SwapZcCurveDefinition(
                    currency="EUR",
                    index_name="EURIBOR",
                    discounting_tenor="OIS"
                ),
                forward_curve_definitions=[
                    ipa.curve.ForwardCurveDefinition(
                        index_tenor="3M",
                        forward_curve_tag="ForwardTag",
                        forward_start_date="2021-02-01",
                        forward_curve_tenors=[
                            "0D",
                            "1D",
                            "2D",
                            "3M",
                            "6M",
                            "9M",
                            "1Y",
                            "2Y",
                            "3Y",
                            "4Y",
                            "5Y",
                            "6Y",
                            "7Y",
                            "8Y",
                            "9Y",
                            "10Y",
                            "15Y",
                            "20Y",
                            "25Y"
                        ]
                    )
                ]
            )
        ],
        outputs=[
            "Constituents"
        ]
    )
    response_tests.success_response_tests(response)


def test_2(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "curveDefinition": {
            "currency": "EUR",
            "indexName": "EURIBOR",
            "discountingTenor": "OIS"
          },
          "forwardCurveDefinitions": [
            {
               "indexTenor": "6M",
               "forwardStartTenor": "3M",
               "forwardCurveTenors": [
                 "0D",
                 "1D",
                 "2D",
                 "3M",
                 "6M",
                 "9M",
                 "1Y",
                 "2Y",
                 "3Y",
                 "4Y",
                 "5Y",
                 "6Y",
                 "7Y",
                 "8Y",
                 "9Y",
                 "10Y",
                 "15Y",
                 "20Y",
                 "25Y"
              ]
            }
          ]
        }
      ]
    }
    """
    response = ipa.curve.Curves().get_curve(universe=[
        ipa.curve.ForwardCurve(
            curve_definition=ipa.curve.SwapZcCurveDefinition(
                currency="EUR",
                index_name="EURIBOR",
                discounting_tenor="OIS"
            ),
            forward_curve_definitions=[
                ipa.curve.ForwardCurveDefinition(
                    index_tenor="6M",
                    forward_start_tenor="3M",
                    forward_curve_tenors=[
                        "0D",
                        "1D",
                        "2D",
                        "3M",
                        "6M",
                        "9M",
                        "1Y",
                        "2Y",
                        "3Y",
                        "4Y",
                        "5Y",
                        "6Y",
                        "7Y",
                        "8Y",
                        "9Y",
                        "10Y",
                        "15Y",
                        "20Y",
                        "25Y"
                    ]
                )
            ]
        )
    ])
    response_tests.success_response_tests(response)


def test_3(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "curveParameters": {
            "valuationDate": "2020-03-17",
            "useSteps": false
          },
          "curveDefinition": {
            "currency": "EUR",
            "indexName": "EURIBOR",
            "discountingTenor": "OIS"
          },
          "forwardCurveDefinitions": [
            {
              "indexTenor": "3M",
              "forwardStartTenor": "6M",
              "forwardCurveTenors": [
                "0D",
                "1D",
                "2D",
                "3M",
                "6M",
                "9M",
                "1Y",
                "2Y",
                "3Y",
                "4Y",
                "5Y",
                "6Y",
                "7Y",
                "8Y",
                "9Y",
                "10Y",
                "15Y",
                "20Y",
                "25Y"
              ]
            }
          ]
        }
      ]
    }
    """
    response = ipa.curve.Curves().get_curve(universe=[
        ipa.curve.ForwardCurve(
            curve_parameters=ipa.curve.SwapZcCurveParameters(
                valuation_date="2020-03-17",
                use_steps=False
            ),
            curve_definition=ipa.curve.SwapZcCurveDefinition(
                currency="EUR",
                index_name="EURIBOR",
                discounting_tenor="OIS"
            ),
            forward_curve_definitions=[
                ipa.curve.ForwardCurveDefinition(
                    index_tenor="3M",
                    forward_start_tenor="6M",
                    forward_curve_tenors=[
                        "0D",
                        "1D",
                        "2D",
                        "3M",
                        "6M",
                        "9M",
                        "1Y",
                        "2Y",
                        "3Y",
                        "4Y",
                        "5Y",
                        "6Y",
                        "7Y",
                        "8Y",
                        "9Y",
                        "10Y",
                        "15Y",
                        "20Y",
                        "25Y"
                    ]
                )
            ]
        )
    ])
    response_tests.success_response_tests(response)
