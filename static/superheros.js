const BASE_URL = 'http://127.0.0.1:5000'

//  ------------SEARCH FORMS--------------------
// change background color on formOne once clicked

$('.buttonOneCls').click(function() {

    let $elem = $(this);
    let black = $elem.css('background-color');
    $elem.css('backgroundColor', '#FF0000');
    setTimeout(function() {
      $elem.css('background-color', black);
    }, 1000);
  });


// ----------FAVORITES PAGE-------------------
// delete superhero from DB and table with button click

$('.delete-superhero').click(deleteSuperhero)

  async function deleteSuperhero() {
    const id = $(this).data('id')
    await axios.delete(`/api/superheros/${id}`)
    $(this).closest('tr').remove()
  }
  



//favorites page

// $('.delete-superhero').click(deleteSuperhero)

// async function deleteSuperhero() {
//     const id = $(this).data('id')
//     await axios.delete(`/api/superheros/${id}`)
//     $(this).closest('tr').remove()
// };



// ---------------SUPERHERO CARDS-----------------------------------
// on click function to hide card then display it when form is submitted

// document.getElementById('buttonOne').onclick = function(event){
//     event.preventDefault();
//     let showCard = document.getElementById('card-container');
//     if ( showCard.style.display != 'none' ){
//         showCard.style.display = 'block';
//     }
//     else {
//         showCard.style.display = 'block';
//     };
// };








