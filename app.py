from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return render_template('result.html', filename=filename)

@app.route('/analyze', methods=['POST'])
def analyze_color():
    r = int(request.form['r'])
    g = int(request.form['g'])
    b = int(request.form['b'])

    selected_rgb = (r, g, b)
    tone_category, tone_name = classify_skin_tone(selected_rgb)
    return render_template(
        'palette.html',
        rgb=selected_rgb,
        tone=tone_category,
        tone_name=tone_name,
        palette=get_palette(tone_name)
    )

def classify_skin_tone(rgb):
    r, g, b = rgb
    tone_name = get_named_tone(r, g, b)

    if tone_name in ["Ivory", "Vanilla", "Shell", "Cool Beige"]:
        return "Fair Cool", tone_name
    elif tone_name in ["Warm Ivory", "Porcelain", "Soft Sand"]:
        return "Fair Warm", tone_name
    elif tone_name in ["Rosy Beige", "Natural Rose", "Neutral Sand"]:
        return "Medium Cool", tone_name
    elif tone_name in ["Golden Natural", "Honey", "Beige Glow"]:
        return "Medium Warm", tone_name
    elif tone_name in ["Espresso", "Cool Cocoa", "Rich Mocha"]:
        return "Deep Cool", tone_name
    elif tone_name in ["Chestnut", "Warm Almond", "Caramel", "Golden Bronze"]:
        return "Deep Warm", tone_name
    else:
        return "Unknown", "Unknown Tone"

def get_named_tone(r, g, b):
    if r > 230 and g > 210 and b > 200:
        return "Ivory"
    elif r > 220 and g > 200 and b > 190:
        return "Vanilla"
    elif r > 215 and g > 195 and b > 185:
        return "Shell"
    elif r > 210 and g > 190 and b > 180:
        return "Cool Beige"
    elif r > 240 and g > 220 and b < 180:
        return "Warm Ivory"
    elif r > 230 and g > 200 and b < 170:
        return "Porcelain"
    elif r > 225 and g > 195 and b < 160:
        return "Soft Sand"
    elif r > 190 and g > 160 and b > 150:
        return "Rosy Beige"
    elif r > 180 and g > 150 and b > 140:
        return "Natural Rose"
    elif r > 175 and g > 145 and b > 135:
        return "Neutral Sand"
    elif r > 200 and g > 170 and b < 130:
        return "Golden Natural"
    elif r > 190 and g > 160 and b < 120:
        return "Honey"
    elif r > 185 and g > 155 and b < 115:
        return "Beige Glow"
    elif r > 100 and g > 80 and b > 70:
        return "Espresso"
    elif r > 90 and g > 70 and b > 60:
        return "Cool Cocoa"
    elif r > 85 and g > 65 and b > 55:
        return "Rich Mocha"
    elif r > 110 and g > 90 and b < 80:
        return "Chestnut"
    elif r > 105 and g > 85 and b < 75:
        return "Warm Almond"
    elif r > 100 and g > 80 and b < 70:
        return "Caramel"
    elif r > 95 and g > 75 and b < 65:
        return "Golden Bronze"
    return "Unknown Tone"

