from django.conf import settings

from apps.ai.logging.ai_log_service import AILogService
from apps.ai.schemas import GenerationRequest, GenerationResponse

from .provider_factory import ProviderFactory
from .prompt_registry_service import PromptRegistryService


class TextGenerationService:
    @classmethod
    def generate_from_prompt(cls, prompt_name: str, user_prompt: str, **kwargs) -> dict:
        request = GenerationRequest(
            prompt_name=prompt_name,
            user_prompt=user_prompt,
            provider=kwargs.get("provider") or settings.AI_PROVIDER,
            model=kwargs.get("model"),
            temperature=kwargs.get("temperature", 0.2),
            timeout=kwargs.get("timeout", 180),
            max_tokens=kwargs.get("max_tokens", 2048),
            metadata={
                k: v
                for k, v in kwargs.items()
                if k
                not in {"provider", "model", "temperature", "timeout", "max_tokens"}
            },
        )
        AILogService.log_generation_start(
            request.prompt_name,
            request.provider,
            {"timeout": request.timeout, "model": request.model},
        )
        provider = ProviderFactory.create(request.provider)
        system_prompt = PromptRegistryService.read("base_system_prompt.txt")
        section_prompt = PromptRegistryService.read(prompt_name)
        full_user_prompt = f"{section_prompt}\n\n{user_prompt}".strip()
        try:
            result = provider.generate(
                system_prompt=system_prompt,
                user_prompt=full_user_prompt,
                model=request.model,
                temperature=request.temperature,
                timeout=request.timeout,
                max_tokens=request.max_tokens,
                **request.metadata,
            )
        except ValueError:
            raise
        except Exception as exc:
            AILogService.log_generation_error(prompt_name, exc)
            raise ValueError(f"Falha ao gerar texto com IA: {exc}") from exc
        normalized = GenerationResponse.from_dict(result).as_dict()
        AILogService.log_generation_end(prompt_name, normalized)
        return normalized
