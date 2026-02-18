from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: Archivo no encontrado</h1>"
    
contenido = {
    '/': leer_archivo('home.html'),
    '/proyecto/1': "<html><h1>Proyecto 1: App de Libros</h1><p>Detalles de la Web Estática.</p></html>",
    '/proyecto/2': "<html><h1>Proyecto 2: MeFalta</h1><p>Tu guía de series y películas.</p></html>",
    '/proyecto/3': "<html><h1>Proyecto 3: Foto22</h1><p>Gestión inteligente de fotos.</p></html>",
            }
class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def ruta(self):
        return self.url().path

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        path_solicitado = self.ruta()

        # Buscamos la ruta en nuestro diccionario
        if path_solicitado in contenido:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            # Enviamos el contenido correspondiente
            html = contenido[path_solicitado]
            self.wfile.write(html.encode("utf-8"))
        else:
            # Si no existe la ruta (ej. alguien escribe /hola)
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Pagina no encontrada</h1>")


        if self.valida_autor():
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_html(self.url().path, self.query_data()).encode("utf-8"))
        else:
            self.send_error(404, 'El autor no existe')
            
    def valida_autor(self):
        if 'autor' in self.query_data():
            return True
        else:
            return False

    def get_html(self, path, qs):
        return f"""
        <h1>Proyecto: {path} Autor: {qs['autor']}<h1>
        """


    def get_response(self):
        return f"""
    <h1> Hola Web </h1>
    <p> URL Parse Result : {self.url()}         </p>
    <p> Path Original: {self.path}         </p>
    <p> Headers: {self.headers}      </p>
    <p> Query: {self.query_data()}   </p>
    
"""


if __name__ == "__main__":
    print("Starting server")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
