# Precision Agriculture using Machine Learning and IOT

## Data Source 📊

- [Crop Recommendation Dataset](https://www.kaggle.com/atharvaingle/crop-recommendation-dataset) (Custom-built Dataset)
- [Fertilizer Suggestion Dataset](https://github.com/Gladiator07/Harvestify/blob/master/Data-processed/fertilizer.csv) (Custom-built Dataset)
- [Disease Detection Dataset](https://www.kaggle.com/vipoooool/new-plant-diseases-dataset)

## Motivation 💪

Farming is one of the major sectors that influences a country’s economic growth.

- In country like India, majority of the population is dependent on agriculture for their livelihood. Many new technologies, such as Machine Learning and Deep Learning, are being implemented into agriculture so that it is easier for farmers to grow and maximize their yield.

- In this project, I present a website in which the following applications are implemented; Crop recommendation, Fertilizer recommendation and Plant disease prediction, respectively.

- In the crop recommendation application, the user can provide the soil data from their side and the application will predict which crop should the user grow.

- For the fertilizer recommendation application, the user can input the soil data and the type of crop they are growing, and the application will predict what the soil lacks or has excess of and will recommend improvements.

- For the last application, that is the plant disease prediction application, the user can input an image of a diseased plant leaf, and the application will predict what disease it is and will also give a little background about the disease and suggestions to cure it.

## Contributors

- [Atharva Labhasetwar](https://www.linkedin.com/in/atharva-labhasetwar)

- [Venkata Narayana Bommanaboina](https://www.linkedin.com/in/bvnarayana515739/)

- [Kundan Patil](https://www.linkedin.com/in/kundan-patil-638979199)

- [GitHub Reference](https://github.com/atharval1/precision-agriculture-using-machine-learning)

## Home Page of our Web Application

![Home Page of our Web Application](https://github.com/atharval1/precision-agriculture-using-machine-learning/blob/main/Project-docs/App-snaps/Home.png)

## How to Use 💻

- Crop Recommendation System ==> Enter the corresponding nutrient values of your soil, state and city. Note that, the N-P-K (Nitrogen-Phosphorous-Pottasium) values to be entered should be the ratio between them. Refer this website for more information. Note: When you enter the city name, make sure to enter mostly common city names. Remote cities/towns may not be available in the Weather API from where humidity, temperature data is fetched.

- Fertilizer Suggestion System ==> Enter the nutrient contents of your soil and the crop you want to grow. The algorithm will tell which nutrient the soil has excess of or lacks. Accordingly, it will give suggestions for buying fertilizers.

- Disease Detection System ==> Upload an image of leaf of your plant. The algorithm will tell the crop type and whether it is diseased or healthy. If it is diseased, it will tell you the cause of the disease and suggest you how to prevent/cure the disease accordingly. Note that, for now it only supports few crops.

## How to Run the Project

- [Demo](https://youtu.be/kU0nf-rzusE)
- [Walkthrough](https://youtu.be/eJ-KytG2H5w)

## Requirements

To run this project locally, you need the following tools and libraries:

- **Python 3.11 (or lower)** ([Python 3.11.9](https://www.python.org/downloads/release/python-3119/) preferred)
- Necessary Python libraries listed in the `requirements.txt` file.
- Download these additional files after cloning the repository by following the folder structure given at the bottom:
    - `plant_disease_model.pth`: (Plant Disease Model to be placed inside `models` folder) [Download Link](https://drive.google.com/file/d/1suOVoZSw5yaDwKZqNe3XxwTklQrXYyBG/view?usp=sharing)
    - `New Plant Diseases Dataset(Augmented)` folder: (Plant Disease Dataset to be placed inside `Data` folder) [Download Link](https://drive.google.com/drive/folders/1MaPU1utHu3E6CMo6c09qdDma4ueQ15mz?usp=sharing)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/arittASinha2003/PrecisionAgriculture.git
cd PrecisionAgriculture
```

### 2. Creating Virtual Environment (Recommended, but Optional)
```bash
python -m venv myenv
myenv/Scripts/activate
```
**❗Note:** If you have more than one Python version installed on your system (check using `where python` command), you should first check the current version of Python runnning before creating virtual environment (check using `python --version` command). If it is not running Python 3.11.9, do the following:

- Go to the file path as seen while executing `where python` command for Python 3.11.9 version (it will be as C:\Program Files\Python311), right click on `python.exe` file, and click on `Copy as path` option.
- Then, execute the following command to create virtual environment using Python 3.11.9 version.
```bash
"C:\Program Files\Python311\python.exe" -m venv myenv
myenv/Scripts/activate
```
or, for Powershell:
```bash
& "C:\Program Files\Python311\python.exe" -m venv myenv
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

1. **Tree**: For generating ASCII folder structure diagrams. [Link](https://tree.nathanfriend.com/)
2. **Readme.so**: For generating the README file. [Link](https://readme.so/)
