import urllib.parse, http.server, socketserver, re, webbrowser, socket, os, json
from pathlib import Path

def env():
    if not os.path.exists('env'):
        os.system('virtualenv env')
    os.system('env/bin/activate')

try:
    f = open('server/config.json')
except:
    print('\nā File di configurazione non trovato ā\n')
SERVER = json.load(f)
pattern = re.compile('.png|.jpg|.jpeg|.js|.css|.ico|.gif|.svg', re.IGNORECASE)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        request_file_path = Path(url_parts.path.strip("/"))

        ext = request_file_path.suffix
        if not request_file_path.is_file() and not pattern.match(ext):
            self.path = SERVER['SERVE']

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def checkValidity():
    for filename in os.listdir('routes'):
        if filename.split('.')[-1] != 'html':
            print('\nā Estensione del file: "' + filename + '" non corretta ā\n')
            exit()


env()
os.system('cls' if os.name == 'nt' else 'clear')
checkValidity()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
public_ip = s.getsockname()[0]
if SERVER['NETWORK']:
    try:
        import qrcode
    except:
        os.system('python3 -m pip install qrcode')
    try:
        from PIL import Image
    except:
        os.system('python3 -m pip install Pillow')
    img = qrcode.make('http://'+public_ip+':'+SERVER['PORT'])
    img.save('qrcode.png')
os.system('cls' if os.name == 'nt' else 'clear')
try:
    httpd = socketserver.TCPServer((SERVER['HOST'], int(SERVER['PORT'])), Handler)
    print('\n')
    print('š Application launched! š\n\n')
    print('\tš  Local\t-> http://{}:{}'.format(SERVER['HOST'], SERVER['PORT']))
    if SERVER['NETWORK']:
        print('\tš Network\t-> http://'+public_ip+':'+SERVER['PORT'])
    print('\n\nvvvvvv LOGS vvvvvv\n')
    if SERVER['NETWORK']:
        with Image.open('qrcode.png') as qr:
            qr.show()
    webbrowser.open_new('http://{}:{}'.format(SERVER['HOST'], SERVER['PORT']))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
except Exception as e:
    print('\nā '+str(e)+' ā\n')



