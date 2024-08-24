import subprocess
from socketserver import BaseRequestHandler, TCPServer
exec_and_args = ['python3', '/Users/rahulkannans/hello.py']
port = 12345
process = None
status_states = {0: 'running', 1: 'stopped'}

class ProcessDaemon(BaseRequestHandler):    
    def start(self):
        global process, exec_and_args
        if self.checkStatus() == status_states[1] :
            process = subprocess.Popen(exec_and_args)
            return 0 
        else:
            return -1
    
    def stop(self):
        global process
        if self.checkStatus() == status_states[0]:
            process.terminate()
            process = None
            return 0  
        else:
            return -1
    
    def checkStatus(self):
        global process
        if process is not None:
            if process.poll() is None:
                return status_states[0]
            else:
                return status_states[1]
        else:
            return status_states[1]
    
    def handle(self):
        data =self.request.recv(1024).strip()
        if data == b'start':
            if self.start() == 0:
                self.request.sendall(b'process started')
            else:
                self.request.sendall(b'process already running')
        elif data == b'stop':
            if self.stop() == 0:
                self.request.sendall(b'process stopped')
            else:
                self.request.sendall(b'process not running already') 
        elif data == b'status':
            status = self.checkStatus()
            self.request.sendall(str(status).encode())
        elif data == b'restart':
            self.stop()
            self.start()
            self.request.sendall(b'process restarted')
        else:
            self.request.sendall(b'unknown command')


if __name__ == '__main__':
    with TCPServer(('localhost', port), ProcessDaemon) as server:
        server.serve_forever()