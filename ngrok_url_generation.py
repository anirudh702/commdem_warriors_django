
from pyngrok import ngrok

# Setting an auth token allows us to open multiple
# tunnels at the same time
ngrok.set_auth_token("2GV01CquWMr9nwEldUElziy1Ag8_3zH1AcPkfotG7iRC3oW7T")

# <NgrokTunnel: "http://<public_sub1>.ngrok.io" -> "http://localhost:80">
# ngrok_tunnel1 = ngrok.connect()
# <NgrokTunnel: "http://<public_sub2>.ngrok.io" -> "http://localhost:8000">
ngrok_tunnel2 = ngrok.connect(8000)
print(f"ngrok_tunnel2 {ngrok_tunnel2}")
