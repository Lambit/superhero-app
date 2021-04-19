
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
  









