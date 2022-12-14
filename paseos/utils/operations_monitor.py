import csv

from loguru import logger
from dotmap import DotMap
import pykep as pk

from paseos.actors.base_actor import BaseActor
from paseos.actors.spacecraft_actor import SpacecraftActor


class OperationsMonitor:
    """This class is used to track actor status and activities over time."""

    def __init__(self, actor_name):
        """Initializes the OperationsMonitor

        Args:
            actor_name (str): Name of the local actor.
        """
        logger.trace("Initializing OperationsMonitor for " + actor_name)
        self._actor_name = actor_name
        self._log = DotMap(_dynamic=False)
        self._log.timesteps = []
        self._log.current_activity = []
        self._log.battery_ratio = []
        self._log.is_in_eclipse = []
        self._log.known_actors = []
        self._log.position = []
        self._log.velocity = []

    def log(
        self,
        local_actor: BaseActor,
        known_actors: list,
    ):
        """Log the current time step.

        Args:
            local_actor (BaseActor): The local actors whose status we are monitoring.
            known_actors (list): List of names of the known actors.
        """
        logger.trace("Logging iteration")
        assert local_actor.name == self._actor_name, (
            "Expected actor's name was" + self._actor_name
        )
        self._log.timesteps.append(local_actor.local_time.mjd2000 * pk.DAY2SEC)
        self._log.current_activity.append(local_actor.current_activity)
        self._log.position.append(local_actor._last_position)
        self._log.velocity.append(local_actor._last_velocity)
        self._log.known_actors.append(known_actors)
        if isinstance(local_actor, SpacecraftActor):
            self._log.battery_ratio.append(local_actor.battery_level_ratio)
        else:
            self._log.battery_ratio.append(1.0)

        if local_actor._last_eclipse_status is None:
            self._log.is_in_eclipse.append(False)
        else:
            self._log.is_in_eclipse.append(local_actor._last_eclipse_status)

    def save_to_csv(self, filename):
        """Write the created log file to a csv file.

        Args:
            filename (str): File to store the log in.
        """
        logger.trace("Writing status log file to " + filename)
        with open(filename, "w", newline="") as f:
            w = csv.DictWriter(f, self._log.keys())
            w.writeheader()
            for i in range(len(self._log.timesteps)):
                row = {
                    "timesteps": self._log.timesteps[i],
                    "current_activity": self._log.current_activity[i],
                    "position": self._log.position[i],
                    "velocity": self._log.velocity[i],
                    "known_actors": self._log.known_actors[i],
                    "battery_ratio": self._log.battery_ratio[i],
                    "is_in_eclipse": self._log.is_in_eclipse[i],
                }
                w.writerow(row)
