class UsuarioException(Exception):
    ...

class UsuarioNotFoundError(UsuarioException):
    def __init__(self):
        self.status_code = 404
        self.detail = "USUARIO_NAO_ENCONTRADO"


class UsuarioAlreadyExistError(UsuarioException):
    def __init__(self):
        self.status_code = 409
        self.detail = "EMAIL_DUPLICADO"

class VendaException(Exception):
    ...

class VendaNotFoundError(VendaException):
    def __init__(self):
        self.status_code = 404
        self.detail = "EMPRESTIMO_NAO_ENCONTRADO"
class DrogaException(Exception):
    ...

class DrogaNotFoundError(DrogaException):
    def __init__(self):
        self.status_code = 404
        self.detail = "DROGA_NAO_ENCONTRADA"

class ItemVendaException(Exception):
    ...

class ItemVendaNotFoundError(ItemVendaException):
    def __init__(self):
        self.status_code = 404
        self.detail = "ITEM_VENDA_NAO_ENCONTRADO"
class ItemVendaAlreadyExistError(ItemVendaException):
    def __init__(self):
        self.status_code = 409
        self.detail = "ITEM_VENDA_DUPLICADO"