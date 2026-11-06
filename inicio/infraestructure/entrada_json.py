import json

from inicio.aplication.casos_uso import emitir_factura
from inicio.aplication.puertos import NotificadorFactura, RepositorioFacturas
from inicio.domain.impuestos import CalculadorImpuesto
from inicio.infraestructure.conversion import convertir_factura
from inicio.infraestructure.presentacion import presentar_emision


def emitir_desde_json(
    texto: str,
    calculador: CalculadorImpuesto,
    repositorio: RepositorioFacturas,
    notificador: NotificadorFactura | None,
) -> str:
    datos = json.loads(texto)
    factura = convertir_factura(datos)
    resultado = emitir_factura(factura, calculador, repositorio, notificador)

    return presentar_emision(resultado)
