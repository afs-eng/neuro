# Segurança - NeuroAvalia

## Visão Geral

Este documento estabelece as políticas, práticas e mecanismos de segurança do sistema NeuroAvalia. A segurança é uma preocupação fundamental em sistemas que lidam com dados de saúde sensíveis, e o NeuroAvalia foi desenhado com múltiplas camadas de proteção para garantir a confidencialidade, integridade e disponibilidade das informações dos pacientes.

O sistema segue princípios de segurança em camadas (defense in depth), onde cada camada oferece proteção adicional mesmo que a camada anterior seja comprometida. Além disso, o sistema segue o princípio do menor privilégio (least privilege), garantindo que cada componente e usuário tenha apenas as permissões estritamente necessárias paraperforming suas funções.

A segurança no NeuroAvalia não é uma reflexão tardia - ela é integrada desde a concepção do sistema, desde a arquitetura de banco de dados até a interface do usuário. Cada decisão de desenvolvimento considera implicações de segurança, e o código passa por revisões de segurança antes de ser incorporado ao projeto principal.

## Autenticação

### Sistema de Tokens JWT

O sistema utiliza JSON Web Tokens (JWT) para autenticação de usuários, oferecendo stateless authentication que escala horizontalmente sem necessidade de sessões server-side. O JWT contém as informações necessárias para identificar o usuário em cada requisição, eliminando a necessidade de consultas ao banco de dados para validar sessões.

#### Estrutura do Token

O token JWT é composto por três partes codificadas em Base64URL:

- **Header**: Algoritmo de assinatura (HS256) e tipo de token
- **Payload**: Identificador do usuário, roles, expiração
- **Signature**: Assinatura HMAC do header e payload

```python
payload = {
    "user_id": 123,
    "email": "psicologo@clinica.com",
    "roles": ["psychologist"],
    "exp": 1699999999,  # Unix timestamp
    "iat": 1699900000   # Issued at
}
```

#### Refresh Tokens

O sistema utiliza refresh tokens para estender sessões sem necessidade de novo login:

- Refresh token é armazenado no banco de dados
- Tempo de expiração: 30 dias (configurável)
- Invalidação explícita no logout
- Rotação de refresh token a cada uso

```
1. Usuário faz login com credentials
2. Servidor gera access_token (24h) e refresh_token (30d)
3. Access token expira após 24h
4. Cliente usa refresh_token para obter novo access_token
5. Refresh token é invalidado e novo é gerado (rotação)
6. Processo repete até expiração do refresh token
```

#### Configurações de Segurança

```python
# Configurações de JWT
JWT_EXPIRATION_HOURS = 24
REFRESH_TOKEN_EXPIRATION_DAYS = 30
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = env("JWT_SECRET_KEY")  # Diferente da SECRET_KEY do Django
```

### Validação de Credenciais

O sistema implementa validações robustas de credenciais:

- **Senha mínima**: 8 caracteres, letras + números
- **Hash**: bcrypt com salt único por usuário
- **Tentativas**: Bloqueio após 5 tentativas falhas (30 min)
- **MFA**: Preparado para autenticação multifator futura

## Autorização

### Modelo de Papéis

O sistema utiliza modelo de Role-Based Access Control (RBAC) com papéis hierárquicos:

| Papel | Descrição | Hierarquia |
|-------|-----------|------------|
| admin | Administrador do sistema | Mais alto |
| psychologist | Psicólogo responsável | Clínico |
| assistant | Assistente administrativo | Leitura |
| readonly | Visualização apenas | Mais baixo |

### Matriz de Permissões

#### Pacientes

| Operação | admin | psychologist | assistant | readonly |
|----------|-------|--------------|-----------|----------|
| Criar | ✓ | ✓ | ✗ | ✗ |
| Ler | ✓ | Próprios | Próprios | ✗ |
| Atualizar | ✓ | Próprios | ✗ | ✗ |
| Deletar | ✓ | ✗ | ✗ | ✗ |
| Exportar | ✓ | ✓ | ✗ | ✗ |

#### Avaliações

| Operação | admin | psychologist | assistant | readonly |
|----------|-------|--------------|-----------|----------|
| Criar | ✓ | ✓ | ✗ | ✗ |
| Ler | ✓ | Próprias | Próprias | ✗ |
| Atualizar | ✓ | ✗ | ✗ | ✗ |
| Deletar | ✓ | ✗ | ✗ | ✗ |

#### Testes

| Operação | admin | psychologist | assistant | readonly |
|----------|-------|--------------|-----------|----------|
| Aplicar | ✓ | ✓ | ✗ | ✗ |
| Validar | ✓ | ✓ | ✗ | ✗ |
| Recalcular | ✓ | ✓ | ✗ | ✗ |
| Ler | ✓ | Próprias | Próprias | ✗ |

#### Laudos

