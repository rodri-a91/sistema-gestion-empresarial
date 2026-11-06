from inicio.aplication.casos_uso import consultar_factura, emitir_factura
from inicio.domain.impuestos import ImpuestoGeneral, ImpuestoRecargo, ImpuestoReducido
from inicio.dominio import Factura, LineaFactura
from inicio.infraestructure.repository import RepositorioLista, RepositorioMemoria
from inicio.notificaciones import NotificadorEmail, NotificadorFactura


class AvisoPrueba(NotificadorFactura):
    def __init__(self) -> None:
        self.avisos: list[float] = []

    def notificar(self, factura: Factura, total: float) -> None:
        self.avisos.append(total)


class RepositorioConFallo(RepositorioMemoria):
    def guardar(self, factura: Factura) -> None:
        raise OSError("Fallo simulado")


def comprobar_emision() -> None:
    factura = Factura(
        "F-001",
        "Comercial Aula SL",
        "B12345678",
        (
            LineaFactura("Licencia ERP", 1, 1500.0),
            LineaFactura("Soporte", 2, 250.0),
        ),
    )
    for repositorio in (RepositorioMemoria(), RepositorioLista()):
        for calculador, esperado in (
            (ImpuestoGeneral(), 2420.0),
            (ImpuestoReducido(), 2200.0),
            (ImpuestoRecargo(), 2524.0),
        ):
            canal = AvisoPrueba()
            assert emitir_factura(factura, calculador, repositorio, canal) == esperado
            assert repositorio.buscar("F-001") == factura
            assert canal.avisos == [esperado]
            assert emitir_factura(factura, calculador, repositorio) == esperado
    canal = AvisoPrueba()
    try:
        emitir_factura(factura, ImpuestoGeneral(), RepositorioConFallo(), canal)
    except OSError:
        pass
    else:
        raise AssertionError("Se ocultó el error de guardado")
    assert canal.avisos == []


def main() -> None:
    factura = Factura(
        "F-001",
        "Comercial Aula SL",
        "B12345678",
        (LineaFactura("Licencia ERP", 1, 1500.0), LineaFactura("Soporte", 2, 250.0)),
    )

    repo = RepositorioMemoria
    resultado = emitir_factura(
        factura, ImpuestoRecargo(), repo, NotificadorEmail("info@example.com")
    )

    assert resultado.total == 2524.0
    assert repo.buscar(factura.numero) == factura

    try:
        consultar_factura("", repo)
    except ValueError:
        print("Número vacío: valueerror esperado")
    else:
        raise AssertionError("La consulta con nombre vacío no debía llegar aquí")

    try:
        consultar_factura("AUSENTE", repo)
    except LookupError:
        print("Consulta factura AUSENTE: lookuperror esperado")
    else:
        raise AssertionError("La consulta debía fallar")

    print(resultado)

    # comprobar_emision()
    # factura = Factura('F-001', 'Comercial Aula SL', 'B12345678', (
    #     LineaFactura('Licencia ERP', 1, 1500.0),
    #     LineaFactura('Soporte', 2, 250.0),
    # ))
    # repo = RepositorioMemoria()
    # canal = NotificadorEmail('aula@example.com')
    # total = emitir_factura(factura, ImpuestoRecargo(), repo, canal)
    # assert total == 2524.0
    # assert repo.buscar('F-001') == factura
    # print(f'Emitida: {total:.2f} EUR')
    # print('Integración: dos repositorios, tres impuestos, aviso opcional y fallo, OK')


if __name__ == "__main__":
    main()
