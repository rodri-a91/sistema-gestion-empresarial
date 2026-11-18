import json

from facturacion.application.casos_uso import emitir_factura
from facturacion.application.puertos import NotificadorFactura, RepositorioFacturas
from facturacion.domain.impuestos import CalculadorImpuesto
from facturacion.infrastructure.conversion import convertir_factura
from facturacion.infrastructure.presentacion import presentar_emision


def emitir_desde_json(
    texto: str,
    calculador: CalculadorImpuesto,
    repositorio: RepositorioFacturas,
    notificador: NotificadorFactura | None = None,
) -> str:
    datos = json.loads(texto)
    factura = convertir_factura(datos)
    resultado = emitir_factura(factura, calculador, repositorio, notificador)
    return presentar_emision(resultado)
