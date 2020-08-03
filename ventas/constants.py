# -*- coding: utf-8 -*-

class CondicionDeVenta:
    CONTADO = 'CON'
    CREDITO = 'CRE'
    CONDICIONES = (
        (CONTADO, 'Contado'),
        (CREDITO, 'Crédito'),
    )


class Iva:
    DIEZ = '10'
    CINCO = '05'
    EXENTA = '00'
    PORCENTAJES = (
        (DIEZ, '10 %'),
        (CINCO, '5 %'),
        (EXENTA, 'exenta')
    )
