# Regras de Negócio - NeuroAvalia

## Visão Geral

Este documento define as regras de negócio do sistema NeuroAvalia, estabelecendo os princípios fundamentais que governam a operação do sistema, a estrutura de dados, os fluxos clínicos e as restrições que garantem a integridade e segurança das informações de avaliação neuropsicológica.

O sistema NeuroAvalia foi concebido para suportar todo o ciclo de vida de uma avaliação neuropsicológica, desde o cadastro inicial de um paciente até a emissão final de um laudo clínico. Cada componente do sistema foi desenhado para manter a integridade dos dados clínicos, garantir rastreabilidade completa das avaliações e separar claramente as responsabilidades entre o backend (lógica de negócio) e o frontend (apresentação).

A arquitetura de negócio fundamenta-se no princípio de que o profissional de neuropsicologia permanece como autoridade final sobre todas as decisões clínicas. O sistema existe para organizar, calcular, armazenar e apresentar informações de forma estruturada, mas nunca para substituir o julgamento profissional.

## Entidade Central: Paciente

O paciente é a entidade central do sistema, serving como raiz de toda a hierarquia de dados clínicos. Todas as demais entidades - avaliações, aplicações de testes, documentos e laudos - estão direta ou indiretamente vinculadas a um paciente.

### Identificação do Paciente

Cada paciente possui identificadores únicos no sistema:

- **id**: Identificador interno único (UUID ou inteiro)
- **cpf**: CPF válido como identificador oficial (campo único)
- **nome completo**: Nome civil completo para documentos oficiais

Informações pessoais adicionais incluem data de nascimento, gênero, escolaridade, profissão e contato. Estas informações são necessárias para correta aplicação das tabelas normativas, que variam conforme idade e nível educacional.

### Dados Clínicos do Paciente

O sistema armazena informações clínicas sensíveis relacionadas ao paciente:

- **Histórico médico**: Condições prévias, medicamentos, internações
- **Histórico neurológico**: Traumatismos cranioencefáuticos, convulsões,neurocirurgias
- **Histórico desenvolvimental**: marcos do desenvolvimento, dificuldades de aprendizagem
- **Queixas principais**: Motivo da busca por avaliação

Estas informações são protegidas por medidas adicionais de segurança e acesso restrito a profissionais autorizados.

### Vinculação com Avaliações

Um paciente pode possuir múltiplas avaliações ao longo do tempo, representando momentos distintos de investigação neuropsicológica. O sistema mantém histórico completo de todas as avaliações, permitindo análise evolutiva do paciente.

## Unidade Clínica: Avaliação

A avaliação neuropsicológica é a unidade clínica principal do sistema, representando uma sessão completa de investigação. A avaliação vincula o paciente a um conjunto de instrumentos aplicados, documentos coletados e laudo emitido.

### Estrutura da Avaliação

```
Avaliação
├── Paciente (obrigatório)
├── Avaliador responsável (obrigatório)
├── Data de início
├── Data de conclusão (opcional)
├── Status (emandamento/concluída/arquivada)
├── Motivo da avaliação
├── Hipótese diagnóstica
├── Aplicações de Teste (nenhum ou muitos)
├── Documentos (nenhum ou muitos)
└── Laudo (opcional, único)
```

### Ciclo de Vida da Avaliação

Uma avaliação passa por estágios definidos:

1. **Criação**: Avaliação inicial criada, vinculada a paciente
2. **Em Andamento**: Aplicações de testes sendo realizadas
3. **Conclusão**: Todos os testes aplicados e validados
4. **Laudo Emitido**: Laudo gerado e revisado
5. **Arquivada**: Avaliação finalizada e arquivada

O sistema impede progressão inadequada - um laudo só pode ser gerado quando todas as aplicações de teste estão validadas.

## Vínculo entre Entidades

O sistema mantém vínculos claros e rastreáveis entre todas as entidades:

### Hierarquia Principal

```
Paciente
    └── Avaliação
            ├── Aplicação de Teste 1
            │       └── Instrumento (WISC-IV)
            ├── Aplicação de Teste 2
            │       └── Instrumento (BPA-2)
            ├── Documento (laudo anterior)
            ├── Documento (imagem cerebral)
            └── Laudo
                    └── Versão 1
                    └── Versão 2 (revisão)
```

