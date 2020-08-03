# -*- coding: utf-8 -*-

#estados de factura y remisión
class EstadoDocumento:
    PENDIENTE = 'PEN'
    CONFIRMADO = 'CON'
    ANULADO = 'ANU'
    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (CONFIRMADO, 'Confirmado'),
        (ANULADO, 'Anulado'),
    )
