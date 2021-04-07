import argparse
import yaml

import clone_mrem_section

def main(
        host: str,
        token: str,
        section_name: str) -> None:
    """ Clones the given NEMM MREM section to NOAA's FSB project the without copying annotations

    :param host: Tator URL
    :param token: Tator API token
    :param section_name: Section to clone

    """

    print("\n")
    print("----------------------------------------------------------------")
    print("Clone MREM NEMM Tator Trip to NOAA FSB Tator's Project: STARTED")
    print("----------------------------------------------------------------")
    print("\n")


    clone_mrem_section.main(
        in_host=host,
        in_token=token,
        in_src_project=30,
        in_dest_project=32,
        in_src_section_name=section_name,
        in_dest_section_name=section_name,
        in_copy_annotations=False)


    print("\n")
    print("----------------------------------------------------------------")
    print("Clone MREM NEMM Tator Trip to NOAA FSB Tator's Project: FINISHED")
    print("----------------------------------------------------------------")
    print("\n")

def parse_args() -> None:
    """ Process script's arguments
    """

    parser=argparse.ArgumentParser()
    parser.add_argument("--info-file", required=True, help=".yaml file with Tator information")
    parser.add_argument("--trip-name", required=True, help="Name of section/trip in NEMM MREM Tator Project to clone")
    args = parser.parse_args()
    return args

def script_main() -> None:
    """ Script's entry point
    """

    args = parse_args()
    with open(args.info_file, "r") as file_handle:
        info = yaml.safe_load(file_handle)

    main(host=info["tator"]["host"], token=info["tator"]["token"], section_name=args.trip_name)

if __name__ == "__main__":
    script_main()