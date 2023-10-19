import http.server
import socketserver
import requests

USERNAME = "lcjazmin_"
port = 9089

def obtener_informacion_ubicacion(lugar):
    url = f"http://api.geonames.org/searchJSON?name={lugar}&maxRows=1&username={USERNAME}"

    try:
        response = requests.get(url)
        data = response.json()
        if "geonames" in data and data["geonames"]:
            ubicacion = data["geonames"][0]
            print(f"Nombre: {ubicacion['name']}")
            print(f"País: {ubicacion['countryName']}")
            print(f"Población: {ubicacion['population']}")
            return f"Nombre: {ubicacion['name']}<br>País: {ubicacion['countryName']}<br>Población: {ubicacion['population']}"
        else:
            return "Ubicación no encontrada."
    except Exception as e:
        print(f"Error: {str(e)}")

# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location','/APIGeonamesWeb.html')
            self.end_headers()
        elif self.path == '/ApiGeonamesWeb.html':
            ubicacion = self.path[9:]
            print(ubicacion)
            resultado = obtener_informacion_ubicacion(ubicacion)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(resultado.encode())
        else:
            super().do_GET()

# Configuración del servidor
with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"Servidor web en el puerto {port} para Geonames")
    httpd.serve_forever()