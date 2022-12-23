
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw, ImageColor
import base64
import io
import random
import re


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///poems.db")


@app.route("/")
def index():
    """default page"""

    query = 'SELECT * FROM poem'
    print(query)
    poem = db.execute(query)
    rannum = random.randint(0, len(poem)-1)


    return render_template("index.html", poem = poem[rannum])
@app.route("/poems")
def poemspage():

    poems = db.execute("SELECT * FROM poem")

    return render_template("poems.html", poems = poems)
@app.route("/poem")
def poempage():
    title = request.args.get("title")
    query = 'SELECT * FROM poem WHERE title = "' + title + '"'
    print(query)
    poem = db.execute(query)
    if (len(poem) > 0):
        print(poem[0]["content"])
        return render_template("poem.html", poem = poem[0])
    return render_template("index.html")

@app.route("/makeimg")
def makeimg():

    #need to pass list of all poem titles, and all font options

    fontoptions = ["Dancing Script", "Kenia", "Rubik Gemstones"]
    poems = db.execute("SELECT * FROM poem")
    authors = db.execute('SELECT DISTINCT "author" FROM poem')

    #need to pass list of all tags and authors

    tagoptions = ["nature", "friendship", "parting", "romance", "love", "women", "loneliness", "moonlight", "alcohol", "home", "music", "war", "frontier", "hardship", "tranquility", "nostalgia"]


    return render_template("makeimg.html", poems = poems, fonts = fontoptions, tags = tagoptions, authors = authors)


