from src.websocket_server import WSServer
import os

if __name__ == '__main__':
    # preparing
    os.system('lsof -i:6633 | tail -1 | awk \'{print $2}\' | xargs kill -9')
    os.system('lsof -i:56565 | tail -1 | awk \'{print $2}\' | xargs kill -9')

    s = WSServer()
    s.start()