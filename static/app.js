
const BASE_URL = '/api/cupcakes'



$('form').on("submit", async function(e) {
    e.preventDefault();
    let flavor =  $('#flavor').val()
    let size = $('#size').val()
    let rating = $('#rating').val()
    let image = $('#image').val()

    const new_cupcake = await createCupcake(flavor, size, rating, image)
    const new_cupcake_style = cupcakeHTML(new_cupcake)
    
    $('ul').append(new_cupcake_style)
    $("#new-cupcake-form").trigger("reset");
})

async function createCupcake(flavor, size, rating, image){

    const resp = await axios.post(BASE_URL, {flavor, size, rating, image})
    return resp.data.cupcake
}

function cupcakeHTML(cupcake) {
    return `
        <div data-cupcake-id=${cupcake.id}>
            <li> ${cupcake.flavor} - ${cupcake.size} </li>
            <img src="${cupcake.image}">
            </div>
        `;
}

async function getAllCupcakes() {
    const resp = await axios.get(BASE_URL)
    return resp.data.cupcakes
}

async function showAllCupcakes() {
    const cupcakes = await getAllCupcakes()
    for(let c of cupcakes) {
        const cStyled = $(cupcakeHTML(c))
        $('ul').append(cStyled)
    }
}

showAllCupcakes();