### Regras de Vínculo

- Toda aplicação de teste deve pertencer a uma avaliação
- Toda avaliação deve pertencer a um paciente
- Um paciente pode ter múltiplas avaliações
- Uma avaliação pode ter múltiplas aplicações de teste
- Uma avaliação pode ter múltiplos documentos
- Uma avaliação pode ter no máximo um laudo
- Um laudo pode ter múltiplas versões (versionamento)

## Regra de Testes Vinculados à Avaliação

A aplicação de instrumentos psicológicos segue regras específicas:

### Aplicação de Instrumento

1. Selecionar instrumento do catálogo (Instrument)
2. Criar aplicação vinculada à avaliação (TestApplication)
3. Preencher dados brutos (raw_payload)
4. Executar processamento (scoring_service)
5. Revisar resultados pelo profissional
6. Marcar como validado (is_validated = true)

### Validação de Instrumento

Cada instrumento define requisitos específicos:

- **Faixa etária**: Idade mínima e máxima do paciente
- **Requisitos de escolaridade**: Anos de estudo necessários
- **Tempo de aplicação**: Duração estimada
- **Materiais necessários**: Kit física necessário

O sistema valida automaticamente estes requisitos antes de permitir a aplicação.

### Recálculo de Testes

O sistema permite recálculo de aplicações de teste quando necessário:

- Alteração de dados brutos pelo avaliador
- Identificação de erro no processamento
- Atualização de tabelas normativas

O recálculo preserva histórico, permitindo auditoria completa.

## Separação entre raw_payload, computed_payload e Interpretação

Esta é a regra de separação de dados mais importante do sistema.

### raw_payload - Dados Brutos

O campo `raw_payload` armazena os dados exatamente como digitados pelo avaliador, sem qualquer processamento:

```python
class TestApplication(models.Model):
    raw_payload = models.JSONField(
        "dados brutos",
        default=dict,
        blank=True
    )
```

Características:

- Entrada原始 do frontend
- Não modificado pelo sistema
- auditável para verificação de entrada
- Pode conter erros de digitação
- Não deve ser usado para decisões clínicas

Exemplo (WISC-IV):
```json
{
    "code": "informacoes",
    "valor": 15,
    "tempo": 45,
    "erros": 2
}
```

### computed_payload - Resultados Calculados

O campo `computed_payload` armazena os resultados do processamento pelo backend:

```python
class TestApplication(models.Model):
    computed_payload = models.JSONField(
        "dados calculados",
        default=dict,
        blank=True
    )
```

Características:

- Gerado exclusivamente pelo backend
- Contém escores, percentis, pontos ponderados
- Aplicação de tabelas normativas
- Determinístico e auditável
- Base para decisões clínicas

Exemplo (WISC-IV):
```json
{
    "escore_padrao": 12,
    "percentil": 75,
    "classificacao": "alto médio",
    "intervalo_confianca_95": [10, 14],
    "subteste": "Informações",
    "codigo": "inf"
}
```

### classified_payload - Classificação Clínica

O campo `classified_payload` contém a classificação clínica baseada nos valores computados:

```python
class TestApplication(models.Model):
    classified_payload = models.JSONField(
        "dados classificados",
        default=dict,
        blank=True
    )
```

Características:

- Classificação conforme padrões internacionais
- Níveis de funcionamento cognitivo
- Identificação de pontos fortes e fracos
- Comparação com esperado para a faixa

### interpretation_text - Interpretação

O campo `interpretation_text` contém a interpretação textual gerada:

```python
class TestApplication(models.Model):
    interpretation_text = models.TextField(
        "interpretação",
        blank=True
    )
```

Características:

- Texto narrativo explicando resultados
- Pode ser gerado por interpreters dos instrumentos
- Pode ser assistido por IA
- Sempre sujeito à revisão profissional

### Fluxo de Processamento

```
1. raw_input (Frontend)
        │
        ▼
2. API recebe raw_payload
        │
        ▼
3. InstrumentModule.validate()
        │ Erros? → Retorna para correção
        ▼
4. InstrumentModule.compute()
        │ Gera computed_payload
        ▼
5. InstrumentModule.classify()
        │ Gera classified_payload
        ▼
6. InstrumentModule.interpret()
        │ Gera interpretation_text
        ▼
7. Salva todos os payloads
        │
        ▼
8. Retorna para frontend
```

