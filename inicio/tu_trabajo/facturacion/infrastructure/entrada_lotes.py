from facturacion.application.casos_uso import emitir_factura
from facturacion.application.puertos import NotificadorFactura, RepositorioFacturas
from facturacion.domain.impuestos import CalculadorImpuesto
from facturacion.infrastructure.conversion import convertir_factura
from facturacion.infrastructure.presentacion import presentar_emision


def emitir_lote(datos: list[dict], calculador: CalculadorImpuesto,
                repositorio: RepositorioFacturas,
                notificador: NotificadorFactura | None = None) -> list[str]:
    mensajes: list[str] = []
    for entrada in datos:
        factura = convertir_factura(entrada)
        resultado = emitir_factura(factura, calculador, repositorio, notificador)
        mensajes.append(presentar_emision(resultado))
    return mensajes