| Operação | admin | psychologist | assistant | readonly |
|----------|-------|--------------|-----------|----------|
| Criar | ✓ | ✓ | ✗ | ✗ |
| Revisar | ✓ | ✓ | ✗ | ✗ |
| Assinar | ✓ | ✓ | ✗ | ✗ |
| Ler | ✓ | Próprios | ✗ | ✗ |
| Exportar | ✓ | ✓ | ✗ | ✗ |

### Implementação de Permissões

As permissões são implementadas em múltiplas camadas:

```python
# Camada 1: Decorator na view
@require_permissions(["test:validate"])
def validate_test(request, application_id):
    # ...

# Camada 2: Service check
def validate_test_service(user, application):
    if not user.has_permission("test:validate"):
        raise PermissionDenied()
    # ...

# Camada 3: Queryset filter
def get_applications_queryset(user):
    if user.role == "psychologist":
        return TestApplication.objects.filter(evaluation__psychologist=user)
    return TestApplication.objects.none()
```

## Menor Princípio de Privilégio

O sistema segue rigorosamente o princípio do menor privilégio:

### Para Usuários

- Cada usuário tem acesso apenas aos dados necessários para suas funções
- Acessos são granted temporariamente quando necessário
- Revisão periódica de acessos concedidos

### Para Componentes

- Backend tem acesso apenas ao banco de dados
- Frontend não tem acesso direto ao banco
- Camada de IA tem acesso apenas a dados já processados
- Serviços externos precisam de credenciais explícitas

### Para APIs

- Endpoints expõem apenas informações necessárias
- Dados sensíveis nunca são expostos em responses sem necessidade
- Rate limiting previne abuso

## Proteção de Dados Sensíveis

### Dados Classificados como Sensíveis

O sistema classifica os seguintes dados como sensíveis, requerendo proteção adicional:

- **Identificação**: CPF, RG, endereço completo
- **Contato**: Telefone pessoal, email pessoal
- **Clínicos**: Diagnósticos, históricos médicos, resultados de testes
- **Financeiros**: Informações de pagamento (se aplicável)
- **Autenticação**: Credenciais, tokens, chaves de API

### Medidas de Proteção

#### Em Trânsito

- TLS 1.3 para todas as comunicações
- HSTS habilitado paraforçar HTTPS
- Certificate pinning para apps móveis (futuro)
- Não há fallback para HTTP em produção

#### Em Repouso

- senhas hasheadas com bcrypt
- Dados sensíveis criptografados com AES-256 (quando aplicável)
-备份 criptografados
- Chaves de criptografia em vault separado

#### Em Interface

- Máscaramento de dados sensíveis (CPF, telefone)
- Exibição apenas mediante justificativa
- Não há logging de dados sensíveis

### Criptografia de Dados

O sistema utiliza múltiplas camadas de criptografia:

```python
# Modelo conceitual
class Patient(models.Model):
    # Dados não criptografados (buscáveis)
    name = models.CharField()
    email = models.EmailField()
    
    # Dados criptografados (sensíveis)
    cpf_encrypted = EncryptedCharField()
    rg_encrypted = EncryptedCharField()
    address_encrypted = EncryptedTextField()
    
    # Dados sensíveis em JSON
    medical_history_encrypted = EncryptedJSONField()
```

## Segurança da API

### Rate Limiting

Endpoints sensíveis possuem rate limiting:

