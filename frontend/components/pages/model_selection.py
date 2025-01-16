import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header("Model Selection Helper", "Pick the right machine learning approach")

    if "auth_token" not in st.session_state:
        st.warning("You need to log in to view model selection help.")
        show_footer()
        return

    st.markdown(
        """
    ## Overview of ML Approaches

    **1) Supervised Learning**
       - **Regression**: Predict continuous numerical values (e.g., house price).
       - **Classification**: Predict discrete labels (e.g., spam/not spam).

    **2) Unsupervised Learning**
       - **Clustering**: Group data points into clusters (e.g., K-means).
       - **Dimensionality Reduction**: e.g., PCA for feature compression.

    **3) Deep Learning**
       - Neural networks for complex tasks (images, text, sequential data).
       - Typically requires more data and more computational resources.

    ---
    """
    )

    st.markdown(
        """
    ### Which category is right for my dataset?
    1. **If you have a target column with continuous values (like prices, amounts, or measurements),** consider a **Regression** algorithm.
    2. **If you have a target column with discrete categories (e.g. 'Yes/No', 'Dog/Cat/Horse'),** consider a **Classification** algorithm.
    3. **If you want to segment or discover hidden groupings in your data without any labeled target,** try **Unsupervised** approaches (e.g. clustering).
    4. **If your dataset is large, or you have images, text, or a problem that might need advanced feature extraction,** you can explore **Deep Learning**.

    ---
    """
    )

    st.info(
        "This page is just a guide. Once you know what approach you need, head over to **Train Model** in the navigation sidebar to apply your choice."
    )

    st.subheader("Quick Wizard")
    st.write("Answer a few quick questions to get a recommendation.")

    data_has_label = st.selectbox("Do you have a labeled target column?", ["Yes", "No"])
    if data_has_label == "Yes":
        label_type = st.selectbox(
            "Is the label numeric or categorical?", ["Numeric", "Categorical"]
        )
        if label_type == "Numeric":
            st.success("Recommended: **Regression** (Supervised).")
        else:
            st.success("Recommended: **Classification** (Supervised).")
    else:
        st.success("Recommended: **Unsupervised** approach (e.g., Clustering).")

    st.write("---")
    st.write(
        "Deep learning could be used in all above scenarios if the dataset is large/complex, but typically you start with classical algorithms first."
    )
    show_footer()
