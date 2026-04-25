# 🧪 TESTE DO WAIS-III COM PREVIEW EM TEMPO REAL

## 📋 Valores de Teste (Paciente 17 anos 11 meses)

| Subteste | Pontos Brutos | Esperado Ponderado |
|----------|---------------|-------------------|
| Completar Figuras | 18 | 11 |
| Vocabulário | 36 | 11 |
| Códigos | 59 | 10 |
| Semelhanças | 22 | 10 |
| Cubos | 22 | 7 |
| Aritmética | 8 | 8 |
| Raciocínio Matricial | 16 | 10 |
| Dígitos | 13 | 10 |
| Informação | 13 | 11 |
| Arranjo de Figuras | 17 | 12 |
| Compreensão | 27 | 14 |
| Procurar Símbolos | 26 | 9 |
| Seq. Números-Letras | 10 | 12 |

## 🎯 Resultados Esperados

### Somas Ponderadas
- **QI Verbal**: 64 (11+11+8+10+11+14)
- **QI Execução**: 50 (11+10+7+10+12)
- **QI Total**: 114 (64+50)
- **ICV**: 32 (11+10+11)
- **IOP**: 28 (11+7+10)
- **IMO**: 30 (8+10+12)
- **IVP**: 19 (10+9)

### Pontos Compostos
- **QI Verbal**: 104 (percentil 61)
- **QI Execução**: 100 (percentil 50)
- **QI Total**: 102 (percentil 55)
- **ICV**: 104 (percentil 61)
- **IOP**: 96 (percentil 39)
- **IMO**: 100 (percentil 50)
- **IVP**: 98 (percentil 45)

## 🚀 Como Testar

### 1. Abrir o Formulário
```
URL: http://localhost:3000/dashboard/tests/wais3?evaluation_id=5
```

### 2. Verificar que carrega corretamente
- ✅ 14 subtestes aparecem
- ✅ Organizados por cores (azul=execução, amarelo=verbal, verde=suplementar)
- ✅ Nenhuma tabela de preview ainda (não tem valores)

### 3. Testar Preview em Tempo Real
- Preencha **Vocabulário = 36**
- Imediatamente deve aparecer uma tabela com:
  - QI Verbal: soma=indefinido (apenas 1 de 6 subtestes)
  - Avisos sobre subtestes faltando

### 4. Preencher Todos os Valores
- Preencha todos os 13 subtestes com os valores da tabela acima
- A tabela deve atualizar dinamicamente
- Resultado final deve mostrar todos os 7 índices com seus valores

### 5. Testar Save
- Clique em "Salvar WAIS-III"
- Deve redirecionar para: `/dashboard/tests/wais3/[id]/result?evaluation_id=5`
- Deve mostrar os mesmos valores na página de resultado

## 🐛 Se Houver Problemas

1. **Preview não aparece**
   - Abra o Console (F12)
   - Veja se há erros ao digitar
   - Verifique se a chamada para `/api/tests/wais3/preview` está sendo feita

2. **Valores errados no preview**
   - Compare com a tabela de valores esperados acima
   - Se different, pode ser problema na normalização das tabelas

3. **Save não funciona**
   - Verifique a URL redirecionada
   - Abra o resultado novamente e compare valores

## ✅ Checklist Final

- [ ] Formulário carrega
- [ ] Preview aparece ao digitar
- [ ] Valores são calculados corretamente
- [ ] Todos os 7 índices aparecem
- [ ] Save redireciona corretamente
- [ ] Página de resultado mostra os dados
