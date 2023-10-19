import http.server
import socketserver
import requests

USERNAME = "lcjazmin_" # Username para API Geonames
API_KEY = "4e02f39241345f4554632c35141a9e85" # APIKEY para API OpenWeather
port = 9090 # Puerto en el que se establecera el servidor

# Función para obtener datos de ubicación
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
        
# Función para obtener datos meteorológicos
def obtener_datos_meteorologicos(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "main" in data and "weather" in data:
            temperatura = data["main"]["temp"] - 273.15  # Convertir de Kelvin a Celsius
            condiciones_climaticas = data["weather"][0]["description"]
            return f"Temperatura: {temperatura:.2f}°C<br>Condiciones Climáticas: {condiciones_climaticas}"
        else:
            return "Datos meteorológicos no disponibles."
    except Exception as e:
        return f"Error: {str(e)}"
    
# Clase personalizada para manejar las solicitudes
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location','/APIWeatherGeonamesWeb.html')
            self.end_headers()
        elif self.path == '/ApiWeatherGeonamesWeb.html':
            lugar = self.path[9:]
            ciudad = obtener_informacion_ubicacion(lugar)
            resultado = obtener_datos_meteorologicos(ciudad)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(resultado.encode())
        else:
            super().do_GET()

# Configuración del servidor
with socketserver.TCPServer(("", port), MyHandler) as httpd:
    print(f"Servidor web en el puerto {port} para OpenWeather-Geonames")
    httpd.serve_forever()