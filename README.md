# Precision Agriculture using Machine Learning

## Data Source 📊

- [Crop Recommendation Dataset](https://www.kaggle.com/atharvaingle/crop-recommendation-dataset) (Custom-built Dataset)
- [Fertilizer Suggestion Dataset](https://github.com/Gladiator07/Harvestify/blob/master/Data-processed/fertilizer.csv) (Custom-built Dataset)
- [Disease Detection Dataset](https://www.kaggle.com/vipoooool/new-plant-diseases-dataset)

## Motivation 💪

Farming is one of the major sectors that influences a country’s economic growth.

- In a country like India, most of the population depends on agriculture for their livelihood. Many new technologies, such as machine learning and deep learning, are being implemented in agriculture to make it easier for farmers to grow and maximize their yield.

- In this project, I present a website on which the following applications are implemented: Crop recommendation, fertilizer recommendation, and plant disease prediction, respectively.

- In the crop recommendation application, the user can provide the soil data from their side, and the application will predict which crop the user should grow.

- For the fertilizer recommendation application, the user can input the soil data and the type of crop they are growing, and the application will predict what the soil lacks or has an excess of and recommend improvements.

- For the last application, the plant disease prediction application, the user can input an image of a diseased plant leaf, and the application will predict what disease it is. It will also provide some background and suggestions for curing the disease.

## Home Page of our Web Application

![Home Page of our Web Application](https://github.com/arittASinha2003/PrecisionAgriculture/blob/main/Project-docs/App%20Snaps/Home.png)

## How to Use 💻

- Crop Recommendation System ==> Enter the corresponding nutrient values of your soil, state, and city. Note that the N-P-K (Nitrogen-Phosphorous-Pottasium) values to be entered should be the ratio between them. Refer to this website for more information. Note: When you enter the city name, make sure to enter common city names. Remote cities/towns may not be available in the Weather API from where humidity and temperature data is fetched.

- Fertilizer Suggestion System ==> Enter the nutrient contents of your soil and the crop you want to grow. The algorithm will tell which nutrient the soil has an excess of or lacks. Accordingly, it will give suggestions for buying fertilizers.

- Disease Detection System ==> Upload an image of a leaf of your plant. The algorithm will tell the crop type and whether it is diseased or healthy. If it is diseased, it will tell you the cause of the disease and suggest how to prevent/cure it accordingly. Note that, for now, it only supports a few crops.

## Requirements

To run this project locally, you need the following tools and libraries:

- **Python 3.11 (or lower)** ([Python 3.11.9](https://www.python.org/downloads/release/python-3119/) preferred)
- Necessary Python libraries listed in the `requirements.txt` file.
- Download these additional files (optional) after cloning the repository by following the folder structure given at the bottom:
    - `plant_disease_model.pth`: (Plant Disease Model to be placed inside `models` folder) [Download Link](https://drive.google.com/file/d/1suOVoZSw5yaDwKZqNe3XxwTklQrXYyBG/view?usp=sharing) (❌ Not Required ❌)
    - `New Plant Diseases Dataset(Augmented)` folder: (Plant Disease Dataset to be placed inside `Data` folder) [Download Link](https://drive.google.com/drive/folders/1MaPU1utHu3E6CMo6c09qdDma4ueQ15mz?usp=sharing) (❗Only required if you want to retrain the model❗)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/arittASinha2003/PrecisionAgriculture.git
```
```bash
cd PrecisionAgriculture
```

### 2. Creating Virtual Environment (Recommended, but Optional)
```bash
python -m venv myenv
```
```bash
myenv/Scripts/activate
```
**❗Note:** If you have more than one Python version installed on your system (check using the `where python` command), you should first check the current version of Python running before creating a virtual environment (check using the `python --version` command). If it is not running Python 3.11.9, do the following:

- Go to the file path as seen while executing the `where python` command for Python 3.11.9 version (it will be as C:\Program Files\Python311), right-click on the `python.exe` file and click on the `Copy as path` option.
- Then, execute the following command to create a virtual environment using the Python 3.11.9 version.
```bash
"C:\Program Files\Python311\python.exe" -m venv myenv
```
```bash
myenv/Scripts/activate
```
or, for Powershell:
```bash
& "C:\Program Files\Python311\python.exe" -m venv myenv
```
```bash
myenv/Scripts/activate
```

### 3. Install Dependencies
First, ensure you have Python 3.x installed. Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
To start the application, run the following command:
```bash
python app.py
```

## Folder Structure

```bash
.
└── PrecisionAgriculture/
    ├── Data/
    │   ├── New Plant Diseases Dataset(Augmented)/
    │   │   ├── train/
    │   │   │   └── 38 folders
    │   │   └── valid/
    │   │       └── 38 folders
    │   ├── test/
    │   │   └── 33 images
    │   ├── Crop_recommendation.csv
    │   └── fertilizer.csv
    ├── models/
    │   ├── plant_disease_model.pth
    │   ├── plant_disease_model_v2.pth (optional)
    │   ├── RandomForest.pkl (optional)
    │   └── RandomForest_v2.pkl
    ├── Project-docs/
    │   └── System-Architecture-final.jpg, App-snaps, etc.
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   ├── images/
    │   │   └── 12 images
    │   └── scripts/
    │       └── cities.js
    ├── templates/
    │   ├── aboutus.html
    │   ├── admindashboard.html
    │   ├── adminlogin.html
    │   ├── base.html
    │   ├── contact.html
    │   ├── crop.html
    │   ├── crop-result.html
    │   ├── dashboard.html
    │   ├── disease.html
    │   ├── disease-result.html
    │   ├── fertilizer.html
    │   ├── fertilizer-result.html
    │   ├── index.html
    │   ├── login.html
    │   ├── reg.html
    │   ├── signup.html
    │   └── try_again.html
    ├── utils/
    │   ├── disease.py
    │   ├── fertilizer.py
    │   └── model.py
    ├── .gitignore
    ├── app.py
    ├── config.py
    ├── Credentials.txt
    ├── database.db
    ├── Procfile
    ├── README.md
    ├── requirements.txt
    ├── Train_Crop.py
    ├── Train_Disease.py
    └── View_Crop.py
```

## Acknowledgements

1. **[Tree](https://tree.nathanfriend.com/)**: For generating ASCII folder structure diagrams.
2. **[Readme.so](https://readme.so/)**: For generating the README file.
3. **[GitHub Reference](https://github.com/atharval1/precision-agriculture-using-machine-learning)**
