import argparse
import car_racer.config as config
from car_racer.main import main


def parse_game_arguments():
    parser = argparse.ArgumentParser(description="Car Racer game",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--track_length",
                        type=int,
                        default=5000,
                        help="How long the track will be (in pixel)")
    parser.add_argument("--track_seed",
                        type=int,
                        default=0,
                        help="With which seed the track will be initialized")
    parser.add_argument("--corner_chance",
                        type=int,
                        default=30,
                        help="The chance of corners happening over straights")
    parser.add_argument("--corner_max_angle",
                        type=int,
                        default=90,
                        help="the maximum turn of a corner in degree")

    arguments = parser.parse_args()
    return arguments


def parse_replay_arguments():
    parser = argparse.ArgumentParser(description="Replay Car Racer games",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--replay_folder",
                        type=str,
                        default="replays",
                        help="path to where replays are saved, defaults to replays and will use the first folder there")

    arguments = parser.parse_args()
    return arguments


def race():
    args = parse_game_arguments()
    main(0, args.track_length, args.track_seed, args.corner_chance, args.corner_max_angle)


def replay():
    args = parse_replay_arguments()
    main(1, replay_folder=args.replay_folder)
