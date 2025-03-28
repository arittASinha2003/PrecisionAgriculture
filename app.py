import string
import bcrypt
import os
from flask import Flask, redirect, render_template, url_for, request, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from datetime import datetime
import requests
import numpy as np
import pandas as pd
import config
import pickle
import io
import torch
from torchvision import transforms
from PIL import Image
from utils.model import ResNet9
from utils.fertilizer import fertilizer_dic
from utils.disease import disease_dic
import plotly.express as px
import matplotlib
matplotlib.use('Agg') # Set non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns

# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

# Loading crop recommendation model
# crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model_path = 'models/RandomForest_v2.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))

# Loading plant disease classification model

disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']

# disease prediction
disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()

def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None

def predict_image(img, model=disease_model):
    """
    Transforms image to tensor and predicts disease label
    :params: image
    :return: prediction (string)
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    # Get predictions from model
    yb = model(img_u)
    # Pick index with highest probability
    _, preds = torch.max(yb, dim=1)
    prediction = disease_classes[preds[0].item()]
    # Retrieve the class label
    return prediction

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = 'thisissecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class UserAdmin(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=5,max=20)],render_kw={"placeholder":"username"})
    password=PasswordField(validators=[InputRequired(),Length(min=5,max=20)],render_kw={"placeholder":"password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exist. please choose different one.")

class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=5,max=20)],render_kw={"placeholder":"username"})
    password=PasswordField(validators=[InputRequired(),Length(min=5,max=20)],render_kw={"placeholder":"password"})
    submit = SubmitField("Login")

class ContactUs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    text = db.Column(db.String(900), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        text = request.form['text']
        contacts = ContactUs(name=name, email=email, text=text)
        db.session.add(contacts)
        db.session.commit()
    return render_template("contact.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    elif form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template("login.html", form=form)

@ app.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    title = 'dashboard'
    return render_template('dashboard.html',title=title)

@ app.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))

@app.route("/signup",methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@ app.route('/crop-recommend')
@login_required
def crop_recommend():
    title = 'crop-recommend - Crop Recommendation'
    return render_template('crop.html', title=title)

@ app.route('/fertilizer')
@login_required
def fertilizer_recommendation():
    title = '- Fertilizer Suggestion'
    return render_template('fertilizer.html', title=title)

@app.route('/disease-predict', methods=['GET', 'POST'])
@login_required
def disease_prediction():
    title = '- Disease Detection'
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return render_template('disease.html', title=title)
        try:
            img = file.read()
            prediction = predict_image(img)

            # For demonstration, you can create a fake confidence score (in reality, use your model's prediction score)
            # disease = prediction  # The predicted disease
            # confidence = 0.85  # Example confidence score

            # fig, ax = plt.subplots()
            # sns.barplot(x=[disease], y=[confidence], ax=ax)
            # ax.set_title(f'Confidence of Disease: {disease}')
            # ax.set_xlabel('Disease')
            # ax.set_ylabel('Confidence (%)')

            # Convert the matplotlib figure to HTML
            # img_stream = io.BytesIO()
            # plt.savefig(img_stream, format='png')
            # img_stream.seek(0)
            # img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf8')
            # img_tag = f"data:image/png;base64,{img_base64}"

            # prediction = Markup(str(disease_dic[prediction])) #
            # return render_template('disease-result.html', prediction=disease, img_tag=img_tag, title=title)
            # return render_template('disease-result.html', prediction=prediction, img_tag=img_tag, title=title) #

            prediction = Markup(str(disease_dic[prediction]))
            return render_template('disease-result.html', prediction=prediction, title=title)
        except:
            pass
    return render_template('disease.html', title=title)

# ===============================================================================================

# RENDER PREDICTION PAGES
# render crop recommendation result page

@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = '- Crop Recommendation'
    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['potassium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        # state = request.form.get("stt")
        city = request.form.get("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]

            # Generate graph for crop suitability
            # crop = final_prediction  # The predicted crop
            # suitability = 90  # Example score for the crop

            # fig = px.bar(x=[crop], y=[suitability], title="Crop Suitability")
            # fig.update_layout(xaxis_title='Crop', yaxis_title='Suitability (%)')

            # Convert the Plotly figure to HTML
            # graph_html = fig.to_html(full_html=False)

            # return render_template('crop-result.html', prediction=final_prediction, graph_html=graph_html, title=title)

            return render_template('crop-result.html', prediction=final_prediction, title=title)
        else:
            return render_template('try_again.html', title=title)

# render fertilizer recommendation result page

@ app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = '- Fertilizer Suggestion'
    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['potassium'])
    pH = float(request.form['ph'])
    SM = int(request.form['sm'])

    df = pd.read_csv('Data/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]
    phr = df[df['Crop'] == crop_name]['pH'].iloc[0]
    smr = df[df['Crop'] == crop_name]['SM'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    ph = phr - pH
    sm = smr - SM

    # temp = {abs(n): "N", abs(p): "P", abs(k): "K", abs(ph): "pH"}
    temp = {"SM": abs(sm), "pH": abs(ph), "N": abs(n), "P": abs(p), "K": abs(k)}
    # max_value = temp[max(temp.keys())]
    max_value = max(temp, key=temp.get)

    if max_value == "N":
        key = "NHigh" if n < 0 else "NLow"
    elif max_value == "P":
        key = "PHigh" if p < 0 else "PLow"
    elif max_value == "K":
        key = "KHigh" if k < 0 else "KLow"
    elif max_value == "pH":
        key = "pHHigh" if ph < 0 else "pHLow"
    else:
        key = "SMHigh" if sm < 0 else "Balanced" if sm == 0 else "SMLow"

    response = Markup(str(fertilizer_dic[key]))

    # Bar graph for nutrient requirements
    fig, ax = plt.subplots()
    # ax.bar(['N', 'P', 'K', 'pH', 'SM'], [nr, pr, kr, phr, smr], color=['red', 'green', 'blue', 'orange', 'yellow'])
    # ax.set_title(f'Nutrient Requirements for {crop_name}')
    # ax.set_xlabel('Nutrients / Factors')
    # ax.set_ylabel('Required Value')

    # Define positions for the bars
    bar_width = 0.35  # Width of the bars
    index = ['N', 'P', 'K', 'pH', 'SM']  # Nutrient labels
    
    # Positioning for the required values and entered values
    bar_positions = range(len(index))
    required_values = [nr, pr, kr, phr, smr]  # Required values from the dataset
    entered_values = [N, P, K, pH, SM]  # Entered values from the form

    # Plot the bars for the required values
    ax.bar([pos - bar_width / 2 for pos in bar_positions], required_values, bar_width, label='Required', color='green')
    # Plot the bars for the entered values
    ax.bar([pos + bar_width / 2 for pos in bar_positions], entered_values, bar_width, label='Entered', color='yellow')

    # Set labels and title
    ax.set_title(f'Nutrient Requirements vs Entered Values for {crop_name}')
    ax.set_xlabel('Nutrients / Factors')
    ax.set_ylabel('Values')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(index)
    ax.legend()

    # Convert the matplotlib figure to HTML
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf8')
    img_tag = f"data:image/png;base64,{img_base64}"

    # return render_template('fertilizer-result.html', recommendation=response, title=title)
    return render_template('fertilizer-result.html', recommendation=response, img_tag=img_tag, title=title)

@app.route("/display")
def querydisplay():
    alltodo = ContactUs.query.all()
    return render_template("display.html",alltodo=alltodo)

@app.route("/AdminLogin", methods=['GET', 'POST'])
def AdminLogin():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('admindashboard'))
    elif form.validate_on_submit():
        user = UserAdmin.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for('admindashboard'))
    return render_template("adminlogin.html", form=form)
    # return render_template("adminlogin.html")

@app.route("/admindashboard")
@login_required
def admindashboard():
    alltodo = ContactUs.query.all()
    alluser = User.query.all()
    return render_template("admindashboard.html",alltodo=alltodo, alluser=alluser)

@app.route("/reg",methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = UserAdmin(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('AdminLogin'))
    return render_template("reg.html", form=form)

if __name__ == "__main__":
    # app.run(debug=True,port=8000)
    # app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    app.run(debug=True,port=int(os.environ.get("PORT", 10000)))
