def validar_cif(cif: str) -> None:
    """Formato ficticio del taller, sin validación fiscal oficial."""
    if (len(cif) != 9 or not cif.startswith(('A', 'B'))
            or not cif[1:].isascii() or not cif[1:].isdigit()):
        raise ValueError('Se espera A o B seguida de ocho dígitos')
