from dominio import Factura, LineaFactura

# from impuestos import ImpuestoGeneral, ImpuestoRecargo, ImpuestoReducido
from persistencia import RepositorioLista, RepositorioMemoria


def main() -> None:
    factura = Factura(
        "F-001",
        "Comercial Aula SL",
        "112345678",
        (LineaFactura("Licencia ERP", 1, 1500.0), LineaFactura("Soporte", 2, 250.0)),
    )

    # for calculador, esperado in (
    #     (ImpuestoGeneral(), 2420.0),
    #     (ImpuestoReducido(), 2200.0),
    #     (ImpuestoRecargo(), 2524.0),
    # ):
    #     total = factura.calcular_total(calculador)
    #     assert total == esperado
    #     print(f"{type(calculador).__name__}: {total:.2f}")

    for repo in (RepositorioMemoria(), RepositorioLista()):
        repo.guardar(factura)
        print(repo.buscar("F-001"))
        factura2 = Factura(
            "F-001",
            "dsadsasdasdsadsa",
            "112345678",
            (
                LineaFactura("Licencia ERP", 1, 1500.0),
                LineaFactura("Soporte", 2, 250.0),
            ),
        )
        repo.guardar(factura2)
        print(repo.buscar("F-001"))


if __name__ == "__main__":
    main()
