import logging


logger = logging.getLogger("apps.ai")


class AILogService:
    @staticmethod
    def log_generation_start(prompt_name: str, provider: str | None, metadata: dict):
        logger.info(
            "AI generation started",
            extra={"prompt_name": prompt_name, "provider": provider, **metadata},
        )

    @staticmethod
    def log_generation_end(prompt_name: str, result: dict):
        logger.info(
            "AI generation completed",
            extra={
                "prompt_name": prompt_name,
                "provider": result.get("provider"),
                "model": result.get("model"),
                "finish_reason": result.get("finish_reason"),
            },
        )

    @staticmethod
    def log_generation_error(prompt_name: str, error: Exception):
        logger.exception(
            "AI generation failed",
            extra={"prompt_name": prompt_name, "error_type": type(error).__name__},
        )
