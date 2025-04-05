import socket
import multiprocessing
import datetime

MAX_CLIENTS = 10
MAX_MSG_LENGTH = 200  # limite de caracteres por mensagem

def log(message):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    print(f"{timestamp} {message}")

def broadcast(all_clients, message, exclude=None):
    for c in all_clients:
        if c != exclude:
            try:
                c.send(message.encode())
            except:
                continue

def process_request(client_socket, addr, all_clients, nicknames, lock, leilao):
    try:
        client_socket.send("Digite seu apelido: ".encode())
        nickname = client_socket.recv(1024).decode().strip()
        if not nickname:
            nickname = f"{addr[0]}:{addr[1]}"

        with lock:
            nicknames[client_socket.fileno()] = nickname

        log(f"{nickname} ({addr}) conectado.")
        client_socket.send("Conectado ao servidor de leilão.\nComandos: item <nome>, lance <valor>, encerrar, sair".encode())

        while True:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                break

            if len(message) > MAX_MSG_LENGTH:
                client_socket.send(f"⚠️ Sua mensagem ultrapassou {MAX_MSG_LENGTH} caracteres.".encode())
                continue

            if message.lower() == "sair":
                log(f"{nickname} desconectou.")
                break

            if message.startswith("item "):
                item = message[5:].strip()
                with lock:
                    leilao['item'] = item
                    leilao['lance'] = {'valor': 0, 'autor': None}
                    leilao['ativo'] = True
                log(f"Novo item cadastrado para leilão: {item}")
                broadcast(all_clients, f"🔨 Leilão iniciado para o item: {item}!", client_socket)
                continue

            if message.startswith("lance "):
                try:
                    valor = int(message[6:].strip())
                except ValueError:
                    client_socket.send("⚠️ Valor de lance inválido.".encode())
                    continue

                with lock:
                    if not leilao.get('ativo', False):
                        client_socket.send("⚠️ Nenhum leilão ativo.".encode())
                        continue

                    if valor <= leilao['lance']['valor']:
                        client_socket.send("⚠️ O lance deve ser maior que o atual.".encode())
                        continue

                    leilao['lance'] = {'valor': valor, 'autor': nickname}
                    log(f"Lance de R$ {valor} por {nickname}")
                    broadcast(all_clients, f"📣 Novo lance de {nickname}: R$ {valor}", client_socket)
                continue

            if message.lower() == "encerrar":
                with lock:
                    if not leilao.get('ativo', False):
                        client_socket.send("⚠️ Nenhum leilão em andamento.".encode())
                        continue
                    vencedor = leilao['lance']['autor']
                    valor = leilao['lance']['valor']
                    item = leilao['item']
                    leilao['ativo'] = False
                resultado = f"🏁 Leilão encerrado para '{item}'! Vencedor: {vencedor} com R$ {valor}" if vencedor else "❌ Leilão encerrado sem lances."
                log(resultado)
                broadcast(all_clients, resultado, None)
                continue

            # Mensagens normais
            log(f"{nickname}: {message}")
            broadcast(all_clients, f"{nickname}: {message}", client_socket)

    except Exception as e:
        log(f"Erro com {addr}: {e}")

    finally:
        with lock:
            if client_socket in all_clients:
                all_clients.remove(client_socket)
            nicknames.pop(client_socket.fileno(), None)
        client_socket.close()

def start_server(host='0.0.0.0', port=12345):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
    except OSError as e:
        if e.errno == 10048:  # Porta já está em uso no Windows
            log(f"❌ A porta {port} já está em uso. Tente usar outra porta ou finalize o processo que está ocupando ela.")
        else:
            log(f"Erro ao iniciar o servidor: {e}")
        return

    server.listen(5)
    log(f"Servidor ouvindo em {host}:{port}")

    manager = multiprocessing.Manager()
    all_clients = manager.list()
    nicknames = manager.dict()
    lock = manager.Lock()

    leilao = manager.dict()
    leilao['item'] = None
    leilao['lance'] = {'valor': 0, 'autor': None}
    leilao['ativo'] = False

    while True:
        client_socket, addr = server.accept()

        with lock:
            if len(all_clients) >= MAX_CLIENTS:
                log(f"Servidor cheio! Recusando {addr}")
                try:
                    client_socket.send("Servidor cheio. Tente novamente mais tarde.".encode())
                except:
                    pass
                client_socket.close()
                continue
            all_clients.append(client_socket)

        client_process = multiprocessing.Process(
            target=process_request,
            args=(client_socket, addr, all_clients, nicknames, lock, leilao)
        )
        client_process.daemon = True
        client_process.start()

if __name__ == "__main__":
    start_server()
