/////////////////////////////////////////////////////////////
//                     VEHICLE TEMPLATE                    //
/////////////////////////////////////////////////////////////

// Function to allow only numbers, uppercase and dashes in vehicle template - plate field
$("#plate")
  .keypress(function (e) {
    var allowedChars = new RegExp("^[A-Z0-9-]+$");
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (allowedChars.test(str)) {
      return true;
    }
    e.preventDefault();
    return false;
  })
  .keyup(function () {
    var forbiddenChars = new RegExp("[^A-Z0-9-]", "g");
    if (forbiddenChars.test($(this).val())) {
      $(this).val($(this).val().replace(forbiddenChars, ""));
    }
  });

//  Filling year dropdownbox from 1920 to currentyear
var nowY = new Date().getFullYear(),
  options = "";

for (var Y = nowY; Y >= 1920; Y--) {
  options += "<option>" + Y + "</option>";
}
$("#year").append(options);

//  Listening if make dropdown list changes,
//  to fill it up with its correspondent models
const makeDropdownbox = document.getElementById("make");

const modelDropdownbox = document.getElementById("vehicleModel");

makeDropdownbox.addEventListener("change", (e) => {
  console.log(e.target.value);
  const selectedmake = e.target.value;

  //  Cleaning previous selections
  modelDropdownbox.innerHTML = "";

  $.ajax({
    type: "GET",
    url: `models-json/${selectedmake}/`,
    success: function (response) {
      console.log(response.data);
      const modelsData = response.data;

      //  First option
      const option = document.createElement("option");
      option.textContent = "Open this select menu";
      modelDropdownbox.appendChild(option);

      //  Options from database
      modelsData.map((item) => {
        const option = document.createElement("option");
        option.textContent = item.name;
        option.setAttribute("value", item.id);
        modelDropdownbox.appendChild(option);
      });
    },
    error: function (error) {
      console.log(error);
    },
  });
});
