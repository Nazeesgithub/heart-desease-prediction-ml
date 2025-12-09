import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Try to locate the model in a few likely locations (so app works from different cwd)
APP_DIR = Path(__file__).resolve().parent
MODEL_NAME = "best_xgb_heart_model.joblib"
candidate_paths = [
    APP_DIR / "models" / MODEL_NAME,
    APP_DIR.parent / "notebooks" / "models" / MODEL_NAME,
    APP_DIR / ".." / "notebooks" / "models" / MODEL_NAME,
]

model = None
found_path = None
for p in candidate_paths:
    p = p.resolve()
    if p.exists():
        try:
            model = joblib.load(p)
            found_path = p
            break
        except Exception as e:
            st.warning(f"Found model file at {p!s} but failed to load: {e}")

if model is None:
    # If not found, show helpful error in the Streamlit app instead of crashing
    st.title("Heart Disease Risk Predictor")
    st.error(
        "Model file not found. Expected one of: {}.\nPlease copy the model file '{}' into the app 'models/' folder or update the path.".format(
            ", ".join(str(p.resolve()) for p in candidate_paths), MODEL_NAME
        )
    )
    st.stop()

st.title("Heart Disease Risk Predictor")
st.write("Enter patient details:")

# Provide a quick reference so users understand each field and choices
with st.expander("Field descriptions / help (click to expand)"):
    st.write(
        """
        - **Age**: Patient age in years.
        - **Sex**: Male or Female.
        - **Chest pain type**: Typical/atypical/non-anginal/asymptomatic chest pain.
        - **Resting blood pressure (trestbps)**: in mm Hg.
        - **Cholesterol (chol)**: serum cholesterol in mg/dl.
        - **Fasting blood sugar (fbs)**: whether > 120 mg/dl.
        - **Resting ECG (restecg)**: 0 = normal, 1 = ST-T abnormality, 2 = LVH.
        - **Max heart rate achieved (thalach)**: peak heart rate during exercise.
        - **Exercise induced angina (exang)**: whether exercise causes angina.
        - **ST depression (oldpeak)**: depression induced by exercise relative to rest.
        - **ST slope**: slope of the peak exercise ST segment.
        - **Number of major vessels (ca)**: 0-3 colored by fluoroscopy.
        - **Thalassemia (thal)**: 1 = normal, 2 = fixed defect, 3 = reversible defect.
        """
    )

# Example inputs — adapt to your columns
age = st.number_input("Age", 1, 120, 50, help="Patient age in years (integer)")

# Friendly choices mapped to model-expected numeric values
sex_map = {"Female": 0, "Male": 1}
sex_label = st.selectbox("Sex", list(sex_map.keys()), help="Biological sex: Male or Female")

cp_map = {
    "Typical angina (0)": 0,
    "Atypical angina (1)": 1,
    "Non-anginal pain (2)": 2,
    "Asymptomatic (3)": 3,
}
cp_label = st.selectbox("Chest pain type", list(cp_map.keys()), help="Type of chest pain experienced; affects risk profile")

trestbps = st.number_input("Resting blood pressure (mm Hg)", 50, 250, 120, help="Resting arterial blood pressure in mm Hg")
chol = st.number_input("Serum cholesterol (mg/dl)", 100, 600, 200, help="Total serum cholesterol in mg/dl")

fbs_map = {"<= 120 mg/dl (No)": 0, "> 120 mg/dl (Yes)": 1}
fbs_label = st.selectbox("Fasting blood sugar (fasting > 120 mg/dl)?", list(fbs_map.keys()), help="Indicates if fasting blood sugar is greater than 120 mg/dl")

restecg_map = {"Normal (0)": 0, "ST-T wave abnormality (1)": 1, "Left ventricular hypertrophy (2)": 2}
restecg_label = st.selectbox("Resting ECG", list(restecg_map.keys()), help="Resting electrocardiographic results (0,1,2)")

thalach = st.number_input("Max heart rate achieved", 60, 220, 150, help="Maximum heart rate achieved during exercise")

exang_map = {"No": 0, "Yes": 1}
exang_label = st.selectbox("Exercise induced angina", list(exang_map.keys()), help="Whether exercise induced chest pain (angina)")

oldpeak = st.number_input("ST depression induced by exercise relative to rest", 0.0, 10.0, 1.0, help="ST depression value (numeric), higher values may indicate ischemia")

slope_map = {"Upsloping (0)": 0, "Flat (1)": 1, "Downsloping (2)": 2}
slope_label = st.selectbox("ST segment slope", list(slope_map.keys()), help="Slope of the ST segment during peak exercise")

ca_map = {"0 (no major vessels)": 0, "1": 1, "2": 2, "3": 3}
ca_label = st.selectbox("Number of major vessels (0-3)", list(ca_map.keys()), help="Number of major vessels colored by fluoroscopy (0-3)")

thal_map = {"Normal (1)": 1, "Fixed defect (2)": 2, "Reversible defect (3)": 3}
thal_label = st.selectbox("Thalassemia status", list(thal_map.keys()), help="Thalassemia: 1=normal, 2=fixed defect, 3=reversible defect")

input_df = pd.DataFrame([{
    'age': age,
    'sex': sex_map[sex_label],
    'cp': cp_map[cp_label],
    'trestbps': trestbps,
    'chol': chol,
    'fbs': fbs_map[fbs_label],
    'restecg': restecg_map[restecg_label],
    'thalach': thalach,
    'exang': exang_map[exang_label],
    'oldpeak': oldpeak,
    'slope': slope_map[slope_label],
    'ca': ca_map[ca_label],
    'thal': thal_map[thal_label]
}])
try:
    import joblib
except ImportError:
    raise RuntimeError("Missing dependency: run `pip install joblib` in the app virtualenv")

if st.button("Predict"):
    proba = model.predict_proba(input_df)[:,1][0]
    st.write(f"Predicted probability of heart disease: {proba:.3f}")
    label = "HIGH RISK" if proba > 0.5 else "LOW RISK"
    st.markdown(f"### Risk: **{label}**")
