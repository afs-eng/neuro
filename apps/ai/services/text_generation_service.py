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
        
        fallback_provider = getattr(settings, "AI_FALLBACK_PROVIDER", None)
        
        provider = ProviderFactory.create(request.provider)
        
        if provider is None:
            if fallback_provider:
                request.provider = fallback_provider
                provider = ProviderFactory.create(fallback_provider)
                if provider:
                    AILogService.log_generation_start(
                        request.prompt_name,
                        f"{request.provider} (fallback)",
                        {"timeout": request.timeout, "model": request.model},
                    )
        
        if provider is None:
            raise ValueError("IA desabilitada. Configure AI_PROVIDER=ollama ou openai.")
        
        system_prompt = PromptRegistryService.read("base_system_prompt.txt")
        section_prompt = PromptRegistryService.read(prompt_name)
        full_user_prompt = f"{section_prompt}\n\n{user_prompt}".strip()
        
        last_error = None
        providers_tried = [request.provider]
        
        while provider:
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
                normalized = GenerationResponse.from_dict(result).as_dict()
                AILogService.log_generation_end(prompt_name, normalized)
                return normalized
            except Exception as exc:
                last_error = exc
                AILogService.log_generation_error(prompt_name, exc)
                
                if fallback_provider and request.provider != fallback_provider:
                    AILogService.log_generation_start(
                        prompt_name,
                        f"{fallback_provider} (fallback)",
                        {"timeout": request.timeout, "model": request.model},
                    )
                    request.provider = fallback_provider
                    provider = ProviderFactory.create(fallback_provider)
                    providers_tried.append(fallback_provider)
                    fallback_provider = None
                    continue
                    
                break
        
        raise ValueError(f"Falha ao gerar texto com IA: {last_error}") from last_error
