from typing import List, Optional
from pydantic import BaseModel, Field


class Motivo(BaseModel):
    titulo: str
    criterio: str
    descripcion: str


class Detalle(BaseModel):
    descripcion: str
    lote: str
    vencimiento: str
    cantidad: int


class ReportadoA(BaseModel):
    nombre: str
    empresa: str
    fecha: str
    nombre1: str
    empresa1: str
    fecha1: str


class FirmaRecepcion(BaseModel):
    nombre: str
    firma: str


class FirmaTecnico(BaseModel):
    nombre: str
    firma: str


class FirmaAutorizacion(BaseModel):
    nombre: str
    fecha: str
    login: str


class Novedad(BaseModel):
    _id: dict
    formulario: str
    lugar: str
    ruc_proveedor: str
    nombre_proveedor: str
    numero_factura: str
    fecha: dict
    fecha_factura: dict
    remitente: str
    transportista: str
    no_cajas: int
    anulado: str
    motivo: List[Motivo]
    detalle: List[Detalle]
    descripcion_novedad: str
    procedimiento: List[dict]
    reportado_a: List[ReportadoA]
    firma_recepcion: List[FirmaRecepcion]
    firma_tecnico: List[FirmaTecnico]
    archivos: List[str]
    secuencia: int
    __v: int
    estado: str
    firma_autorizacion: List[FirmaAutorizacion]
    

class Producto(BaseModel):
    _id: dict
    especificaciones: List[str] = []


class Auditoria(BaseModel):
    _id: dict
    login: str
    fecha: str
    operacion: str
    aprobado: str


class Recepcion(BaseModel):
    _id: dict
    formulario: str
    lugar: str
    ruc_proveedor: str
    nombre_proveedor: str
    numero_factura: str
    aprobado: str
    fecha: dict
    fecha_factura: dict
    anulado: str
    productos: List[Producto]
    firma_entrega: List[FirmaRecepcion]
    firma_recepcion: List[FirmaTecnico]
    firma_autorizacion: List[FirmaAutorizacion]
    archivos: List[str]
    auditoria: List[Auditoria]
    secuencia: int
    __v: int
    estado: str
    


