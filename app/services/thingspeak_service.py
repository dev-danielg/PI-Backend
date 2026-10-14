from thingspeak import Channel
import os


class ThingSpeakService:
    
    def __init__(self) -> None:
        self.channel = Channel(id=os.getenv("CHANNEL_ID"))
    
    
    def get_campo(self, campo):
        return self.channel.get_field(field=campo)

    