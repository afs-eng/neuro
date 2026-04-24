from __future__ import annotations

import json
import re

from apps.ai.services.text_generation_service import TextGenerationService
from .section_context_service import SectionContextService


class ClinicalConsistencyAuditService:
    PROMPT_NAME = "reports/consistency_audit_prompt.txt"

    @classmethod
    def audit_report(cls, report, context: dict) -> dict:
        payload = cls._build_audit_payload(report, context)
        result = cls._call_ai(payload)
        normalized = cls._normalize_audit_result(result.get("content") or "")
        normalized["metadata"] = {
            "provider": result.get("provider"),
            "model": result.get("model"),
            "finish_reason": result.get("finish_reason"),
            "usage": result.get("usage") or {},
            "warnings": result.get("warnings") or [],
            "prompt_name": cls.PROMPT_NAME,
        }
        normalized["status"] = "flagged" if normalized["alerts"] else "ok"
        return normalized

    @classmethod
    def _build_audit_payload(cls, report, context: dict) -> dict:
        return SectionContextService.build_for_audit(report, context)

    @classmethod
    def _call_ai(cls, payload: dict) -> dict:
        return TextGenerationService.generate_from_prompt(
            prompt_name=cls.PROMPT_NAME,
            user_prompt=(
                "Audite a coerencia do laudo com base apenas nos dados abaixo. "
                "Retorne somente JSON valido.\n\n"
                f"{json.dumps(payload, ensure_ascii=False, indent=2)}"
            ),
            timeout=1200,
            temperature=0.1,
            max_tokens=1400,
        )

    @classmethod
    def _normalize_audit_result(cls, content: str) -> dict:
        payload = cls._parse_json(content)
        alerts = payload.get("alerts") or []
        normalized_alerts = []
        for item in alerts:
            if not isinstance(item, dict):
                continue
            severity = str(item.get("severity") or "medium").lower()
            if severity not in {"high", "medium", "low"}:
                severity = "medium"
            normalized_alerts.append(
                {
                    "severity": severity,
                    "section_key": str(item.get("section_key") or "geral"),
                    "issue": str(item.get("issue") or "").strip(),
                    "suggestion": str(item.get("suggestion") or "").strip(),
                }
            )
        return {"alerts": [item for item in normalized_alerts if item["issue"]]}

    @staticmethod
    def _parse_json(content: str) -> dict:
        text = str(content or "").strip()
        if not text:
            return {"alerts": []}
        try:
            payload = json.loads(text)
            return payload if isinstance(payload, dict) else {"alerts": []}
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                return {
                    "alerts": [
                        {
                            "severity": "medium",
                            "section_key": "geral",
                            "issue": "A auditoria retornou um formato inválido e precisa de revisão manual.",
                            "suggestion": "Executar novamente a auditoria ou revisar o laudo manualmente.",
                        }
                    ]
                }
            try:
                payload = json.loads(match.group(0))
                return payload if isinstance(payload, dict) else {"alerts": []}
            except json.JSONDecodeError:
                return {
                    "alerts": [
                        {
                            "severity": "medium",
                            "section_key": "geral",
                            "issue": "A auditoria retornou um JSON inválido e precisa de revisão manual.",
                            "suggestion": "Executar novamente a auditoria ou revisar o laudo manualmente.",
                        }
                    ]
                }
