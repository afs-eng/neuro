import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger("ai")


class AILogger:
    @staticmethod
    def log_request(
        task_type: str,
        input_data_keys: list,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
    ):
        logger.info(
            f"AI Request - task: {task_type}, user: {user_id}, ip: {ip_address}, "
            f"data_keys: {input_data_keys}, timestamp: {datetime.utcnow().isoformat()}"
        )

    @staticmethod
    def log_response(
        task_type: str,
        success: bool,
        output_length: int,
        warnings: Optional[list] = None,
        error: Optional[str] = None,
    ):
        if success:
            logger.info(
                f"AI Response - task: {task_type}, output_length: {output_length}, "
                f"warnings: {warnings}, timestamp: {datetime.utcnow().isoformat()}"
            )
        else:
            logger.error(
                f"AI Error - task: {task_type}, error: {error}, "
                f"timestamp: {datetime.utcnow().isoformat()}"
            )

    @staticmethod
    def log_guard_violation(guard: str, details: str):
        logger.warning(
            f"AI Guard Violation - guard: {guard}, details: {details}, "
            f"timestamp: {datetime.utcnow().isoformat()}"
        )
