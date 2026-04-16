import logging

from .ai_log_service import AILogService


class AILogger:
    @staticmethod
    def log_request(
        task_type: str, input_data_keys: list, user_id=None, ip_address=None
    ):
        AILogService.log_generation_start(
            task_type,
            None,
            {
                "input_data_keys": input_data_keys,
                "user_id": user_id,
                "ip_address": ip_address,
            },
        )

    @staticmethod
    def log_response(
        task_type: str, success: bool, output_length: int, warnings=None, error=None
    ):
        if success:
            AILogService.log_generation_end(
                task_type,
                {
                    "provider": None,
                    "model": None,
                    "finish_reason": None,
                    "output_length": output_length,
                    "warnings": warnings or [],
                },
            )
        else:
            AILogService.log_generation_error(task_type, error or Exception("AI error"))

    @staticmethod
    def log_guard_violation(guard: str, details: str):
        logging.getLogger("apps.ai").warning(
            "AI Guard Violation", extra={"guard": guard, "details": details}
        )


__all__ = ["AILogService", "AILogger"]
