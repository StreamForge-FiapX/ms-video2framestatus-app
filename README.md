![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=POSTECH-SOAT-SALA11_application-avalanches-producao-ms&metric=alert_status)
![Bugs](https://sonarcloud.io/api/project_badges/measure?project=POSTECH-SOAT-SALA11_application-avalanches-producao-ms&metric=bugs)
![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=POSTECH-SOAT-SALA11_application-avalanches-pagamento-ms&metric=code_smells)
![Coverage](https://sonarcloud.io/api/project_badges/measure?project=POSTECH-SOAT-SALA11_application-avalanches-producao-ms&metric=coverage)
# **Documentação do Microserviço de Consulta de Histórico e Geração de URLs: ms-video2framestatus-app**  
Este documento descreve o funcionamento do microserviço responsável por fornecer, a partir de requisições do frontend, o histórico de solicitações de um usuário e os status delas. Para solicitações com status "concluído", o microserviço também permite que o frontend solicite uma URL auto-assinada para download do objeto armazenado no bucket S3.

---

### **Visão Geral do Sistema**  
O sistema fornece uma interface para que os usuários visualizem o histórico de solicitações de processamento de vídeos e seus respectivos status. Ele acessa informações armazenadas em um banco de dados Redis e, em caso de solicitações "concluídas", permite a geração de URLs auto-assinadas para download do resultado diretamente do S3.

---

### **Objetivo do Microserviço**  
O microserviço é responsável por:  

1. **Consultar o Histórico do Usuário**:  
   Recuperar informações sobre solicitações feitas por um usuário, como:  
   - Nome do vídeo  
   - Data e hora da solicitação  
   - Status (em andamento, falha, concluído, etc.)  

2. **Gerar URLs Auto-assinadas**:  
   Para solicitações com status "concluído", gerar uma URL auto-assinada que permita o download do objeto diretamente do bucket S3.  

3. **Atender Requisições do Frontend**:  
   Expor endpoints que permitem ao frontend:  
   - Listar o histórico de solicitações por usuário.  
   - Solicitar URLs auto-assinadas para objetos concluídos.  

---

### **Fluxo de Funcionamento**  

#### **Consulta de Histórico**  
1. O frontend envia uma requisição para consultar o histórico de solicitações de um usuário.  
2. O microserviço consulta o banco Redis utilizando o identificador do usuário.  
3. O Redis retorna uma lista contendo:  
   - Nome do vídeo  
   - Data e hora da solicitação  
   - Status da solicitação  
   - (Opcional) Caminho do objeto no S3 para solicitações "concluídas".  

4. O microserviço devolve os dados estruturados ao frontend.  

#### **Geração de URL Auto-assinada**  
1. O frontend envia uma requisição para solicitar uma URL de download de um objeto associado a uma solicitação "concluída".  
2. O microserviço consulta o Redis para recuperar o caminho do objeto no S3.  
3. Com base no caminho, o microserviço utiliza as APIs do S3 para gerar uma URL auto-assinada.  
4. A URL é retornada ao frontend para que o usuário possa fazer o download.  

---

### **Integrações e Dependências**  

1. **Banco Redis (AWS Elasticache)**  
   - Armazena informações sobre as solicitações e seus status.  
   - Contém o caminho do objeto no S3 para solicitações "concluídas".  

2. **Amazon S3**  
   - Armazena os objetos gerados a partir do processamento de vídeos.  
   - Permite a geração de URLs auto-assinadas para download.  

3. **Frontend**  
   - Consome os endpoints do microserviço para exibir o histórico de solicitações e realizar downloads.  

---

### **Tecnologias e Ferramentas Utilizadas**  
- **Linguagem**: Python, Node.js ou .NET Core  
- **Banco de Dados**: Redis (AWS Elasticache)  
- **Armazenamento**: Amazon S3  
- **Orquestração**: Kubernetes (AWS EKS, opcional)  

---

### **Regras de Negócio e Pontos Críticos**  

1. **Validação do Usuário**  
   Garantir que apenas usuários autenticados e autorizados possam acessar suas solicitações.  

2. **Consultas ao Redis**  
   As operações de leitura devem ser otimizadas para garantir baixa latência, especialmente em cenários com grande volume de dados.  

3. **URLs Temporárias**  
   As URLs auto-assinadas devem ter validade configurável (ex.: 15 minutos).  

4. **Segurança**  
   As informações armazenadas no Redis devem ser protegidas com criptografia. As URLs geradas devem ser acessíveis apenas pelos usuários que fizeram a requisição.  

5. **Gerenciamento de Erros**  
   Implementar tratamento robusto para cenários de falha no Redis ou na geração de URLs no S3.  

---

### **Estrutura do Projeto**  

#### **Estrutura de Diretórios**  
```plaintext
ms-video2framestatus-app/
├── Dockerfile
├── README.md
├── requirements.txt
├── src
│   ├── domain
│   │   ├── repositories.py
│   │   └── use_cases.py
│   ├── infrastructure
│   │   ├── redis_repository.py
│   │   └── s3_event_parser.py
│   └── main.py
└── tests
    ├── test_lambda_handler.py
    ├── test_redis_repository.py
    ├── test_repositories.py
    ├── test_s3_event_parser.py
    └── test_use_cases.py
```

---

### **Detalhamento do Fluxo de Trabalho**  

1. **Consulta de Histórico**:  
   - O caso de uso `GetUserHistoryUseCase` consulta o Redis para buscar o histórico de solicitações do usuário.  
   - Os dados são estruturados e enviados ao frontend.  

2. **Geração de URL Auto-assinada**:  
   - O caso de uso `GenerateSignedUrlUseCase` utiliza o caminho do objeto no Redis para gerar a URL auto-assinada via S3.  

3. **Manuseio de Erros**:  
   - `SignedUrlException` é acionada em caso de falhas na geração da URL.  
   - Logs são registrados para auditoria e depuração.  
