import http.server  
import ssl  
import socket  

class IPv6HTTPServer(http.server.HTTPServer):  
    address_family = socket.AF_INET6  

httpd = IPv6HTTPServer(('::', 4443), http.server.SimpleHTTPRequestHandler)  

# Wrap the server with SSL  
httpd.socket = ssl.wrap_socket(httpd.socket,  
                                certfile='/mnt/disk1/unraid/ssl/cert.pem',  
                                keyfile='/mnt/disk1/unraid/ssl/key.pem',  
                                server_side=True,
			        ssl_version=ssl.PROTOCOL_TLSv1_2)  

print("Serving on https://[::]:4443")  
httpd.serve_forever()  



