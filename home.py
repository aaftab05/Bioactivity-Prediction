# Import necessary libraries
import streamlit as st
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle
import firebase_admin
from firebase_admin import credentials, auth
import matplotlib.pyplot as plt  # Not used in this version, but might be needed for future visualizations
from rdkit import Chem
from rdkit.Chem import Draw

from chembl_webresource_client.new_client import new_client


# Function to check user login (replace with your actual authentication logic)
def check_login():
    try:
        # Assuming you're storing the user ID or token in session_state after successful login
        user = auth.get_user(st.session_state.user_id)
        return True
    except:
        return False


# Function to calculate molecular descriptors using PaDEL
def desc_calc():
    bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove('molecule.smi')


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Function to build the prediction model and display results
def build_model(input_data, load_data):
    try:
        load_model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
        prediction = load_model.predict(input_data)

        prediction_output = pd.Series(prediction, name='pIC50')
        molecule_name = pd.Series(load_data[1], name='molecule_name')
        df = pd.concat([molecule_name, prediction_output], axis=1)

        # Rank molecules by predicted activity
        df['Activity Rank'] = df['pIC50'].rank(ascending=False)
        df['Activity Level'] = pd.cut(df['Activity Rank'], bins=3, labels=['High', 'Medium', 'Low'])

        st.header('**Top Predicted Molecules**')

        top_candidates = df.head(5)

        # Display the table with color grading FIRST
        st.subheader("**Predicted Activities and Rankings**")
        def color_activity(val):
            if val <= len(df) * 0.33:
                color = 'green'
            elif val <= len(df) * 0.66:
                color = 'orange'
            else:
                color = 'red'
            return f'background-color: {color}'

        styled_df = df[['molecule_name', 'pIC50', 'Activity Rank']].style.applymap(color_activity, subset=['Activity Rank'])
        st.dataframe(styled_df)
        st.markdown(filedownload(df), unsafe_allow_html=True) #Download button

        molecule_client = new_client.molecule
        st.subheader("**Molecular Structures**")
        for index, row in top_candidates.iterrows():
            st.write(f"Molecule: {row['molecule_name']}")
            st.write(f"Predicted Activity Level: **{row['Activity Level']}**")

            # Get SMILES from ChEMBL ID and display molecule structure
            try:
                molecule = molecule_client.get(row['molecule_name'])
                if molecule and 'molecule_structures' in molecule and molecule['molecule_structures'] and 'canonical_smiles' in molecule['molecule_structures']:
                    canonical_smiles = molecule['molecule_structures']['canonical_smiles']
                    if canonical_smiles:
                        mol = Chem.MolFromSmiles(canonical_smiles)
                        if mol is not None:
                            img = Draw.MolToImage(mol, size=(300, 300))
                            st.image(img, use_column_width=False)
                        else:
                            st.write("Could not generate molecule from SMILES.")
                    else:
                        st.write("SMILES not available for this ChEMBL ID.")
                else:
                    st.write(f"Molecule with ChEMBL ID {row['molecule_name']} not found or does not contain structure information.")
            except Exception as e:
                st.write(f"Error retrieving or drawing molecule: {e}")

            st.write("---")

        st.markdown("""
        **Explanation:** This project uses a computational model to predict the potential of molecules to inhibit Acetylcholinesterase, a key target in Alzheimer's disease. The molecules shown above are predicted to have the highest activity levels, making them promising candidates for further research. A higher predicted activity suggests a greater potential to block the enzyme, which could lead to more effective treatments for Alzheimer's.
        """)
    except FileNotFoundError:
        st.error("Error: Model file 'acetylcholinesterase_model.pkl' not found.")
    except Exception as e:
        st.error(f"An error occurred during model prediction: {e}")

# Main app function
def app():
    # Logo image
    image = Image.open('logo.png')
    st.image(image, use_column_width=True)

    # Page title
    st.markdown("""
    # Bioactivity Prediction App (Acetylcholinesterase)

    This app allows you to predict the bioactivity towards inhibiting the `Acetylcholinesterase` enzyme. `Acetylcholinesterase` is a drug target for Alzheimer's disease.

    **Credits**
    - Descriptor calculated using [PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/) [[Read the Paper]](https://doi.org/10.1002/jcc.21707).
    ---
    """)

    # Sidebar
    with st.sidebar.header('1. Upload your CSV data'):
        uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
        st.sidebar.markdown("""
        [Example input file](https://raw.githubusercontent.com/dataprofessor/bioactivity-prediction-app/main/example_acetylcholinesterase.txt)
        """)

    if st.sidebar.button('Predict'):
        load_data = pd.read_table(uploaded_file, sep=' ', header=None)
        load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)
        
        st.header('**Original input data**')
        st.write(load_data)
        
        with st.spinner("Calculating descriptors..."):
            desc_calc()

        # Read in calculated descriptors and display the dataframe
        st.header('**Calculated molecular descriptors**')
        desc = pd.read_csv('descriptors_output.csv')
        st.write(desc)
        st.write(desc.shape)

        # Read descriptor list used in previously built model
        st.header('**Subset of descriptors from previously built models**')
        Xlist = list(pd.read_csv('descriptor_list.csv').columns)
        desc_subset = desc[Xlist]
        st.write(desc_subset)
        st.write(desc_subset.shape)

        # Apply trained model to make prediction on query compounds
        build_model(desc_subset,load_data)
    
    else:
        st.info('Please log in to access the prediction app. Login in the sidebar!')
