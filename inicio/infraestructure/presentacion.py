from inicio.aplication.resultado import ResultadoEmision


def presentar_emision(resultado: ResultadoEmision) -> str:
    return f"Emitida {resultado.numero}: {resultado.total:.2f} EUR"



