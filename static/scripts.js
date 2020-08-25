
let addRouteButton = document.querySelector('#addRouteButton');


addRouteButton.addEventListener('click', () => {
  let routesCount = document.querySelectorAll('#routeId').length;

  let routeTemplate = `
                        <div class="routes_container">
                        <div class="form_element" id="routeId">
                        <label>route: </label>
                        <input type="text" value="" name="route">
                        </div>

                        <div class="space8"></div>
                        responses
                        <div class="form_element">
                        <input type="file" multiple="multiple" name="responses${routesCount}">
                        </div>

                        <div class="space16"></div>
                        </div>`;

  document.getElementById('serviceContainer').innerHTML += routeTemplate;
});
