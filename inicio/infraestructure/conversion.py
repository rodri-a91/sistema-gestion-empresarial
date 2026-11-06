from inicio.dominio import Factura


def convertir_factura(datos: dict) -> Factura:
    if datos is dict:
        raise ValueError("No es un diccionario")
