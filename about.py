import streamlit as st

import streamlit as st

def app():
    st.title("About This App")

    with st.expander("About Alzheimer's Disease"):
        st.write("""
            Alzheimer's disease is a progressive brain disease that gradually destroys memory and thinking skills, and eventually the ability to carry out the simplest tasks. It's the most common cause of dementia among older adults. 

            **Impact:**
            *   Millions of people worldwide are affected by Alzheimer's.
            *   It has a significant impact on individuals, families, and healthcare systems.

            **The Need for New Treatments:**
            Current treatments can only manage symptoms to a limited extent. There is a critical need for new and more effective therapies that can slow down or prevent the progression of the disease.
        """)

    with st.expander("How This App Works (Simplified)"):
        st.write("""
            This app uses a computational approach to predict the potential of different molecules to inhibit Acetylcholinesterase, an enzyme that plays a key role in Alzheimer's disease. Think of it like a virtual screening process:

            1.  **Input:** You provide a list of molecules (ChEMBL IDs).
            2.  **Calculations:** The app calculates various properties of these molecules (descriptors).
            3.  **Prediction:** A trained machine learning model uses these properties to predict how strongly each molecule might inhibit the target enzyme.
            4.  **Output:** The app displays the top predicted molecules, along with their predicted activity levels and visualizations of their structures.

            This process helps researchers identify promising drug candidates more efficiently, reducing the time and cost associated with traditional laboratory experiments.
        """)

    with st.expander("About the Model"):
        st.write("""
            The predictions in this app are generated using a machine learning model trained on a dataset of known molecules and their experimentally determined activities against Acetylcholinesterase. This model learns the relationships between molecular properties and activity, allowing it to predict the activity of new molecules.
        """)

    with st.expander("Credits and Acknowledgements"):
        st.write("""
            This app utilizes the following tools and resources:

            *   **PaDEL-Descriptor:** For calculating molecular descriptors.
            *   **ChEMBL Database:** For retrieving molecular information and structures.
            *   **RDKit:** For molecular visualization.
            *   **Streamlit:** For building the web application.

            We acknowledge the contributions of the researchers and developers who created these valuable resources.
        """)

    

    #st.subheader("Video explaining the project")
    #video_file = open('Alzheimer.mp4', 'rb')
    #video_bytes = video_file.read()
    #st.video(video_bytes)


    