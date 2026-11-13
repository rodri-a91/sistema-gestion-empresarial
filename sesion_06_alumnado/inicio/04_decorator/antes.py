class Emisor:
    def emitir(self, numero: str) -> str:
        print(f"INICIO {numero}")
        resultado = f"Emitida {numero}"
        print(f"FIN {numero}")
        return resultado

if __name__ == "__main__":
    print(Emisor().emitir("F-001"))
