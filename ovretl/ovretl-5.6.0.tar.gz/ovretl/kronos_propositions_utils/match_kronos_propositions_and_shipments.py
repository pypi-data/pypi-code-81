import pandas as pd


def match_kronos_propositions_and_shipments(
    kronos_propositions_df: pd.DataFrame, shipments_all_propositions_df: pd.DataFrame
):
    kronos_propositions_df = kronos_propositions_df.rename(columns={"id": "kronos_proposition_id"})
    kronos_propositions_df = kronos_propositions_df.dropna(subset=["shipment_id"])

    # Add a foreign key, "foresea_name", to mark computed quotations which are the most relevant
    kronos_propositions_df = pd.merge(
        kronos_propositions_df,
        shipments_all_propositions_df[["proposition_id", "kronos_state"]].dropna(subset=["proposition_id"]),
        how="left",
        on="proposition_id",
    )

    # Sort with foresea_name first to put most relevant CQs first
    kronos_propositions_df = kronos_propositions_df.sort_values(
        by=["shipment_id", "proposition_id", "created_at"], ascending=False,
    )
    kronos_propositions_df = kronos_propositions_df.drop_duplicates(subset=["shipment_id"])
    return kronos_propositions_df.drop(["foresea_name"], axis=1, errors="ignore")
