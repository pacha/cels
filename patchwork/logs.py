import coloredlogs  # type: ignore


def init_logging(log_level):
    coloredlogs.install(fmt="%(levelname)8s | %(message)s", level=log_level)
