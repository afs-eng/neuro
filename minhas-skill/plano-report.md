Plano
Fase 1
Objetivo: centralizar a definição das seções sem mudar o fluxo.
Arquivos:
1. apps/reports/services/section_registry.py
2. ajustes mínimos em apps/reports/services/report_ai_service.py
3. ajustes mínimos em apps/reports/services/report_generation_service.py
Implementação:
1. criar um registro único por section_key
2. mover para esse registro:
label, supports_ai, prompt_name, codes, kind, timeout
3. deixar ReportAIService ler do registry em vez de manter mapas separados
4. deixar ReportGenerationService._enabled_sections_config() usar o mesmo registry para decidir presença de testes
Ganho:
1. remove duplicação
2. facilita adicionar nova seção
3. reduz inconsistência entre IA e geração completa
Risco:
1. baixo
Verificação:
1. listar laudos
2. gerar laudo completo
3. regenerar fdt, bpa2, funcoes_executivas
4. confirmar que títulos, seções e prompts continuam corretos
Fase 2
Objetivo: extrair a montagem do contexto por seção.
Arquivos:
1. apps/reports/services/section_context_service.py
2. reduzir lógica em apps/reports/services/report_ai_service.py
Implementação:
1. mover _build_section_context
2. mover _build_test_payload
3. mover regras específicas do WISC
4. deixar ReportAIService só orquestrar:
validar -> montar contexto -> chamar IA -> normalizar resposta
Ganho:
1. separa responsabilidade
2. facilita inspeção do payload enviado para a IA
3. prepara terreno para validação declarativa
Risco:
1. médio, porque mexe em payload enviado para IA
Verificação:
1. comparar contexto antigo e novo para fdt
2. regenerar seção com IA
3. validar que generation_metadata e warnings permanecem corretos
Fase 3
Objetivo: formalizar validação mínima por seção.
Arquivos:
1. apps/reports/services/section_validation_service.py
2. ou evolução de apps/ai/guards/data_presence_guard.py
3. pequenos ajustes em section_registry.py
Implementação:
1. cada seção passa a declarar requisitos mínimos
2. exemplos:
   - fdt exige teste fdt
   - ravlt exige ravlt
   - funcoes_executivas exige ao menos fdt ou wisc4
3. a validação retorna mensagens consistentes
4. warnings e erros passam a ser mais previsíveis
Ganho:
1. menos prompt vazio
2. mensagens melhores
3. menos fallback “misterioso”
Risco:
1. baixo a médio
Verificação:
1. testar seção com dados completos
2. testar seção sem instrumento necessário
3. confirmar erro/warning claro no frontend
Fase 4
Objetivo: padronizar prompts e saída.
Arquivos:
1. apps/ai/prompts/reports/*.txt
2. opcionalmente helpers pequenos no registry
Implementação:
1. definir um template editorial comum para prompts
2. padronizar:
   - objetivo clínico
   - limites do contexto
   - tom técnico
   - proibição de inventar dados
   - instrução de saída limpa
3. revisar prompts mais críticos primeiro:
   - fdt
   - bpa2
   - ravlt
   - funcoes_executivas
   - conclusao
Ganho:
1. mais consistência clínica
2. menos variação de estilo
3. menor chance de resposta fora do formato
Risco:
1. médio, porque muda qualidade textual percebida
Verificação:
1. regenerar seções antes/depois
2. comparar consistência, objetividade e aderência clínica
Fase 5
Objetivo: melhorar observabilidade e contratos leves.
Arquivos:
1. section_registry.py
2. report_section_service.py
3. frontend do laudo
Implementação:
1. incluir no metadata campos mais claros:
   - used_fallback
   - prompt_name
   - section_kind
2. mostrar melhor no frontend:
   - motivo do fallback
   - modelo efetivamente usado
   - seção suportada por IA ou não
3. manter contrato de saída padronizado internamente, sem criar camada pesada demais
Ganho:
1. auditoria melhor
2. diagnóstico mais rápido
3. suporte operacional mais simples
Risco:
1. baixo
Verificação:
1. regenerar seção por IA
2. regenerar com fallback
3. checar UI e payload da API
Fase 6
Objetivo: só se necessário, criar fallback especializado por seção.
Arquivos:
1. apps/reports/fallbacks/*.py ou algo equivalente
Implementação:
1. começar apenas por seções onde o fallback genérico é fraco
2. exemplos possíveis:
   - fdt
   - conclusao
   - funcoes_executivas
Ganho:
1. fallback mais útil quando a IA falhar
Risco:
1. médio/alto de manutenção
Verificação:
1. simular falha de IA
2. comparar qualidade do fallback atual vs especializado
Ordem recomendada
1. Fase 1
2. Fase 2
3. Fase 3
4. Fase 4
5. Fase 5
6. Fase 6 só se houver necessidade real
Minha recomendação prática
Se eu fosse executar agora, faria só estas 3 primeiras primeiro:
1. section_registry.py
2. section_context_service.py
3. validação mínima por seção
Isso já entrega quase todo o ganho estrutural com risco controlado.
Se quiser, no próximo passo eu posso começar a implementar a Fase 1 diretamente.