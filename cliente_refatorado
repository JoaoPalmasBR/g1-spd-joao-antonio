import socket
import threading
import curses
import time

def receive_messages(client_socket, chat_win, lock):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                with lock:
                    chat_win.addstr(f"{message}\n")
                    chat_win.scrollok(True)
                    chat_win.refresh()
        except:
            break

def chat_interface(stdscr, client_socket):
    curses.curs_set(1)
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    chat_win = curses.newwin(height - 3, width, 0, 0)
    input_win = curses.newwin(3, width, height - 3, 0)

    input_win.addstr(0, 0, "Digite sua mensagem (digite 'sair' para encerrar):")
    input_win.refresh()

    lock = threading.Lock()

    recv_thread = threading.Thread(target=receive_messages, args=(client_socket, chat_win, lock))
    recv_thread.daemon = True
    recv_thread.start()

    while True:
        input_win.move(1, 0)
        input_win.clrtoeol()
        curses.echo()
        msg = input_win.getstr(1, 0).decode()
        curses.noecho()

        if msg.lower() == 'sair':
            client_socket.send(msg.encode())
            break
        else:
            client_socket.send(msg.encode())

    client_socket.close()

def start_client(server_host='172.29.28.32', server_port=12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((server_host, server_port))
    except ConnectionRefusedError:
        print("Erro: O servidor não está disponível.")
        return

    # Login: Usuário
    server_msg = client.recv(1024).decode()
    print(server_msg, end='')
    usuario = input()
    client.send(usuario.encode())

    # Login: Senha
    server_msg = client.recv(1024).decode()
    print(server_msg, end='')
    senha = input()
    client.send(senha.encode())

    # Resposta do servidor após autenticação
    resposta = client.recv(1024).decode()
    print(resposta)
    if "❌" in resposta:
        client.close()
        return

    # Após login bem-sucedido, abrir interface
    print("abrindo interface")
    time.sleep(1)
    curses.wrapper(chat_interface, client)

if __name__ == "__main__":
    start_client()
