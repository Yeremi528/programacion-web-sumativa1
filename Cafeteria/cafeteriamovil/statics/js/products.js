// Variable para almacenar la tasa de cambio
let dolarData = {};

// Funcion para obtener el tipo de cambio desde DolarAPI
async function getDolarRate() {
  try {
      const response = await fetch('https://cl.dolarapi.com/v1/cotizaciones/usd');
      dolarData = await response.json();
      console.log('Datos del dólar cargados:', dolarData);
      
      // Actualizar la información del tipo de cambio
      updateCurrencyInfo();
      
      // Calcular los precios en USD de todos los productos
      calculateUsdPrices();
      
      return dolarData;
  } catch (error) {
      console.error('Error al obtener tipo de cambio:', error);
      document.getElementById('currency-info').innerHTML = 
          '<div class="alert alert-warning" role="alert">No se pudo obtener información del tipo de cambio. Intente más tarde.</div>';
      
      // Mostrar mensaje de error en los precios USD
      const usdPriceElements = document.querySelectorAll('[data-price]');
      usdPriceElements.forEach(element => {
          element.textContent = 'Error al calcular USD';
          element.classList.remove('text-success');
          element.classList.add('text-danger');
      });
  }
}

// Funcion para actualizar la informacion del tipo de cambio
function updateCurrencyInfo() {
  const currencyInfoElement = document.getElementById('currency-info');
  if (dolarData && dolarData.venta) {
      currencyInfoElement.innerHTML = `
          <div class="d-flex align-items-center justify-content-center">
              <i class="bi bi-currency-exchange me-2 text-light"></i>
              <strong class="text-light">Tipo de cambio:</strong>
              <span class="ms-2 text-light">1 USD = ${dolarData.venta.toFixed(2)} CLP</span>
          </div>
      `;
  }
}

// Funcion para calcular los precios en USD
function calculateUsdPrices() {
  if (!dolarData || !dolarData.venta) {
      console.error('No hay datos de tipo de cambio disponibles');
      return;
  }
  
  const usdPriceElements = document.querySelectorAll('[data-price]');
  usdPriceElements.forEach(element => {
      const clpPrice = parseFloat(element.getAttribute('data-price'));
      const usdPrice = (clpPrice / dolarData.venta).toFixed(2);
      element.textContent = `${usdPrice} USD`;
  });
}

window.addEventListener('DOMContentLoaded', async () => {
  await getDolarRate();
});