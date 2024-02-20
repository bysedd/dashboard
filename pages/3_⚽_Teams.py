import streamlit as st
import pandas as pd
import plotly.express as px

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
                "Wage(£)",
                "Overall",
                "Joined",
                "Height(Cm.)",
                "Weight(Lbs.)",
                "Contract Valid Until",
                "Value(£)",
                "Release Clause(£)",
            ]
        ],
        hide_index=True,
        column_config={
            "Age": st.column_config.NumberColumn(
                label="Age", format="%d", help="Age in years"
            ),
            "Photo": st.column_config.ImageColumn(label="Photo", help="Player's photo"),
            "Flag": st.column_config.ImageColumn(label="Country"),
            "Value(£)": st.column_config.Column(
                label="Market Value", help="Market value of the player"
            ),
            "Wage(£)": st.column_config.ProgressColumn(
                label="Weekly Wage",
                format="£ %d",
                min_value=0,
                max_value=club_df["Wage(£)"].max(),
                width="medium",
            ),
            "Overall": st.column_config.ProgressColumn(
                label="Overall", format="%d", min_value=0, max_value=100, width="medium"
            ),
            "Joined": st.column_config.DateColumn(
                label="Joined Club",
                format="MM/DD/YYYY",
                help="Date that the player joined the club",
            ),
            "Contract Valid Until": st.column_config.NumberColumn(
                label="Contract Valid Until",
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


def display_more_info(club_df: pd.DataFrame) -> None:
    # Cria uma tabela com as informações do time
    team_info = pd.DataFrame(
        {
            "Total players": [club_df.shape[0]],
            "Total market value": [
                f"£ {club_df['Value(£)'].apply(lambda x: int(x[2:].replace(',', ''))).sum():,.0f}"
            ],
            "Weekly player spend": [f"£ {club_df['Wage(£)'].sum():,.0f}"],
            "Average age": [round(club_df["Age"].mean())],
            "Overall average": [club_df["Overall"].mean()],
            "Average height": [f"{club_df['Height(Cm.)'].mean():.2f} cm"],
            "Average weight": [f"{club_df['Weight(Lbs.)'].mean():.2f} lbs"],
            "Most contract end": [club_df["Contract Valid Until"].mode().iloc[0]],
        }
    )
    st.dataframe(
        team_info,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total players": st.column_config.NumberColumn(
                format="%d",
                width="small",
                help="Total players in the team",
            ),
            "Total market value": st.column_config.TextColumn(
                width="small",
                help="Total market value of the team",
            ),
            "Weekly player spend": st.column_config.TextColumn(
                width="small",
                help="Total weekly player spend",
            ),
            "Average age": st.column_config.NumberColumn(
                format="%d",
                width="small",
                help="Average age of the team",
            ),
            "Overall average": st.column_config.ProgressColumn(
                format="%d",
                min_value=0,
                max_value=100,
                width="medium",
                help="Average overall rating of the team",
            ),
            "Average height": st.column_config.TextColumn(
                width="small", help="Average height of the team"
            ),
            "Average weight": st.column_config.TextColumn(
                width="small", help="Average weight of the team"
            ),
            "Most contract end": st.column_config.NumberColumn(
                format="%d",
                width="small",
                help="Most common contract end year",
            ),
        },
    )

    st.divider()

    # Cria uma tabela com as médias por posição
    position_averages = club_df.groupby("Position")[
        ["Age", "Overall", "Height(Cm.)", "Weight(Lbs.)"]
    ].mean().round(decimals=0)

    fig = px.bar(
        position_averages,
        x=position_averages.index,
        y=["Age", "Overall", "Height(Cm.)", "Weight(Lbs.)"],
        title="Averages by position",
        labels={"variable": "Metrics", "value": "Average"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )

    # Aumenta a fonte do título e das métricas
    fig.update_layout(
        title={
            "text": "Averages by position",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(
                size=24,
            ),
        },
        legend=dict(
            title_font_size=18,
            font=dict(size=14),
        ),
        xaxis_title="Position",
        yaxis_title="Average",
        xaxis=dict(
            title_font=dict(
                size=18,
            ),
            tickfont=dict(
                size=14,
            ),
        ),
        yaxis=dict(
            title_font=dict(
                size=18,
            ),
            tickfont=dict(
                size=14,
            ),
        ),
        height=600,
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)


def main():
    df_data = st.session_state["df_data"]
    club_df = select_club(df_data)
    display_club_info(club_df)
    display_club_stats(club_df)
    display_more_info(club_df)


if __name__ == "__main__":
    try:
        main()
    except KeyError:
        st.error("Please go to the **🏠 Home** first. Then back to this page.")
