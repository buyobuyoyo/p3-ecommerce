export class Product {
    constructor({ id_product, titulo, descripcion, genero, precio, disponible, imgurl, duracion, lanzamiento }) {
        this.id = id_product;
        this.titulo = titulo;
        this.descripcion = descripcion;
        this.genero = genero;
        this.precio = precio;
        this.disponible = disponible;
        this.imgurl = imgurl;
        this.duracion = duracion;
        this.lanzamiento = lanzamiento;
    }
}
