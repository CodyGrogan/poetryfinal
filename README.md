# Chinese Poetry Image Generator and Database

#### Video Demo:  <URL HERE>
#### Description:
This project was made for the final project of Harvard's CS50x. It was made with Python, Flask, Jinja2, and SQLite. Background images were made with Stable Diffusion, and translations by Ying Sun.

I was interested in making a project like this after taking a Chinese poetry course in college and thought it would be nice to have a database that was searchable by tags describing the content rather than just authors. To make the project more complicated I decided to make sharable images with the poems written on them. The user is able to select a poem by title, or select a random poem using tags and/or an author's name. The user can also select a color, a font, text size, and one of three background images that I made with stable diffusion that look similar to old Chinese paintings that often would be inscribed with lines of poetry.

I left the styling mostly with default bootstrap elements as I've never been very artistically inclined. Since the theme of this was Chinese poetry I thought it would be neat to add an animation showing the chinese words for differnt menu options as you hovered over them, and this was implemented purely in CSS.

The project uses a very small amount of jquery and uses jquery datatables to make an easily searchable and sortable table for the poetry database. The datatable uses bootstrap styling. 

User input is properly validated and returns error messages without crashing if the user submits improper input to the server.



To run this locally clone the directory, use pip install -r requirements.txt  to get the necessary packages.
Then run the server with:   flask run --host=0.0.0.0

This worked both in the cs50 cloud environment and locally on my ubuntu server. 

A copy of this project is hosted publicly on my github page:  https://github.com/CodyGrogan/poetryfinal