| Endpoint | Limite | Janela |
|----------|--------|--------|
| /api/auth/login | 5 | 15 min |
| /api/patients/ | 100 | 1 min |
| /api/ai/generate | 10 | 1 min |
| /api/tests/*/calculate | 20 | 1 min |

### Validação de Entrada

Toda entrada de API é validada:

- Schemas Pydantic para validação estrutural
- Sanitização para prevenir XSS
- Limites de tamanho para prevenir DoS
- Type coercion para garantir tipos corretos

```python
# Exemplo de validação
class PatientSchema(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    cpf: str = Field(pattern=r"^\d{11}$")
    email: Optional[EmailStr] = None
    
    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v):
        if not valida_cpf(v):
            raise ValueError("CPF inválido")
        return v
```

### Headers de Segurança

O sistema configura headers de segurança:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; script-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

### CORS

Configuração restritiva de CORS:

```python
CORS_ALLOWED_ORIGINS = [
    "https://app.neuroavalia.com.br",
    "https://admin.neuroavalia.com.br",
]
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["Content-Length", "X-Requested-With"]
```

## Segurança de Arquivos

### Upload de Arquivos

Arquivos são tratados como dados sensíveis:

- **Tipos permitidos**: PDF, JPG, PNG (configurável)
- **Tamanho máximo**: 10MB por arquivo
- **Escaneamento**: Verificação de malware (futuro)
- **Armazenamento**: Em storage separado (S3/local)
- **Acesso**: Via signed URLs temporárias

### Assinatura Digital

Laudos utilizam assinatura digital:

- Certificado digital do profissional
- Timestamp confiável
- hash do conteúdo
- Validação de integridade

## Segurança da Camada de IA

A camada de IA possui guardrails específicos que excedem as medidas de segurança gerais.

### AIGuard - Validações Específicas

```python
class AIGuard:
    @validate_no_clinical_decision(output)
    @validate_data_safety(data)
    @check_output_length(output, max_chars=10000)
    @sanitize_output(output)
```

### Restrições Específicas para IA

- **Sem acesso direto ao banco**: IA só recebe dados processados
- **Sem capacidade de escrita**: IA apenas sugere, não persiste
- **Sem decisões clínicas**: Linguagem bloqueada para diagnóstico/tratamento
- **Logging completo**: Toda interação é logada
- **Revisão obrigatória**: Output sempre passa por revisão humana

### Provedores de IA

O sistema suporta múltiplos provedores com configuração de segurança:

- **OpenAI**: API keys com permisos mínimos
- **Anthropic**: Modo sandbox quando disponível
- **Local**: Para processamento offline (futuro)

## Auditoria

### Sistema de AuditLog

Todas as ações críticas são registradas:

```python
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    action = models.CharField(choices=ACTION_CHOICES)
    resource_type = models.CharField()  # patient, evaluation, test, report
    resource_id = models.CharField()
    changes = models.JSONField()  # Dados alterados
    ip_address = models.GenericIPField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField()  # Dados adicionais
```

### Ações Auditadas

| Ação | Detalhes |
|------|----------|
| create | Criação de qualquer entidade |
| update | Alteração de dados (inclui diff) |
| delete | Exclusão lógica ou física |
| view | Acesso a dados sensíveis |
| export | Exportação de dados |
| print | Impressão de laudos |
| login | Autenticação bem-sucedida |
| logout | Logout |
| validate | Validação de teste |
| sign | Assinatura de laudo |

### Retenção de Logs

- Logs de auditoria: 7 anos (conforme legislação de saúde)
- Logs de aplicação: 90 dias
- Logs de segurança (falhas): 1 ano

## Backup e Recuperação

### Estratégia de Backup

- **Frequência**: Diário incremental, semanal completo
- **Retenção**: 30 dias de backups diários
- **Localização**: Armazenamento geograficamente separado
- **Teste**: Restore testado mensalmente

### Plano de Recuperação

```
RTO (Recovery Time Objective): 4 horas
RPO (Recovery Point Objective): 1 dia

1. Detecção de falha
2. Avaliação de impacto
3. Decisão de recuperar vs reconstruir
4. Execução de backup
5. Verificação de integridade
6. Comunicação com stakeholders
7. Return to normal operations
```

## Segurança Docker e Produção

### Imagens Docker

- **Base**: Imagem oficial Python (slim)
- **Usuário**: Não-root execution
- **Secrets**: Não embedded em imagens
- **Scan**: Vulnerability scanning automatizado

### Variáveis de Ambiente

Variáveis sensíveis nunca são commitadas:

```bash
# .env.example (NÃO commitado)
DATABASE_URL=postgres://user:***@host/db
SECRET_KEY=***
JWT_SECRET_KEY=***
OPENAI_API_KEY=***
```

### Configuração de Produção

```yaml
# docker-compose.prod.yml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  backend:
    restart: unless-stopped
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
    secrets:
      - db_password
      - secret_key
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/var/www/static
    depends_on:
      - backend
```

### Hardening de Produção

- Firewall configurado (apenas portas necessárias)
- Logs centralizados
- Monitoramento de segurança
- Alertas de anomalias
- Update automatizado de segurança

## Responsabilidade do Backend como Autoridade de Segurança

O backend Django é a autoridade final para todas as decisões de segurança do sistema. Esta designação implica responsabilidades específicas:

### Validação Centralizada

Toda validação de segurança ocorre no backend:

- Autenticação de usuários
- Verificação de permissões
- Validação de dados de entrada
- Verificação de integridade
- Criptografia e descriptografia

O frontend nunca deve realizar validações de segurança por conta própria - todas as decisões são tomadas pelo backend e comunicadas ao cliente.

### Princípio de Defesa em Profundidade

O backend implementa múltiplas camadas de defesa:

```
Requisição
    │
    ▼
1. Rate Limiting (nginx)
    │
    ▼
2. CORS Validation
    │
    ▼
3. Authentication (JWT)
    │
    ▼
4. Authorization (permissions)
    │
    ▼
5. Input Validation (Pydantic)
    │
    ▼
6. Business Logic Validation
    │
    ▼
7. Database (constraints)
    │
    ▼
Response
```

### Atualizações de Segurança

O projeto mantém dependências atualizadas:

- Review semanal de security advisories
- Atualização de patches de segurança em até 72h
- Scanning automatizado de vulnerabilidades
- Dependency review antes de cada release

## Referências

- Visão Geral: `SKILLS.md`
- Regras de Negócio: `SKILLS_REGRAS_NEGOCIO.md`
- Inteligência Artificial: `SKILLS_IA.md`
- Arquitetura: `PROJECT_ARCHITECTURE.md`
