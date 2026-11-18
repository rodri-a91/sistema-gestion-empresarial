from facturacion.application.puertos import NotificadorFactura, RepositorioFacturas
from facturacion.application.resultados import ResultadoEmision
from facturacion.domain.entidades import Factura
from facturacion.domain.impuestos import CalculadorImpuesto


def emitir_factura(
    factura: Factura,
    calculador: CalculadorImpuesto,
    repositorio: RepositorioFacturas,
    notificador: NotificadorFactura | None = None,
) -> ResultadoEmision:
    total = factura.calcular_total(calculador)
    repositorio.guardar(factura)
    if notificador is not None:
        notificador.notificar(factura, total)
    return ResultadoEmision(factura.numero, total)


def consultar_factura(numero: str, repositorio: RepositorioFacturas) -> Factura:
    if not numero.strip():
        raise ValueError('El número es obligatorio')
    factura = repositorio.buscar(numero)
    if factura is None:
        raise LookupError(f'Factura {numero} no encontrada')
    return factura