@app.route("/draw")
def drawimg():

    #get request info

    style = request.args.get("styleselect")
    print(style)
    pickedfont = request.args.get("fontselect")

    fontaddress = 'fonts/DancingScript-VariableFont_wght.ttf'
    if pickedfont == "Kenia":
        #set fontaddress to kenia
        fontaddress = 'fonts/Kenia-Regular.ttf'
    elif pickedfont == "Rubik Gemstones":
        fontaddress = 'fonts/RubikGemstones-Regular.ttf'

    size = request.args.get("sizeselect")
    bgimg = request.args.get("imgselect")
    color = request.args.get("colorselect")
    
    if (style == None or size == None or bgimg == None or color == None ):
        return render_template("notfound.html")

    try:
        if (int(bgimg) > 3 or int(bgimg) < 1):
            print("invalid int")
            print(int(bgimg))
            return render_template("notfound.html")
    except ValueError:
        print("not an int")
        return render_template("notfound.html")

    print(color)

    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)  #from stack overflow, uses regular expressions to check if string is a valid hexadecimal before trying to convert hex to RGB. prevents crashes if user somehow gives invalid color
    if not match:
        print('Hex is invalid')
        return render_template("notfound.html")

    rgb = ImageColor.getcolor(color, "RGB")
    print(rgb)
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    if (style == "By Title"):

        #first get select style, in order to choose to use poem by title or a random poem by author/tag
        title = request.args.get("poemselect")

        query = 'SELECT * FROM poem WHERE title = "' + title + '"'
        print(query)
        poem = db.execute(query)
        if (len(poem) > 0):
            print(poem[0]["content"])
            imgpath = "static/images/" + bgimg + ".png"

            my_image = Image.open(imgpath)
            title_text = poem[0]["content"]+ "- " + poem[0]["author"]
            title_font = ImageFont.truetype(fontaddress, int(size))
            image_editable = ImageDraw.Draw(my_image)
            image_editable.text((15,15), title_text, (red, green, blue), font=title_font)
            data = io.BytesIO()
            my_image.save(data, "PNG")
            encoded_img_data = base64.b64encode(data.getvalue())
            return render_template("download.html", img_data=encoded_img_data.decode('utf-8'))
        else:
            return render_template("notfound.html")
    else:
        author = request.args.get("authorselect")
        print(author)
        taglist = request.args.getlist("checktag")
        print(taglist)

        tagstring = ""
        if len(taglist) > 0:
            tagstring = "AND tags LIKE '%"+taglist[0] + "%'"
            i = 0
            for tag in taglist:
                if i > 0:
                    tagstring = tagstring + " AND tags LIKE '%" + tag + "%'"
                i = i + 1

        if (author != "Any"):
            if (len(taglist) > 0):
                query = 'SELECT * FROM poem WHERE author = "' + author + '" ' + tagstring
                print(query)
                poem = db.execute(query)
                if len(poem) > 0:
                    rannum = random.randint(0, len(poem)-1)
                    print(poem[rannum]["content"])
                    imgpath = "static/images/" + bgimg + ".png"

                    my_image = Image.open(imgpath)
                    title_text = poem[rannum]["content"] + "- " + poem[rannum]["author"]
                    title_font = ImageFont.truetype(fontaddress, int(size))
                    image_editable = ImageDraw.Draw(my_image)
                    image_editable.text((15,15), title_text, (red, green, blue), font=title_font)
                    data = io.BytesIO()
                    my_image.save(data, "PNG")
                    encoded_img_data = base64.b64encode(data.getvalue())
                    return render_template("download.html", img_data=encoded_img_data.decode('utf-8'))
            else:
                query = 'SELECT * FROM poem WHERE author = "' + author + '"'
                print(query)
                poem = db.execute(query)
                if len(poem) > 0:
                    rannum = random.randint(0, len(poem)-1)

                    print(poem[rannum]["content"])
                    imgpath = "static/images/" + bgimg + ".png"

                    my_image = Image.open(imgpath)
                    title_text = poem[rannum]["content"] + "- " + poem[rannum]["author"]
                    title_font = ImageFont.truetype(fontaddress, int(size))
                    image_editable = ImageDraw.Draw(my_image)
                    image_editable.text((15,15), title_text, (red, green, blue), font=title_font)
                    data = io.BytesIO()
                    my_image.save(data, "PNG")
                    encoded_img_data = base64.b64encode(data.getvalue())
                    return render_template("download.html", img_data=encoded_img_data.decode('utf-8'))
        else:
            tagstring = ""
            if len(taglist) > 0:
                tagstring = "WHERE tags LIKE '%"+taglist[0] + "%'"
                i = 0
                for tag in taglist:
                    if i > 0:
                        tagstring = tagstring + " AND tags LIKE '%" + tag + "%'"
                    i = i + 1
                query = 'SELECT * FROM poem ' + tagstring
                print(query)
                poem = db.execute(query)
                if len(poem) > 0:
                    rannum = random.randint(0, len(poem)-1)
                    print(poem[rannum]["content"])
                    imgpath = "static/images/" + bgimg + ".png"

                    my_image = Image.open(imgpath)
                    title_text = poem[rannum]["content"] + "- " + poem[rannum]["author"]
                    title_font = ImageFont.truetype(fontaddress, int(size))
                    image_editable = ImageDraw.Draw(my_image)
                    image_editable.text((15,15), title_text, (red, green, blue), font=title_font)
                    data = io.BytesIO()
                    my_image.save(data, "PNG")
                    encoded_img_data = base64.b64encode(data.getvalue())
                    return render_template("download.html", img_data=encoded_img_data.decode('utf-8'))
            else:
                query = 'SELECT * FROM poem '
                print(query)
                poem = db.execute(query)
                rannum = random.randint(0, len(poem)-1)
                print(poem[rannum]["content"])
                imgpath = "static/images/" + bgimg + ".png"
                my_image = Image.open(imgpath)
                title_text = poem[rannum]["content"] + "- " + poem[rannum]["author"]
                title_font = ImageFont.truetype(fontaddress, int(size))
                image_editable = ImageDraw.Draw(my_image)
                image_editable.text((15,15), title_text, (red, green, blue), font=title_font)
                data = io.BytesIO()
                my_image.save(data, "PNG")
                encoded_img_data = base64.b64encode(data.getvalue())
                return render_template("download.html", img_data=encoded_img_data.decode('utf-8'))







        return render_template("notfound.html")

