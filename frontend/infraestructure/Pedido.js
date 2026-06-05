export class Pedido {
    constructor({ id_pedido, id_profile, id_product, fecha_renta, fecha_devolucion, estado, total }) {
        this.id = id_pedido;
        this.id_profile = id_profile;
        this.id_product = id_product;
        this.fecha_renta = fecha_renta;
        this.fecha_devolucion = fecha_devolucion;
        this.estado = estado;
        this.total = total;
    }
}
