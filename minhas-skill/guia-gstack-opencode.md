# Guia de uso do gstack no OpenCode

Este guia mostra, passo a passo, como instalar e usar o **gstack** no **OpenCode**, com foco em um fluxo simples e prático para desenvolvimento.

## Objetivo

Usar os skills do gstack dentro do OpenCode para apoiar revisão de código, planejamento, QA e organização do desenvolvimento.

## 1. Instale o OpenCode

Você pode instalar pelo script oficial:

```bash
curl -fsSL https://opencode.ai/install | bash
```

Ou pelo npm:

```bash
npm i -g opencode-ai@latest
```

Depois, confirme se o comando está funcionando:

```bash
opencode --version
```

## 2. Deixe o OpenCode funcional

Antes de instalar o gstack, verifique se o OpenCode já está abrindo normalmente e se o modelo/provedor que você pretende usar já está configurado.

## 3. Baixe o repositório do gstack

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack
```

## 4. Rode o setup para OpenCode

```bash
./setup --host opencode
```

Esse comando prepara a versão compatível com o OpenCode e instala os skills no diretório esperado pelo host.

## 5. Verifique se os skills foram instalados

Os skills devem ficar em uma pasta semelhante a esta:

```bash
~/.config/opencode/skills/
```

Para verificar:

```bash
ls ~/.config/opencode/skills
```

Se quiser filtrar pelo gstack:

```bash
ls ~/.config/opencode/skills | grep gstack
```

## 6. Reinicie o OpenCode

Se o OpenCode já estava aberto antes da instalação, feche e abra novamente para garantir que ele reconheça os skills instalados.

## 7. Abra seu projeto

Entre na pasta do seu projeto e inicie o OpenCode:

```bash
cd /caminho/do/seu/projeto
opencode
```

## 8. Como usar os skills

No OpenCode, o gstack funciona como **skill**, e não como slash command nativo.

Por isso, a melhor forma de uso é pedir de maneira explícita dentro da conversa.

Exemplos:

```text
Faça uma revisão deste código usando o skill do gstack.
```

```text
Use o gstack para revisar esta arquitetura antes de eu implementar.
```

```text
Use o skill do gstack para fazer QA deste fluxo.
```

```text
Analise este endpoint e proponha melhorias de estrutura usando o gstack.
```

## 9. Como usar no seu sistema neuro

No seu sistema neuropsicológico, o gstack pode ajudar principalmente em:

- revisão de código do backend Django
- revisão de componentes e fluxos no Next.js
- planejamento de novas features
- padronização de módulos de testes
- QA do fluxo de avaliação, testes e geração de laudo
- revisão de prompts e estrutura de geração por IA
- análise de arquitetura antes de refatorações

## 10. Onde ele ajuda mais

### Muito útil para

- revisar endpoints
- revisar serializers, schemas e serviços
- pensar estrutura de testes como WISC-IV, BPA-2, RAVLT, FDT e SRS-2
- checar consistência entre frontend, backend e geração de laudo
- melhorar organização de código
- reduzir retrabalho em refatorações

### Usar com cuidado para

- regras psicométricas
- cálculo de percentis
- classificação clínica
- interpretação automática de resultados
- hipótese diagnóstica

Nesses pontos, a validação final deve continuar com você.

## 11. Se o skill não funcionar de primeira

Confira estes pontos:

### O OpenCode está instalado?

```bash
opencode --version
```

### A pasta de skills existe?

```bash
ls ~/.config/opencode/skills
```

### O setup foi executado com o host correto?

```bash
./setup --host opencode
```

### O OpenCode foi reiniciado?

Se ele já estava aberto, feche e abra novamente.

### Você pediu de forma explícita?

No OpenCode, vale a pena dizer claramente que quer usar o skill do gstack.

## 12. Sugestão de uso prático no dia a dia

Para o seu fluxo, uma forma boa de usar seria:

### Antes de implementar uma feature

```text
Use o gstack para revisar a arquitetura desta feature antes de eu codar.
```

### Depois de implementar

```text
Use o gstack para revisar este código e apontar riscos de manutenção.
```

### Antes de mexer em geração de laudo

```text
Use o gstack para analisar este fluxo de geração de laudo e sugerir melhorias.
```

### Antes de refatorar módulos grandes

```text
Use o gstack para avaliar esta refatoração e identificar pontos de quebra.
```

## 13. Conclusão

O gstack pode ser um bom apoio dentro do OpenCode para melhorar a qualidade do desenvolvimento do seu sistema neuro.

Ele tende a ajudar mais na parte de:

- engenharia de software
- revisão de arquitetura
- revisão de código
- QA de fluxo
- organização do projeto

Já a parte clínica, psicométrica e interpretativa deve continuar sob sua validação direta.
