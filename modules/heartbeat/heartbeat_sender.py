"""
Heartbeat sending logic.
"""

from pymavlink import mavutil


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
class HeartbeatSender:
    """
    HeartbeatSender class to send a heartbeat
    """

    __private_key = object()

    @classmethod
    def create(
        cls,
        connection: mavutil.mavfile,
        args: object,  # Put your own arguments here
    ) -> "tuple[bool, HeartbeatSender | None]":
        """
        Falliable create (instantiation) method to create a HeartbeatSender object.
        """
        # Create a HeartbeatSender object
        try:
            instance = HeartbeatSender(key=HeartbeatSender.__private_key, connection=connection, args=args)
            return True, instance
        except Exception:
            return False, None

    def __init__(
        self,
        key: object,
        connection: mavutil.mavfile,
        args: object,  # Put your own arguments here
    ) -> None:
        assert key is HeartbeatSender.__private_key, "Use create() method"

        # Do any intializiation here
        self.__connection = connection

    def run(
        self,
        args: object,  # Put your own arguments here
    ) -> bool:
        """
        Attempt to send a heartbeat message.
        """
        # Send a heartbeat message
        try:
            self.__connection.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0
            )
            return True
        except Exception:
            return False


# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
