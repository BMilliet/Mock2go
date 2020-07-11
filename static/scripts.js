
let addRouteButton = document.querySelector('#addRouteButton');

addRouteButton.addEventListener('click', () => {
  let routeTemplate = `
                        <div class="routes_container">
                          <div class="form_element">
                            <label>path: </label>
                            <input type="text" value="" name="path">
                          </div>
                          <div style="height: 8px;"></div>
                          responses
                          <div class="form_element">
                          <textarea name="responses" cols="60" rows="5"></textarea>
                          </div>
                          <div style="height: 16px;"></div>
                        </div>`;

  document.getElementById('serviceContainer').innerHTML += routeTemplate;
});
