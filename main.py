# main.py
import argparse
import logging
from game.game import Game

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO"],
        help="Set the logging level"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    game = Game()
    game.run()

if __name__ == '__main__':
    main()
