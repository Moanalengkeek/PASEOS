from dotmap import DotMap
from loguru import logger


def check_cfg(cfg: DotMap):
    """This function validates that all required entries are in the config.

    Args:
        cfg (DotMap): Run config you intend to use.
    """
    major_categories = ["sim", "io"]
    _check_for_keys(cfg, major_categories)
    _check_entry_types(cfg, major_categories)
    _check_value_ranges(cfg, major_categories)
    logger.debug("Config validated successfully.")


def _check_for_keys(cfg: DotMap, major_categories: list) -> None:
    """Checks that all required keys are present in the config"""
    required_keys = [
        "start_time",
        "dt",
        "activity_timestep",
        "time_multiplier",
        "logging_interval",
    ]
    # Check only expected categories are there that are expected
    for key in cfg.keys():
        if key not in major_categories:
            raise KeyError(f"Found unexpected category in cfg: {key}")

    # Check required keys are there
    for key in required_keys:
        key_found = False
        for category in major_categories:
            if key in cfg[category]:
                key_found = True
        if not key_found:
            raise KeyError(f"CFG missing required key: {key}")

    # Check no other keys are there (to e.g. catch typos)
    for category in major_categories:
        for key in cfg[category].keys():
            if key not in required_keys:
                raise KeyError(
                    f"CFG Key {key} is not a valid key. Valid are {required_keys}"
                )


def _check_entry_types(cfg: DotMap, major_categories: list) -> None:
    """Check that all entries in the config are of the correct type"""
    # fmt: off
    integer_keys = []
    float_keys = ["start_time","dt","activity_timestep","time_multiplier","logging_interval",]
    boolean_keys = []
    string_keys = []
    list_keys = []
    # fmt: on

    for key in integer_keys:
        for category in major_categories:
            if key in cfg[category].keys() and not isinstance(cfg[category][key], int):
                raise TypeError(f"{key} must be an integer")

    for key in float_keys:
        for category in major_categories:
            if key in cfg[category].keys() and not isinstance(
                cfg[category][key], float
            ):
                raise TypeError(f"{key} must be a float")

    for key in boolean_keys:
        for category in major_categories:
            if key in cfg[category].keys() and not isinstance(cfg[category][key], bool):
                raise TypeError(f"{key} must be a boolean")

    for key in string_keys:
        for category in major_categories:
            if key in cfg[category].keys() and not isinstance(cfg[category][key], str):
                raise TypeError(f"{key} must be a string")

    for key in list_keys:
        for category in major_categories:
            if key in cfg[category].keys() and not isinstance(cfg[category][key], list):
                raise TypeError(f"{key} must be a list")


def _check_value_ranges(cfg: DotMap, major_categories: list) -> None:
    """Check that all values in the config are within the correct range.
    This throws runtime errors as ValueErrors are caught in training to avoid NaNs crashing the training."""

    # fmt: off
    positive_value_keys = ["dt","activity_timestep","time_multiplier","logging_interval",]
    positive_or_zero_value_keys = ["start_time"]
    # fmt: on

    for key in positive_value_keys:
        for category in major_categories:
            if key in cfg[category].keys() and not (cfg[category][key] > 0):
                raise RuntimeError(f"{key} must be a positive integer")

    for key in positive_or_zero_value_keys:
        for category in major_categories:
            if key in cfg[category].keys() and not (cfg[category][key] >= 0):
                raise RuntimeError(f"{key} must be a positive or zero integer")