def get_palette(tone_name):
    full_palettes = {
        "Ivory": ['#E6E6FA', '#BFEFFF', '#FFB6C1', '#D3D3D3', '#D8B7DD', '#B0E0E6', '#E0FFF0', '#C4D8E2', '#C0AEB1', '#C0C0C0'],
        "Vanilla": ['#87CEEB', '#FFDDE1', '#F7CAC9', '#B9B3A9', '#98FF98', '#C3CDE6', '#FADADD', '#FFE5B4', '#D8BFD8', '#D8CAB8'],
        "Shell": ['#EED5EA', '#FBC6CA', '#F7E7CE', '#CAD2D3', '#E4E2F0', '#CFCFCF', '#DAF4F0', '#FFDAB9', '#DA70D6', '#758DA3'],
        "Cool Beige": ['#BFA6A0', '#A9A9A9', '#FFEEF0', '#E0FFFF', '#CBCED6', '#7BB2D9', '#DCDCDC', '#C4C3D0', '#E6DAF0', '#B2C6D6'],
        "Warm Ivory": ['#FFE5B4', '#FFFDD0', '#F08080', '#FBCEB1', '#ECD9B0', '#F0FFF0', '#E6B7A9', '#F4A460', '#FDBCB4', '#FFFFF0'],
        "Porcelain": ['#F88379', '#FFFACD', '#F5DEB3', '#F6E2B3', '#E9CFCB', '#FFE0BD', '#FFD59A', '#EEC8B9', '#D4A798', '#F7E7CE'],
        "Soft Sand": ['#D8CAB8', '#E2725B', '#D2B1A3', '#FFE5B4', '#DAA5A4', '#F0E68C', '#FFD2A6', '#D4A017', '#F5BBAA', '#E1C699'],
        "Rosy Beige": ['#800020', '#A94064', '#A3989D', '#722F37', '#580F41', '#B6B6B4', '#B76E79', '#A3989D', '#C54B8C', '#C48189'],
        "Natural Rose": ['#70193D', '#367588', '#6A5ACD', '#DAA5A4', '#8A2BE2', '#4682B4', '#837060', '#E0B0FF', '#C08081', '#905D5D'],
        "Neutral Sand": ['#CBBFB2', '#DCAE96', '#848884', '#C4C3D0', '#483C32', '#E5C1CD', '#B1907F', '#C1A192', '#B2BEB5', '#8A8776'],
        "Golden Natural": ['#CC5500', '#FFBF00', '#B5A642', '#FFDA03', '#7B3F00', '#FF7518', '#DAA520', '#B7410E', '#CD7F32', '#C46210'],
        "Honey": ['#DDB67D', '#FFCBA4', '#C19A6B', '#BC7F61', '#805533', '#FBE870', '#E2725B', '#FFAE42', '#996515', '#CC7722'],
        "Beige Glow": ['#EDC9AF', '#D2B48C', '#A9746E', '#B08D57', '#FFD700', '#E6A57E', '#D2691E', '#F5DEB3', '#AD8A56', '#DA8A67'],
        "Espresso": ['#4169E1', '#50C878', '#673147', '#C0C0C0', '#0F52BA', '#722F37', '#191970', '#D8B7DD', '#708090', '#580F41'],
        "Cool Cocoa": ['#9E003A', '#614051', '#C49DA3', '#36454F', '#9932CC', '#8B4963', '#9400D3', '#4682B4', '#6A5A78', '#2E1A47'],
        "Rich Mocha": ['#70193D', '#837060', '#36454F', '#4B3B47', '#C1A192', '#43464B', '#6699CC', '#7E5E60', '#5A3E36', '#AB92B3'],
        "Chestnut": ['#C04000', '#B87333', '#B22222', '#E97451', '#B7410E', '#FFD700', '#AA6C39', '#FD5E53', '#964F4C', '#FFBF00'],
        "Warm Almond": ['#D2B1A3', '#D2996E', '#8B5A2B', '#8B2500', '#A97142', '#A1866F', '#FFD700', '#C08A7C', '#955628', '#5C3317'],
        "Caramel": ['#A9746E', '#B26900', '#FFDDA0', '#CC7722', '#996515', '#7B3F00', '#D2B48C', '#DA9100', '#B65C35', '#FFC75F'],
        "Golden Bronze": ['#B87333', '#DAA520', '#AF6E4D', '#8A3324', '#A0522D', '#B8860B', '#E97451', '#7B3F00', '#A67B5B', '#FFA500']
    }
    return full_palettes.get(tone_name, ['#CCCCCC'])

if __name__ == '__main__':
    app.run(debug=True)
