# superhero-app
Create an account and search superheros using an external API, and add them to favorites. The app is called "Find A Hero".

The API that the app calls is https://superheroapi.com/

The language of this app mostly consists of Python, some Javascript/JQuery. For the databse and server Postgesql 13 and Flask SQLAlchemy are used 
for a full CRUD app. 

The modles.py is where the tables live along with a function that connects the app.py to the database. There are two modles, one for users loging in 
and one for favorited superheros. Using flask_bcrypt the users password is hashed when stored. These two tables have a relationship being the user_id.

The app.py calls the function from modles to connect to the database. The first route is just a blank index, and the second one is /superheros.
This is where https://superheroapi.com/ is called. Using a form's name and parsing out the json. By creating an object with the data it will be displayed 
on a the index template. The favorites route just querys all superheros from the table and displays them on a template. The register and login 
routes use WTForms to store and authenticate data. api/superheros is an in house api that is used to get, post, and delete superheros from the database. 

Bootstrap was used for most of the styling. The base.html holds the links, navbar, and flashed messages, which are chained to all the other templates.
The index just contains a form, which is the one used to call https://superheroapi.com/. Once a superheros name is searched, it's displayed under the form
using a card. Its shows the heros image, name, place of birth, and powerstats. At the bottom of the card, is a button that once clicked stores the hero in the 
Favoritehero modle. The favorites templates consists of a table that holds all favorited heros. It displays their image, name and a button for deleteing. When
the button is hit, it is deleted from the table as well as the database. The login and register templates just display the forms, title, and flashed mesages 
for logging in or errors.

JQuery was used for a some handler functions. One in particular being the delete button on the favorites table. Using an aysnc function with await axios.delete
the superhero is deleted from the DB and DOM. Styles.css holds a some styling for the aplication. The test.py holds a few tests using unittests and TestCase. 
Requirments.txt holds all the tools need for this project.

So basically a user creates an account and logs in. Then searches a superhero by name from a form, which is diplayed once searched. If the user likes the hero
they can click the button on the bottom of the card, and add it to favorites. Once they are done searching they can go to the favorites page (which is only 
accesed once logged in), to view thier favorites. There then can view them and say WOOOOWWWWW or say NAHHHHHH and delete them. Thanks for reading!