## Laudo como Saída Revisada

O laudo é o documento final da avaliação neuropsicológica, representando a síntese profissional de todos os dados coletados.

### Estrutura do Laudo

```
Laudo
├── Avaliação (obrigatório)
├── Avaliador responsável (obrigatório)
├── Data de emissão
├── Versão
├── Status (rascunho/revisão final)
├── Conteúdo estruturado
│   ├── Identificação
│   ├── Queixa principal
│   ├── Histórico
│   ├── Exame mental
│   ├── Resultados por instrumento
│   ├── Síntese clínica
│   └── Conclusões
├── Assinatura digital
└── Histórico de revisões
```

### Regras de Emissão

- Todas as aplicações de teste devem estar validadas
- Laudo deve ter um avaliador responsável
- Conteúdo deve passar por revisão antes de finalização
- Assinatura digital garante autenticidade

### Versionamento de Laudos

O sistema mantém histórico completo de versões:

- Cada alteração gera nova versão
- Versões anteriores são preservadas
- É possível comparar versões
- Rastreabilidade de alterações

## Versionamento e Rastreabilidade

O sistema implementa versionamento em múltiplas entidades:

### TestApplication

- **created_at**: Data de criação
- **updated_at**: Data de última atualização
- **is_validated**: Status de validação
- **validated_at**: Data de validação
- **validated_by**: Usuário que validou
- **recalculated_at**: Data do último recálculo

### Report (Laudo)

- Campo de versão numérico
- Histórico de alterações preservado
- Comparação entre versões disponível

### Auditoria

Todas as ações críticas são registradas em AuditLog:

- Criação de paciente
- Alteração de dados clínicos
- Aplicação de teste
- Validação de resultado
- Emissão de laudo
- Exportação de dados

## IA Apenas como Apoio Textual e Organizacional

A inteligência artificial no sistema serve exclusivamente como ferramenta de produtividade, nunca como autoridade clínica.

### Usos Permitidos de IA

A IA pode auxiliar nas seguintes tarefas:

- **Resumos**: Sintetizar informações de múltiplas fontes
- **Sugestões de estrutura**: Propor organização para laudos
- **Tradução**: Converter termos técnicos para linguagem acessível
- **Revisão**: Verificar consistência de texto
- **Extração**: Identificar padrões em dados não estruturados

### Usos Não Permitidos de IA

A IA não deve ser utilizada para:

- Cálculo de escores ou percentis
- Aplicação de tabelas normativas
- Classificação de resultados
- Emissão de diagnósticos
- Decisões de tratamento
- Substituição de julgamento profissional

### Fluxo de Uso de IA

```
1. Backend processa teste completamente
2. Dados calculados são salvos
3. Usuário solicita ajuda da IA
4. IA recebe dados estruturados (NÃO raw)
5. IA gera sugestão
6. Profissional revisa e aprova
7. Se aprovado, texto é incorporado
```

A IA nunca tem acesso a dados brutos diretamente, apenas a dados já processados e validados pelo backend.

## Restrições Adicionais

### Sobre Dados de Pacientes

- CPF deve ser válido e único no sistema
- Data de nascimento é obrigatória para cálculos normativos
- Escolaridade é obrigatória para instrumentos que exigem
- Informações sensíveis devem ser criptografadas

### Sobre Avaliações

- Uma avaliação só pode ter um laudo
- Laudo só pode ser gerado com testes validados
- Avaliador responsável deve estar logado para alterações
- Avaliação arquivada não pode ser alterada

### Sobre Testes

- Instrumento deve estar ativo para aplicação
- Paciente deve estar na faixa etária válida
- Aplicação validada não pode ter raw_payload alterado sem recálculo
- Recálculo deve preservar histórico

### Sobre Laudos

- Laudo rascunho pode ser alterado livremente
- Laudo final não pode ser alterado (criar nova versão)
- Assinatura digital é obrigatória para laudos finais
- Exportação de PDF deve ser registrada em auditoria

## Referências

- Visão Geral do Projeto: `SKILLS.md`
- Arquitetura: `PROJECT_ARCHITECTURE.md`
- Segurança: `SKILLS_SEGURANCA.md`
- Inteligência Artificial: `SKILLS_IA.md`
