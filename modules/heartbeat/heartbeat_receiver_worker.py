"""
Heartbeat worker that sends heartbeats periodically.
"""

import os
import pathlib

from pymavlink import mavutil

from utilities.workers import queue_proxy_wrapper
from utilities.workers import worker_controller
from . import heartbeat_receiver
from ..common.modules.logger import logger


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
def heartbeat_receiver_worker(
    connection: mavutil.mavfile,
    controller: worker_controller.WorkerController,
    condition: str,
    type: str,
    blocking: bool,
    blocking_timeout: float,
    queue_timeout: float,
    disconnect_threshold: int,
    output_queue_manager: queue_proxy_wrapper.QueueProxyWrapper,
    args: object,  # Place your own arguments here
    # Add other necessary worker arguments here
) -> None:
    """
    Worker process.

    args... describe what the arguments are
    """
    # =============================================================================================
    #                          ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
    # =============================================================================================

    # Instantiate logger
    worker_name = pathlib.Path(__file__).stem
    process_id = os.getpid()
    result, local_logger = logger.Logger.create(f"{worker_name}_{process_id}", True)
    if not result:
        print("ERROR: Worker failed to create logger")
        return

    # Get Pylance to stop complaining
    assert local_logger is not None

    local_logger.info("Logger initialized", True)

    # =============================================================================================
    #                          ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
    # =============================================================================================
    # Instantiate class object (heartbeat_receiver.HeartbeatReceiver)
    res, receiver = heartbeat_receiver.HeartbeatReceiver.create(
        connection=connection, 
        local_logger=local_logger, 
        args=None
    )

    if (res == True):
        local_logger.info("Heartbeat receiver connected")
    
    while (controller.is_exit_requested() == False):
        controller.check_pause()

        res = receiver.run(
            type=type, 
            condition=condition, 
            blocking=blocking, 
            timeout=blocking_timeout, 
            disconnection_threshold=disconnect_threshold, 
            args=None
        )

        output_queue_manager.queue.put(res)

        if (queue_timeout > 0):
            output_queue_manager.drain_queue(timeout=queue_timeout)


# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
