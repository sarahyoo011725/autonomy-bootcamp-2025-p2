"""
Telemtry worker that gathers GPS data.
"""

import os
import pathlib

from pymavlink import mavutil

from utilities.workers import queue_proxy_wrapper
from utilities.workers import worker_controller
from . import telemetry
from ..common.modules.logger import logger


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
def telemetry_worker(
    controller: worker_controller.WorkerController,
    connection: mavutil.mavfile,
    timeout: float,
    output_queue_wrap: queue_proxy_wrapper.QueueProxyWrapper,
    args,  
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
    # Instantiate class object (telemetry.Telemetry)
    res, telementry = telemetry.Telemetry.create(connection=connection, args=None, local_logger=local_logger)

    if (res == False or telementry == None) :
        local_logger.error("Failed to create Telementry")
        return

    # Main loop: do work.
    while (controller.is_exit_requested() == False):
        controller.check_pause()
        data = telementry.run(timeout=timeout, args=None)
        if (data != None):
            output_queue_wrap.queue.put(data)

# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
