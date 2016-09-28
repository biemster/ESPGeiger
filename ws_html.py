import usocket as socket
import uos
import network
import websocket
import websocket_helper

CONTENT = b"""\
HTTP/1.0 200 OK

<!DOCTYPE HTML>
<html>
  <head> 
    <title>ESPGeiger CPM</title>
  </head>
  <body>
    <label id="CPM"></label>
    <script type="text/javascript">
      if ("WebSocket" in window)
      {
        var ws = new WebSocket("ws://%s:%d/");
        
        ws.onmessage = function (evt) 
        {
          var CPM_label = document.getElementById("CPM");
            CPM_label.innerHTML = evt.data;
        };
      }
      else
      {
        // The browser doesn't support WebSocket
        alert("WebSocket NOT supported by your Browser!");
      }
    </script>
  </body>
</html>
"""

listen_s = None
client_s = list()

def send_CPM(msg):
    for cl in client_s: cl.send(msg)

def setup_conn(port, accept_handler):
    global listen_s
    listen_s = socket.socket()
    listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ai = socket.getaddrinfo("0.0.0.0", port)
    addr = ai[0][4]

    listen_s.bind(addr)
    listen_s.listen(1)
    if accept_handler:
        listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)

def accept_html(listen_sock):
    cl, remote_addr = listen_sock.accept()
    cl.recv(4096) # recv request
    
    for i in (network.AP_IF, network.STA_IF):
        iface = network.WLAN(i)
        if iface.active():
            # Start WebSocket
            port_ws = 5000
            setup_conn(port_ws, accept_ws)
            cl.send(CONTENT % (iface.ifconfig()[0], port_ws))
            cl.close()

def accept_ws(listen_sock):
    global client_s
    cl, remote_addr = listen_sock.accept()
    client_s.append(cl)

    websocket_helper.server_handshake(cl)
    ws = websocket.websocket(cl, True)
    cl.setblocking(False)
    cl.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)
    uos.dupterm(ws)

def stop():
    global listen_s, client_s
    uos.dupterm(None)

    if listen_s: listen_s.close()
    for cl in client_s: cl.close()

def start():
    # Start webserver, on connect start WebSocket
    setup_conn(80, accept_html)
