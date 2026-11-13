class ExportadorTexto:
    def renderizar(self, numero: str) -> str:
        return f"Factura {numero}"

def publicar(numero: str) -> str:
    exportador = ExportadorTexto()
    return "PUBLICADO: " + exportador.renderizar(numero)

if __name__ == "__main__":
    print(publicar("F-001"))
