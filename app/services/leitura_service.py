


class LeituraService:
    
    def __init__(self, service) -> None:
        self.service = service
        
        
    def get_temperatura(self):
        return self.service.get_campo("Temperatura")
        
        
    def get_umidade(self):
        return self.service.get_campo("Umidade")
        
        
        
    