import pickle

from wikivents.wikidata import WikidataClient

exported_entity_name_id_dict = {
    "Q470110": "org_american_red_cross",
    "Q1761": "gpe_dublin_ireland",
    "Q76": "human_barack_obama",
    "Q193689": "event_easter_rising"
}


def export_entities_request_content_to_pickle_files():
    for k, v in exported_entity_name_id_dict.items():
        with open(f"./{k}_{v}_request_data.pickle", mode="wb") as output_file:
            pickle.dump(WikidataClient().request(f'./wiki/Special:EntityData/{k}.json'), output_file)


if __name__ == "__main__":
    export_entities_request_content_to_pickle_files()
