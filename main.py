import logging

from src.agent import Agent
from src.configs import AgentConfig


def main():
    prepare_logger()
    Agent(AgentConfig()).start()


def prepare_logger():
    logging.basicConfig(level=logging.INFO,
                        format="onyxdb-agent: %(asctime)s.%(msecs)03d %(levelname)s %(name)s.%(funcName)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    main()
