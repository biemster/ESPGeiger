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

listen_s = list()
client_s = list()
port_ws = 5000

def send_CPM(msg):
    for cl in client_s: cl.send(msg)

def setup_conn(port, accept_handler):
    global listen_s
    ls = socket.socket()
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_s.append(ls)

    ai = socket.getaddrinfo("0.0.0.0", port)
    addr = ai[0][4]

    ls.bind(addr)
    ls.listen(5)
    if accept_handler:
        ls.setsockopt(socket.SOL_SOCKET, 20, accept_handler)

def accept_html(listen_sock):
    global port_ws
    cl, remote_addr = listen_sock.accept()
    cl.recv(4096) # recv request
    cl.send(CONTENT % (network.WLAN(network.STA_IF).ifconfig()[0], port_ws))
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

    for ls in listen_s: ls.close()
    for cl in client_s: cl.close()

def start():
    global port_ws
    # Start webserver, on connect start WebSocket
    setup_conn(80, accept_html)
    
    # Start WebSocket
    setup_conn(port_ws, accept_ws)
