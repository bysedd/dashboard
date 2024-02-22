import streamlit as st
import pandas as pd
import plotly.express as px
from resources.helper_functions import format_currency

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

    club_stats = pd.DataFrame(
        {
            "Name": club_df["Name"],
            "Age": club_df["Age"],
            "Photo": club_df["Photo"],
            "Position": club_df["Position"],
            "Flag": club_df["Flag"],
            "Overall": club_df["Overall"],
            "Joined": club_df["Joined"],
            "Height(M.)": club_df["Height(M.)"],
            "Weight(Kg.)": club_df["Weight(Kg.)"],
            "Contract Valid Until": club_df["Contract Valid Until"],
            "Wage(£)": club_df["Wage(£)"],
            "Value(£)": club_df["Value(£)"],
            "Release Clause(£)": club_df["Release Clause(£)"],
        }
    )

    # # Apply the formatting function to the desired columns
    # club_stats[["Release Clause(£)", "Value(£)", "Wage(£)"]] = club_stats[
    #     ["Release Clause(£)", "Value(£)", "Wage(£)"]
    # ].apply(format_currency)

    st.dataframe(
        club_stats,
        hide_index=True,
        column_config={
            "Age": st.column_config.NumberColumn(format="%d", help="Age in years"),
            "Photo": st.column_config.ImageColumn(help="Player's photo"),
            "Position": st.column_config.TextColumn(help="Player's position"),
            "Flag": st.column_config.ImageColumn(label="Country"),
            "Value(£)": st.column_config.NumberColumn(
                format="£ %d",
                label="Market Value",
                help="Market value of the player",
            ),
            "Wage(£)": st.column_config.NumberColumn(
                format="£ %d",
                label="Weekly Wage",
                help="Weekly wage of the player",
            ),
            "Release Clause(£)": st.column_config.NumberColumn(
                format="£ %d",
                label="Release Clause",
                help="Release clause value",
            ),
            "Overall": st.column_config.ProgressColumn(
                format="%d", min_value=0, max_value=100, width="medium"
            ),
            "Joined": st.column_config.DateColumn(
                label="Joined Club",
                format="MM/DD/YYYY",
                help="Date that the player joined the club",
            ),
            "Contract Valid Until": st.column_config.NumberColumn(
                format="%d",
                help="Contract valid until year end",
            ),
            "Height(M.)": st.column_config.NumberColumn(
                label="Height", format="%.2f", help="Height in meters", width="small"
            ),
            "Weight(Kg.)": st.column_config.NumberColumn(
                label="Weight", format="%d", help="Weight in kilograms", width="small"
            ),
        },
        use_container_width=True,
    )


def display_more_info(club_df: pd.DataFrame) -> None:
    # Cria uma tabela com as informações do time
    team_info = pd.DataFrame(
        {
            "Total players": [club_df.shape[0]],
            "Total market value": [f"£ {club_df['Value(£)'].sum():,.0f}"],
            "Weekly player spend": [f"£ {club_df['Wage(£)'].sum():,.0f}"],
            "Average age": [round(club_df["Age"].mean())],
            "Overall average": [club_df["Overall"].mean()],
            "Average height": [f"{club_df['Height(M.)'].mean():.2f} m"],
            "Average weight": [f"{club_df['Weight(Kg.)'].mean():.2f} kg"],
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
                width="small", help="Average weight in kilograms of the team"
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
    position_averages = (
        club_df.groupby("Position")[["Age", "Overall", "Height(M.)", "Weight(Kg.)"]]
        .mean()
        .round(decimals=0)
    )

    fig = px.bar(
        position_averages,
        x=position_averages.index,
        y=["Age", "Overall", "Height(M.)", "Weight(Kg.)"],
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
    main()
