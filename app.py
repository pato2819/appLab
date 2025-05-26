import socket
import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_server_ip():
    """Obtiene la IP pública del servidor"""
    try:
        # Usamos un servicio externo para obtener la IP pública
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json().get('ip', 'Desconocida')
    except:
        try:
            # Fallback: obtenemos la IP local
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return 'Desconocida'

def get_server_region():
    """Intenta determinar la región del servidor usando la IP"""
    ip = get_server_ip()
    if ip == 'Desconocida':
        return 'Desconocida'
    
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        data = response.json()
        return data.get('region', 'Desconocida')
    except:
        return 'Desconocida'

@app.route('/server-info', methods=['GET'])
def server_info():
    """Endpoint que devuelve la información del servidor"""
    return jsonify({
        'ip': get_server_ip(),
        'region': get_server_region(),
        'hostname': socket.gethostname()
    })

@app.route('/', methods=['GET'])
def home():
    """Página de inicio con información básica"""
    return """
    <h1>Información del Servidor</h1>
    <p>IP: {}</p>
    <p>Región: {}</p>
    <p>Hostname: {}</p>
    <p><a href="/server-info">Ver datos en JSON</a></p>
    """.format(get_server_ip(), get_server_region(), socket.gethostname())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)