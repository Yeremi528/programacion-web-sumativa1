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

//Funcion para editar un producto
async function editarProducto(id) {
  try {
    // Obtenemos el producto desde la API
    const response = await fetch(`/api/productos/${id}`);
    const producto = await response.json();

    if (producto) {
      // Usamos SweetAlert2 para crear el formulario de edicion con mejor diseño
      const { value: formValues } = await Swal.fire({
          title: 'Editar Producto',
          html: `
              <form id="editarForm" class="text-left">
                  <div class="form-group mb-3" style="text-align: left">
                      <label for="editNombre" style="display: block; margin-bottom: 5px; font-weight: 500;">Nombre producto</label>
                      <input id="editNombre" class="form-control" value="${producto.product_name}" placeholder="Nombre del Producto">
                  </div>
                  <div class="form-group mb-3" style="text-align: left">
                      <label for="editDescripcion" style="display: block; margin-bottom: 5px; font-weight: 500;">Descripción</label>
                      <textarea id="editDescripcion" class="form-control" rows="3" placeholder="Descripción">${producto.product_desc}</textarea>
                  </div>
                  <div class="form-group mb-3" style="text-align: left">
                      <label for="editPrecio" style="display: block; margin-bottom: 5px; font-weight: 500;">Precio</label>
                      <input id="editPrecio" class="form-control" type="number" value="${producto.product_price}" placeholder="Precio">
                  </div>
                  <div class="form-group mb-3" style="text-align: left">
                      <label for="editStock" style="display: block; margin-bottom: 5px; font-weight: 500;">Stock</label>
                      <input id="editStock" class="form-control" type="number" value="${producto.stock_product}" placeholder="Stock">
                  </div>
              </form>
          `,
          focusConfirm: false,
          showCancelButton: true,
          confirmButtonText: 'Guardar',
          cancelButtonText: 'Cancelar',
          customClass: {
              container: 'my-swal-container',
              popup: 'my-swal-popup',
              content: 'my-swal-content'
          },
          preConfirm: () => {
              // Captura los valores de los campos
              const nombre = document.getElementById('editNombre').value;
              const descripcion = document.getElementById('editDescripcion').value;
              const precio = document.getElementById('editPrecio').value;
              const stock = document.getElementById('editStock').value;
              
              // Valida que no esten vacios
              if (!nombre || !descripcion || !precio || !stock) {
                  Swal.showValidationMessage('Por favor complete todos los campos');
                  return false;
              }
              
              return {
                  product_name: nombre,
                  product_desc: descripcion,
                  product_price: precio,
                  stock_product: stock
              };
          }
      });

      // Si el usuario confirma el modal y los valores existen
      if (formValues) {
        console.log("Datos a enviar:", formValues); // Para depuración
        // Envia los datos al servidor sin token CSRF
        const editResponse = await fetch(`/api/productos/${id}/`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(formValues)
        });

        // Verificar si la respuesta fue exitosa
        if (editResponse.ok) {
          Swal.fire('¡Éxito!', 'Producto actualizado correctamente.', 'success');
          cargarProductos();  // Recarga la lista de productos
        } else {
          const errorData = await editResponse.json().catch(() => ({}));
          Swal.fire('Error', 'Hubo un error al actualizar el producto.', 'error');
          console.error('Error respuesta:', errorData);
        }
      }
    }
  } catch (error) {
      console.error("Error al obtener el producto: ", error);
      Swal.fire('Error', `Error en la operación: ${error.message}`, 'error');
  }
}

// Función para mostrar el modal de eliminación con SweetAlert2
async function eliminarProducto(id) {
  const producto = await fetch(`/api/productos/${id}/`);
  const productoData = await producto.json();

  if (productoData) {
    // Usamos SweetAlert2 para confirmar la eliminacion
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
          cargarProductos();  // Recarga la lista de productos
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
      cargarProductos();  // Recarga la lista de productos
      document.getElementById("formularioProducto").reset();  // Limpia el formulario
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
  