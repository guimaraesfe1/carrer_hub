# ConnectUni

A ConnectUni é uma plataforma que tem como objetivo conectar alunos da UNIMAM a empresas parceiras que oferecem vagas de estágio, trainees e oportunidades de primeira experiência profissional.
O sistema centraliza o processo de candidatura, gestão de vagas e comunicação entre alunos, empresas e a instituição de ensino.

## Documentação

[Objetivo](#Objetivo)

[Funcionalidade](#Funcionalidade)

[Arquitetura do Sistema](#ArquiteturaDoSistema)

[Pré-Requisitos](#Pré-Requisitos)

[Instalação](#Instalação)

# 1. Objetivo

Facilitar o acesso dos estudantes a oportunidades de estágio.
Aumentar a eficiência da triagem e seleção por parte das empresas.
Disponibilizar à universidade ferramentas de acompanhamento e métricas de empregabilidade.

## 1.1  Como funciona

Os alunos criam seus perfis, as empresas publicam oportunidades, e o sistema faz o match entre competências e requisitos das vagas.
A universidade acompanha tudo por um painel administrativo.

 Alunos criam perfis → encontram vagas → se candidatam.

 Empresas cadastram oportunidades → analisam candidatos → contratam.

# 2. Funcionalidade
## 2.1 Para alunos

### 2.1.1 Cadastro e Login

Criação de conta com dados pessoais e acadêmicos

Autenticação por e-mail institucional

### 2.1.3 Busca e Exploração de Vagas

Filtros por área, modalidade, localização e carga horária

Visualização detalhada das ofertas

### 2.1.4 Candidatura

Aplicação com um clique

Envio automático do perfil para a empresa

Notificações de atualização

## 2.2 para Empresas
### 2.2.1 Registro Corporativo

Criação de conta empresarial

Cadastro de informações da empresa (CNPJ, setor, tamanho etc.)

### 2.2.2 Publicação de Vagas

Criação de vagas

Formulário completo de requisitos

Gestão de vagas ativas e encerradas



# 3. Arquitetura do Sistema

## 3.1 Modelos

A plataforma é construída seguindo os princípios RESTful, que é um padrão de arquitetura para APIs

### 3.1.1 Modelo Account

Representa um usuário no sistema, seja estudante ou empresa.
Armazena informações básicas como nome de usuário, email, senha e tipo de conta.

Permite criar novas contas com validação de dados únicos.
Garante que cada conta tenha um tipo definido (estudante ou empresa).
Registra automaticamente a data de criação da conta.

### 3.1.2 Modelo Company

Representa uma empresa no sistema.
Cada empresa está ligada a uma conta de usuário.
É possível criar uma nova empresa junto com a conta.

Também é possível atualizar as informações da empresa.
E, se necessário, a empresa e a conta associada podem ser excluídas.

### 3.1.3 Modelo Inscription

Representa a inscrição de um estudante em uma vaga de trabalho.
Permite registrar o motivo da inscrição e a data em que foi feita.

Garante que o mesmo estudante não se inscreva na mesma vaga mais de uma vez.
Permite criar, atualizar e excluir inscrições no sistema.
Mantém o vínculo entre o estudante e a vaga de forma clara e segura.

### 3.1.4 Modelo Job

Permite criar uma nova vaga de trabalho no sistema.

Recebe os dados da vaga e salva no banco de forma segura.
Depende de uma sessão ativa do banco de dados para funcionar.

### 3.1.5 Modelo Student

Permite criar uma nova conta de estudante no sistema.
Recebe os dados do usuário e cria a conta vinculada ao estudante.

Garante que o cadastro seja único e seguro.
Retorna uma mensagem de confirmação quando a conta é criada com sucesso.

# 4. Pré-Requisitos

Python 3.13

# 5. Instalação

Clone o projeto na sua maquina e entre a raiz do projeto
```bash
git clone git@github.com:guimaraesfe1/carrer_hub.git
cd carrer_hub
```

Instale as dependencias descritas no arquivo pyproject.toml utilizando seu gerenciador de pacotes. Nesse projeto foi utilizado o poetry
```bash
poetry install
```

Ative o ambiente virutal do projeto no linux
```bash
eval $(poetry env activate)
```
No windows
```pwsh
Invoke-Expression (poetry env activate --path)
```

para rodar o servidor de desenvolvimento
```bash
task dev
```