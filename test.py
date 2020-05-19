from pypresence import Presence
import time

client_id = "712088548278403123"
RPC = Presence(client_id)
RPC.connect()
RPC.update(large_image="icon", large_text="Bloons TD 6", details="In Menu")
