# 💸 Plataforma de Leilões em Rede (Distribuído via Docker)

Sistema distribuído de leilões em tempo real utilizando **sockets TCP**, **threads**, **multiprocessamento** e **Docker**. Agora com suporte a **volume nomeado** para histórico, e **cópia manual** para pasta local.

---

## ✅ Funcionalidades

- Vários participantes simultâneos (via TCP)
- Autenticação de usuários com login e senha
- Interface interativa em terminal (curses)
- Histórico de leilões salvo em volume Docker
- Cópia manual do histórico para o PC local
- Comunicação entre containers por nome de serviço

---

## 📦 Requisitos

- Docker e Docker Compose instalados
- Python (apenas para desenvolvimento, não para execução Docker)
- Em Windows: instalar `windows-curses` se quiser rodar o cliente manualmente

---

## 🚀 Como executar

### 1. Subir apenas o servidor

```bash
docker-compose up servidor --build
```

### 2. Rodar o cliente (modo interativo)

```bash
docker-compose run --rm cliente
```
ou 

```bash
docker-compose up --build --scale cliente=5
```
```bash
docker exec -it g1-spd-joao-antonio-cliente-2 bash
```

- O cliente já abrirá pedindo **Usuário** e **Senha**.
- Exemplo de usuário: `joao`, senha: `1234`.

---

## 🔐 Comandos dentro do cliente

| Comando                | Descrição                                |
|-------------------------|-----------------------------------------|
| `item <nome>`           | Inicia leilão com o item especificado    |
| `lance <valor>`         | Realiza um lance no leilão               |
| `encerrar`              | Encerra o leilão atual                   |
| `sair`                  | Sai do sistema de leilões                |

---

## 📂 Como copiar o histórico dos leilões

O servidor salva os registros no volume nomeado `historico_data`.

Para copiar o histórico manualmente para sua máquina:

```bash
docker cp g1-spd-joao-antonio-servidor-1:/historico ./
```

- `g1-spd-joao-antonio-servidor-1` é o nome do container do servidor (veja com `docker ps`).
- O histórico será salvo na pasta `./historico/`.

---

## 🛠️ Estrutura de Pastas

```
/
├── servidor/              # Código do servidor
├── cliente/               # Código do cliente
├── historico/             # Pasta onde serão copiados os 
|                            históricos
├── docker-compose.yml     # Compose principal
├── README.md              # Este arquivo
```

---
## Inspiração

- https://hub.docker.com/_/python
- https://www.docker.com/blog/how-to-dockerize-your-python-applications/
---

## 🎯 Futuras Melhorias (opcionais)

- Implementar SSL/TLS para segurança
- Criar cliente Web via WebSocket
- Timeout automático de leilões
- Dashboard para histórico de leilões

---