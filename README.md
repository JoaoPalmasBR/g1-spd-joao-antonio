
# Sistem de  Leilões distribuiods (Containerizado)
Sistema distribuído de leilões:
- em tempo real 
- utilizando: **sockets TCP**, **threads**, **multiprocessamento**
- uma interface interativa em **terminal** com `curses`.

## Integrantes
- João Antonio
- Emmanuel Peralta

## Funcionalidades

- Vários participantes simultâneos
- Autenticação de usuários com usuario e senha (predefinidos)
- Interface em modo texto (terminal) com atualização de mensagens em tempo real
- Registro de histórico completo dos leilões (`historico_leiloes.txt`)
- Validação de lances (nao deixa ser menor que um anterior)
- Notificações em tempo real de novos lances e vencedor


## Requisitos

- Python
- `windows-curses` (apenas no Windows)

## Instalação

### No Linux/macOS:
O módulo `curses` já vem instalado.

### No Windows:

1. Instale o módulo compatível com `curses`:

```bash
pip install windows-curses
```


## Servidor

Em um terminal
```bash
    python servidor.py
```

## Cliente

Em outro terminal, inicie o cliente
```bash
    python cliente_refatorado.py
```

## Autenticacao

Ao abrir o cliente, será solicitado:

- Usuário: 
    - joao
    - peralta
    - fabio

- Senha:
    - 1234

Os usuários estão definidos no servidor (USUARIOS no servidor_leilao.py)

## Comandos
    item <nome>     |	Inicia um leilão
    ----------------------------------------------------
    lance <valor>   |	Realiza um lance (valor inteiro)
    ----------------------------------------------------
    encerrar        |	Encerra o leilão atual. 
                    |    registra no log
                    |   anuncia o vencedor
    ----------------------------------------------------
    sair	        |   Sai da plataforma

O resultado do leilão é registrado automaticamente em historico_leiloes.txt.


docker-compose up servidor --build

docker-compose run --rm cliente
