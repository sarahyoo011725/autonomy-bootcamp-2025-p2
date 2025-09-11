"""
Heartbeat receiving logic.
"""

from pymavlink import mavutil

from ..common.modules.logger import logger


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
class HeartbeatReceiver:
    """
    HeartbeatReceiver class to send a heartbeat
    """
    __private_key = object()
    __connection : mavutil.mavfile
    __logger: logger.Logger
    __connected = False
    __disconnection_timestamp = 0

    @classmethod
    def create(
        cls,
        connection: mavutil.mavfile,
        local_logger: logger.Logger,
        args: object, 
    ) -> "tuple[bool, HeartbeatReceiver | None]":
        """
        Falliable create (instantiation) method to create a HeartbeatReceiver object.
        """
        try:
            instance = HeartbeatReceiver(key=HeartbeatReceiver.__private_key, connection=connection, args=args)
            instance.__logger = local_logger
            return True, instance
        except Exception:
            local_logger.debug("Failed to create a HeartbeatReceiver object.")
            return False, None

    def __init__(
        self,
        key: object,
        connection: mavutil.mavfile,
        args: object,  # Put your own arguments here
    ) -> None:
        assert key is HeartbeatReceiver.__private_key, "Use create() method"

        # Do any intializiation here
        self.__private_key = key
        self.__connection = connection 
        
    def run(
        self,
        condition: str,
        type: str,
        blocking: bool,
        timeout: float,
        disconnection_threshold: int,
        args: object,  # Put your own arguments here
    ) -> str:
        """
        Attempt to recieve a heartbeat message.
        If disconnected for over a threshold number of periods,
        the connection is considered disconnected.
        """
        msg = self.__connection.recv_match(type=type, condition=condition, blocking=blocking, timeout=timeout)

        if (msg.get_type() == type): # type: ignore
            self.__connected = True
            self.__disconnection_timestamp = 0
        else:
            self.__disconnection_timestamp += 1 
            if (self.__disconnection_timestamp >= disconnection_threshold):
                self.__connected = False
                self.__logger.info("The receiver stayed disconnected over the threshold.")
        
        return "CONNECTED" if self.__connected else "DISCONNECTED"

# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
