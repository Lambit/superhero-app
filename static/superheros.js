const BASE_URL = 'https://superheroapi.com/api/10225580844013004';

// given dadta about superhero, generate html

function generateSuperheroHTML(superhero) {
    return `
        <div data-superhero-id=${superhero.id}
         <li>
            ${superhero.name}
            <button class="delete-button">X</button>
         </li>
         <img class="Superhero-img"
                src="${superhero.image}"
                alt="(no image provided)"
        </div>
        `;
}

// put intial hero on page

async function showInitialSuperhero() {
    const response = await axios.get(`${BASE_URL}/search/name`);

    for(let superheroData of response.data.superheros) {
        let newSuperhero = $(generateSuperheroHTML(superheroData));
        $("#superhero-list").append(newSuperhero);
    }
}

// handle form for adding of new superhero

$('#search-hero-form').on('submit', async function (evt) {
    evt.preventDefault();

    let name = $("#form-name").val();

    const newSuperheroResponse = await axios.post(`${BASE_URL}/search/${name}`, {
        name
    });

    let newSuperhero = $(generateSuperheroHTML(newSuperheroResponse.data.superhero));
    $("#superhero-list").append(newSuperhero);
    $("#search-hero-form").trigger("reset");
});

$("#superhero-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $superhero = $(evt.target).closest('div');
    let superheroId = $superhero.attr("data-superhero-id");

    await axios.delete(`${BASE_URL}/superheros/${superheroId}`);
    $superhero.remove();
});

$(showInitialSuperhero);