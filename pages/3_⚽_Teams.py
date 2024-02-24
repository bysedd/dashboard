import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Teams", page_icon="⚽", layout="wide")


def select_club(df_data):
    club = st.sidebar.selectbox("Select a club", df_data["Club"].unique())
    club_df = df_data[df_data["Club"] == club]
    return club_df


def display_club_stats(club_df):
    with st.container(border=True):
        st.image(club_df["Club Logo"].iloc[0], width=60)

        st.header("Club Info")
        club_stats = pd.DataFrame(
            {
                "Name": club_df["Name"],
                "Age": club_df["Age"],
                "Photo": club_df["Photo"],
                "Position": club_df["Position"],
                "Flag": club_df["Flag"],
                "Overall": club_df["Overall"],
                "Joined": club_df["Joined"],
                "Height(m.)": club_df["Height(m.)"],
                "Weight(Kg.)": club_df["Weight(Kg.)"],
                "Contract Valid Until": club_df["Contract Valid Until"],
                "Wage(£)": club_df["Wage(£)"],
                "Value(£)": club_df["Value(£)"],
                "Release Clause(£)": club_df["Release Clause(£)"],
            }
        )

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
                "Height(m.)": st.column_config.NumberColumn(
                    label="Height",
                    format="%.2f m",
                    help="Height in meters",
                    width="small",
                ),
                "Weight(Kg.)": st.column_config.NumberColumn(
                    label="Weight",
                    format="%d kg",
                    help="The weight of the player in kilograms.",
                    width="small",
                ),
            },
            use_container_width=True,
        )

        st.header("Club Statistics")
        team_info = pd.DataFrame(
            {
                "Total players": [club_df.shape[0]],
                "Total market value": [f"£ {club_df['Value(£)'].sum():,.0f}"],
                "Weekly players spend": [f"£ {club_df['Wage(£)'].sum():,.0f}"],
                "Average age": [round(club_df["Age"].mean())],
                "Overall average": [club_df["Overall"].mean()],
                "Average height": [f"{club_df['Height(m.)'].mean():.2f} m"],
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
                "Weekly players spend": st.column_config.TextColumn(
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


def display_position_means(club_df: pd.DataFrame) -> None:
    selected_columns = [
        "Wage(£)",
        "Age",
        "Overall",
        "Height(m.)",
        "Weight(Kg.)",
        "Value(£)",
    ]

    # Permite que o usuário escolha uma feature
    selected_feature = st.selectbox("Select a feature", selected_columns)

    # Cria uma tabela com a média da feature selecionada por posição
    position_averages = (
        club_df.groupby("Position")[selected_feature].mean().round(decimals=2)
    )

    fig = px.bar(
        position_averages,
        x=position_averages.index,
        y=position_averages.values,
        title=f"Average {selected_feature} by position",
        labels={"color": selected_feature, "y": selected_feature},
    )

    fig.update_layout(
        title={
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(
                size=24,
            ),
        },
        xaxis=dict(
            title="Position",
            title_font=dict(
                size=18,
            ),
            tickfont=dict(
                size=14,
            ),
        ),
        yaxis=dict(
            title=selected_feature,
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
    df_data = st.session_state["fifa23"]
    club_df = select_club(df_data)
    display_club_stats(club_df)
    display_position_means(club_df)


if __name__ == "__main__":
    try:
        main()
    except KeyError:
        st.error("Please go to the **🏠 Home** first. Then back to this page.")
