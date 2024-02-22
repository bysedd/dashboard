import re
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="centered",
    menu_items={
        "Report a bug": "https://github.com/bysedd/FIFA-23/issues/new",
        "About": "FIFA23 OFFICIAL DATASET CLEAN FROM 2023",
    },
)


@st.cache_data
def load_data(*, file_csv: str, num_rows: None = None) -> pd.DataFrame:
    data = pd.read_csv(file_csv, nrows=num_rows, index_col=0)
    data = data[data["Value(£)"] > 0]
    data.sort_values(by="Overall", ascending=False, inplace=True)
    data.rename(lambda x: str(x).lower(), axis="columns", inplace=True)

    data["name"] = data["name"].apply(lambda x: re.sub(r"\d+", "", x).strip())
    data["Weight(Kg.)"] = data["weight(lbs.)"].apply(lambda x: x * 0.453592)
    data["Height(m.)"] = data["height(cm.)"].apply(lambda x: x / 100)

    return data


st.session_state["df_data"] = load_data(
    file_csv="resources/CLEAN_FIFA23_official_data.csv"
)

st.title("FIFA23 Official Dataset")
col1, col2, *_ = st.columns(4)
with col1:
    st.link_button(
        label="Access data",
        url="https://www.kaggle.com/datasets/kevwesophia/fifa23-official-datasetclean-data",
    )
with col2:
    st.download_button(
        label="Download data",
        data=st.session_state["df_data"].reset_index().to_csv(),
        file_name="CLEAN_FIFA23_official_data.csv",
    )
st.markdown(
    """
    ## About this dataset
    The Football Player Dataset from 2017 to 2023 provides comprehensive information about professional
    football players. The dataset contains a wide range of attributes, including player demographics,
    physical characteristics, playing statistics, contract details, and club affiliations.\n
    With over 17,000 records, this dataset offers a valuable resource for football analysts, researchers,
    and enthusiasts interested in exploring various aspects of the footballing world,
    as it allows for studying player attributes, performance metrics, market valuation, club analysis,
    player positioning, and player development over time.
    """
)
st.sidebar.caption("Made with ❤️ by [Felippe A.](https://linkedin.com/in/bysedd/)")
st.sidebar.caption("Check the code on [GitHub](https://github.com/bysedd/FIFA-23/)")
