// Función para cargar los productos desde la API
async function cargarProductos() {
    const tablaProductos = document.getElementById("tablaProductos");
    tablaProductos.innerHTML = ""; // Limpiamos la tabla
  
    try {
        const response = await fetch('/api/productos/');
        const productos = await response.json();
  
        productos.forEach(producto => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${producto.id}</td>
                <td>${producto.product_name}</td>
                <td>${producto.product_desc}</td>
                <td>$${producto.product_price}</td>
                <td>${producto.stock_product}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editarProducto(${producto.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="eliminarProducto(${producto.id})">Eliminar</button>
                </td>
            `;
            tablaProductos.appendChild(tr);
        });
    } catch (error) {
        console.error("Error al cargar los productos: ", error);
    }
  }
  
  // Función para mostrar el modal de edición con los datos del producto usando SweetAlert2
  async function editarProducto(id) {
    try {
        // Obtener el producto desde la API
        const response = await fetch(`/api/productos/${id}`);
        const producto = await response.json();
  
        if (producto) {
            // Usamos SweetAlert2 para crear el formulario de edición en el modal
            const { value: formValues } = await Swal.fire({
                title: 'Editar Producto',
                html: `
                    <form id="editarForm">
                        <span class="">Nombre producto</span>
                        <input id="editNombre" class="swal2-input" value="${producto.product_name}" placeholder="Nombre del Producto">
                        <input id="editDescripcion" class="swal2-input" value="${producto.product_desc}" placeholder="Descripción">
                        <input id="editPrecio" class="swal2-input" type="number" value="${producto.product_price}" placeholder="Precio">
                        <input id="editStock" class="swal2-input" type="number" value="${producto.stock_product}" placeholder="Stock">
                    </form>
                `,
                focusConfirm: false,
                preConfirm: () => {
                    // Obtener los datos del formulario
                    return {
                        product_name: document.getElementById('editNombre').value,
                        product_desc: document.getElementById('editDescripcion').value,
                        product_price: document.getElementById('editPrecio').value,
                        stock_product: document.getElementById('editStock').value
                    };
                }
            });
  
            // Si el usuario confirma el modal
            if (formValues) {
                // Crear el objeto con los datos a enviar
                const updatedProduct = {
                    product_name: formValues.product_name,
                    product_desc: formValues.product_desc,
                    product_price: formValues.product_price,
                    stock_product: formValues.stock_product
                };
  
                // Enviar los datos al servidor
                const editResponse = await fetch(`/api/productos/${id}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(updatedProduct)
                });
  
                // Verificar si la respuesta fue exitosa
                if (editResponse.ok) {
                    Swal.fire('¡Éxito!', 'Producto actualizado correctamente.', 'success');
                    cargarProductos();  // Recargar la lista de productos
                } else {
                    Swal.fire('Error', 'Hubo un error al actualizar el producto.', 'error');
                }
            }
        }
    } catch (error) {
        console.error("Error al obtener el producto: ", error);
    }
  }
  
  
  // Función para mostrar el modal de eliminación con SweetAlert2
  async function eliminarProducto(id) {
    const producto = await fetch(`/api/productos/${id}/`);
    const productoData = await producto.json();
  
    if (productoData) {
        // Usamos SweetAlert2 para confirmar la eliminación
        const result = await Swal.fire({
            title: `¿Estás seguro de eliminar el producto ${productoData.product_name}?`,
            text: "Esta acción no se puede deshacer.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        });
  
        if (result.isConfirmed) {
            try {
                const deleteResponse = await fetch(`/api/productos/${id}/`, {
                    method: 'DELETE',
                });
  
                if (deleteResponse.ok) {
                    cargarProductos();  // Recargar la lista de productos
                    Swal.fire('Eliminado', 'El producto ha sido eliminado.', 'success');
                } else {
                    Swal.fire('Error', 'Hubo un error al eliminar el producto.', 'error');
                }
            } catch (error) {
                console.error("Error al eliminar el producto: ", error);
            }
        }
    }
  }
  
  // Función para crear un nuevo producto con SweetAlert2
  document.getElementById("formularioProducto").onsubmit = async function (e) {
    e.preventDefault();
  
    const newProduct = {
        product_name: document.getElementById("nombre").value,
        product_desc: document.getElementById("descripcion").value,
        product_price: document.getElementById("precio").value,
        stock_product: document.getElementById("stock").value
    };
  
    try {
        const response = await fetch('/api/productos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newProduct)
        });
  
        if (response.ok) {
            cargarProductos();  // Recargar la lista de productos
            document.getElementById("formularioProducto").reset();  // Limpiar el formulario
            Swal.fire('Producto creado', 'El producto ha sido creado exitosamente.', 'success');
        } else {
            Swal.fire('Error', 'Hubo un error al crear el producto.', 'error');
        }
    } catch (error) {
        console.error("Error al crear el producto: ", error);
    }
  };
  
  // Cargar los productos cuando se carga la página
  document.addEventListener('DOMContentLoaded', cargarProductos);
  