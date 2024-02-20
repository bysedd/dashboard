import streamlit as st


def set_page():
    st.set_page_config(page_title="Teams", page_icon="⚽", layout="wide")


def select_club(df_data):
    club = st.sidebar.selectbox("Select a club", df_data["club"].unique())
    club_df = df_data[df_data["club"] == club]
    return club_df


def display_club_info(club_df):
    st.image(club_df["club logo"].iloc[0], width=50)
    st.subheader(club_df["club"].iloc[0])


def display_club_stats(club_df):
    club_df.rename(
        lambda x: str(x).title(), axis="columns", inplace=True
    )  # rename columns to title case

    # format the value columns
    for value_column in ["Value(£)", "Release Clause(£)"]:
        club_df[value_column] = club_df[value_column].apply(
            lambda x: f"£ {int(x):,.0f}"
        )

    st.dataframe(
        club_df[
            [
                "Name",
                "Age",
                "Photo",
                "Flag",
                "Value(£)",
                "Wage(£)",
                "Joined",
                "Height(Cm.)",
                "Weight(Lbs.)",
                "Contract Valid Until",
                "Release Clause(£)",
            ]
        ],
        hide_index=True,
        column_config={
            "Overall": st.column_config.ProgressColumn(
                "Overall", format="%d", min_value=0, max_value=100
            ),
            "Photo": st.column_config.ImageColumn(),
            "Flag": st.column_config.ImageColumn("Country", width="small"),
            "Value(£)": st.column_config.Column(
                "Market Value", help="Market value of the player"
            ),
            "Wage(£)": st.column_config.ProgressColumn(
                "Weekly Wage",
                format="£ %d",
                min_value=0,
                max_value=club_df["Wage(£)"].max(),
                width="medium",
            ),
            "Joined": st.column_config.DateColumn(
                "Joined",
                format="MM/DD/YYYY",
                help="Date that the player joined the club",
            ),
            "Contract Valid Until": st.column_config.NumberColumn(
                "Contract Valid Until",
                format="%d",
                help="Contract valid until year end",
            ),
            "Release Clause(£)": st.column_config.Column("Release Clause"),
            "Height(Cm.)": st.column_config.NumberColumn(
                "Height", format="%d", help="Height in centimeters"
            ),
            "Weight(Lbs.)": st.column_config.NumberColumn(
                "Weight", format="%d", help="Weight in pounds"
            ),
        },
        use_container_width=True,
    )


def main():
    set_page()
    df_data = st.session_state["df_data"]
    club_df = select_club(df_data)
    display_club_info(club_df)
    display_club_stats(club_df)


if __name__ == "__main__":
    try:
        main()
    except KeyError:
        st.error("Please go to the **🏠 Home** first. Then back to this page.")
