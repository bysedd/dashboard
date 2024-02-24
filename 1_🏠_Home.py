import re

import numpy as np
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
def load_data(*, file_csv: str) -> pd.DataFrame:
    data = pd.read_csv(file_csv, index_col=0)
    data = data[data["Value(£)"] > 0]
    data.sort_values(by="Overall", ascending=False, inplace=True)

    data["Name"] = data["Name"].apply(lambda x: re.sub(r"\d+", "", x).strip())
    data["Weight(Kg.)"] = data["Weight(lbs.)"].apply(lambda x: x * 0.453592)
    data["Height(m.)"] = data["Height(cm.)"].apply(lambda x: x / 100)

    fifa22 = pd.read_csv("resources/CLEAN_FIFA22_official_data.csv", index_col=0)
    fifa22["Name"] = fifa22["Name"].apply(lambda x: re.sub(r"\d+", "", x).strip())

    for value_column in ["Value(£)", "Wage(£)", "Release Clause(£)"]:
        data = data.merge(
            fifa22[["Name", value_column]],
            on="Name",
            how="left",
            suffixes=("", "_fifa22"),
        )
        data[f"Previous {value_column}"] = (
            data[value_column] - data[f"{value_column}_fifa22"]
        )
        data.drop(columns=[f"{value_column}_fifa22"], inplace=True)

    # Remove jogadores com nomes duplicados
    data.drop_duplicates(subset="Name", keep="first", inplace=True)

    return data


@st.cache_data
def get_clubs(df_data: pd.DataFrame) -> np.ndarray:
    return df_data["Club"].unique()


st.session_state["fifa23"] = load_data(
    file_csv="resources/CLEAN_FIFA23_official_data.csv"
)
st.session_state["clubs"] = get_clubs(st.session_state["fifa23"])

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
        data=st.session_state["fifa23"].reset_index().to_csv(),
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
