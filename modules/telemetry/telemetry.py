"""
Telemetry gathering logic.
"""

import time

from pymavlink import mavutil

from ..common.modules.logger import logger


class TelemetryData:  # pylint: disable=too-many-instance-attributes
    """
    Python struct to represent Telemtry Data. Contains the most recent attitude and position reading.
    """

    def __init__(
        self,
        time_since_boot: int | None = None,  # ms
        x: float | None = None,  # m
        y: float | None = None,  # m
        z: float | None = None,  # m
        x_velocity: float | None = None,  # m/s
        y_velocity: float | None = None,  # m/s
        z_velocity: float | None = None,  # m/s
        roll: float | None = None,  # rad
        pitch: float | None = None,  # rad
        yaw: float | None = None,  # rad
        roll_speed: float | None = None,  # rad/s
        pitch_speed: float | None = None,  # rad/s
        yaw_speed: float | None = None,  # rad/s
    ) -> None:
        self.time_since_boot = time_since_boot
        self.x = x
        self.y = y
        self.z = z
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.z_velocity = z_velocity
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.roll_speed = roll_speed
        self.pitch_speed = pitch_speed
        self.yaw_speed = yaw_speed

    def __str__(self) -> str:
        return f"""{{
            time_since_boot: {self.time_since_boot},
            x: {self.x},
            y: {self.y},
            z: {self.z},
            x_velocity: {self.x_velocity},
            y_velocity: {self.y_velocity},
            z_velocity: {self.z_velocity},
            roll: {self.roll},
            pitch: {self.pitch},
            yaw: {self.yaw},
            roll_speed: {self.roll_speed},
            pitch_speed: {self.pitch_speed},
            yaw_speed: {self.yaw_speed}
        }}"""


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
class Telemetry:
    """
    Telemetry class to read position and attitude (orientation).
    """

    __private_key = object()
    __connection : mavutil.mavfile
    __local_logger : logger.Logger

    @classmethod
    def create(
        cls,
        connection: mavutil.mavfile,
        args,  # Put your own arguments here
        local_logger: logger.Logger,
    ) -> "tuple[bool, Telemetry | None]":
        """
        Falliable create (instantiation) method to create a Telemetry object.
        """
        try:
            instance = Telemetry(key=Telemetry.__private_key, connection=connection, args=args, local_logger=local_logger)
            return True, instance
        except Exception:
            return False, None

    def __init__(
        self,
        key: object,
        connection: mavutil.mavfile,
        local_logger: logger.Logger,
        args,  # Put your own arguments here
    ) -> None:
        assert key is Telemetry.__private_key, "Use create() method"

        self.__connection = connection
        self.__local_logger = local_logger
        

    def run(
        self,
        timeout: float,
        args,  
    ):
        """
        Receive LOCAL_POSITION_NED and ATTITUDE messages from the drone,
        combining them together to form a single TelemetryData object.
        """
        # Read MAVLink message LOCAL_POSITION_NED (32)
        # Read MAVLink message ATTITUDE (30)
        # Return the most recent of both, and use the most recent message's timestamp

        pos_msg = self.__connection.recv_match(type="LOCAL_POSITION_NED", blocking=True, timeout=timeout)

        att_msg = self.__connection.recv_match(type="ATTITUDE", blocking=True, timeout=timeout)

        if (not pos_msg):
            self.__local_logger.error("Failed to receive LOCAL_POSITION_NED message")
            return None
        
        if (not att_msg):
            self.__local_logger.error("Failed to ATTITUDE message")
            return None
        
        recent_timestamp = max(pos_msg.time_boot_ms, att_msg.time_boot_ms)

        return TelemetryData(
            time_since_boot=recent_timestamp,
            x=pos_msg.x,
            y=pos_msg.y,
            z=pos_msg.z,
            x_velocity=pos_msg.vx,
            y_velocity=pos_msg.vy,
            z_velocity=pos_msg.vz,
            roll=att_msg.roll,
            pitch=att_msg.pitch,
            yaw=att_msg.yaw,
            roll_speed=att_msg.rollspeed,
            pitch_speed=att_msg.pitchspeed,
            yaw_speed=att_msg.yawspeed
        )

# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
