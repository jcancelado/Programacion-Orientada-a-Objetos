class VentanaBase:
    def mostrar(self):
        raise NotImplementedError
class VentanaPrincipal(VentanaBase):
    def mostrar(self):
        print("Mostrnado valores")()