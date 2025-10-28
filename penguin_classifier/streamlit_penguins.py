import streamlit as st
import pickle
import pandas as pd

# === Streamlit Page Configuration ===
st.set_page_config(
    page_title="Penguin Species Classifier",
    page_icon=":penguin:",
    layout="wide"
)

# === Load Trained Model and Label Mapping ===
with open("rfc_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_uniques.pkl", "rb") as f:
    output_uniques_map = pickle.load(f)

# === Load and Prepare the Dataset for Reference ===
# Used to retrieve category options and the correct feature structure
df = pd.read_csv("penguins_raw.csv", usecols=[2, 4, 9, 10, 11, 12, 13])
df['Species'] = df['Species'].str.replace(r"\s*\(.*?\)", "", regex=True)
df.dropna(inplace=True)

# Keep only features and apply one-hot encoding
original_features = df.iloc[:, 1:]
original_features = pd.get_dummies(original_features)

# === Sidebar Navigation ===
with st.sidebar:
    st.title("Select a page")
    page = st.selectbox("Choose page", ["Introduction", "Prediction"])

# === Page 1: Introduction ===
if page == "Introduction":
    st.header("Introduction")
    st.markdown("""
The **Palmer Penguins** dataset contains biological measurements of three penguin species — **Adelie**, **Chinstrap**, and **Gentoo** — observed on the Palmer Archipelago in Antarctica.

This application uses a **Random Forest Classifier** trained on this dataset to predict the species of a penguin based on these attributes:

- **Species** – Penguin species (Adelie, Chinstrap, or Gentoo)  
- **Island** – Island where the penguin was observed (Biscoe, Dream, or Torgersen)  
- **Sex** – Biological sex of the penguin (Male or Female)  
- **Culmen Length (mm)** – Length of the penguin’s bill  
- **Culmen Depth (mm)** – Depth (height) of the penguin’s bill  
- **Flipper Length (mm)** – Length of the penguin’s flippers  
- **Body Mass (g)** – Body weight in grams  

The Random Forest model combines multiple decision trees to improve prediction accuracy and reduce overfitting, making it an effective and robust tool for biological classification.
    """)

# === Page 2: Prediction Form ===
elif page == "Prediction":
    st.header("Penguin Species Classifier")
    st.markdown("""
This web application uses a model trained with the Palmer Penguins dataset.
By entering six characteristics, you can predict the species of a penguin.
Fill in the form below to get started!
    """)

    # === User Input Form ===
    with st.form("User_inputs"):
        # Selectboxes with non-empty labels
        island = st.selectbox(
            "Penguin-inhabited island",
            options=df['Island'].unique().tolist()
        )
        sex = st.selectbox(
            "Penguin’s sex",
            options=df['Sex'].unique().tolist()
        )

        # Number inputs with hidden labels (prevents accessibility warnings)
        culmen_length = st.number_input(
            "Culmen Length (mm)",
            min_value=0.0,
            label_visibility="hidden"
        )
        culmen_depth = st.number_input(
            "Culmen Depth (mm)",
            min_value=0.0,
            label_visibility="hidden"
        )
        flipper_length = st.number_input(
            "Flipper Length (mm)",
            min_value=0.0,
            label_visibility="hidden"
        )
        body_mass = st.number_input(
            "Body Mass (g)",
            min_value=0.0,
            label_visibility="hidden"
        )

        submit = st.form_submit_button("Predict Penguin Species")

        # === Prediction Logic ===
        if submit:
            # Create DataFrame for user input and align with training features
            user_input = pd.DataFrame([{
                "Island": island,
                "Culmen Length (mm)": culmen_length,
                "Culmen Depth (mm)": culmen_depth,
                "Flipper Length (mm)": flipper_length,
                "Body Mass (g)": body_mass,
                "Sex": sex
            }])
            user_features = pd.get_dummies(user_input)
            user_features = user_features.reindex(columns=original_features.columns, fill_value=0)

            # Predict species using the trained model
            pred_code = model.predict(user_features)[0]
            pred_species = output_uniques_map[pred_code]
            st.success(f"Prediction: {pred_species}")
