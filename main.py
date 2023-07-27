from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
from colorthief import ColorThief
from webcolors import rgb_to_name, hex_to_rgb, CSS3_HEX_TO_NAMES
from scipy.spatial import KDTree


UPLOAD_FOLDER = os.path.join('static', 'uploads')
app = Flask(__name__)
app.secret_key = "kjdfkae23984kdjf93jkdfj93"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]


img = ColorThief('static/uploads/istockphoto-520700958-612x612.jpg')
colors = img.get_palette(color_count=11)
colors_name = []
for color in colors:
    colors_name.append(convert_rgb_to_names(color))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        image = request.files["image"]
        img_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config.get('UPLOAD_FOLDER'), img_filename))
        session['uploaded_image_file_path'] = os.path.join(app.config.get('UPLOAD_FOLDER'), img_filename)
    return render_template('index.html')


@app.route('/show_image')
def display_image():
    img_file_path = session.get('uploaded_image_file_path')
    return render_template('image.html', user_image=img_file_path)


@app.route('/show_color')
def show_color():
    img = ColorThief(session.get('uploaded_image_file_path'))
    colors = img.get_palette(color_count=11)
    colors_name = []
    for color in colors:
        colors_name.append(convert_rgb_to_names(color))
    return render_template('colors.html', colors=colors, names=colors_name)


if __name__ == "__main__":
    app.run(debug=True)




