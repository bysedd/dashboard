import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="Teams", page_icon="👤", layout="wide")


@st.cache_data
def get_club_players(df_players: pd.DataFrame) -> np.ndarray:
    return df_players["Name"].unique()


def select_player(df: pd.DataFrame) -> pd.DataFrame:
    use_club = st.sidebar.checkbox("Filter by club", True)
    if use_club:
        club = st.sidebar.selectbox("Select a club", st.session_state["clubs"])
        df_players = df[df["Club"] == club]
    else:
        df_players = df

    players = get_club_players(df_players)
    player = st.sidebar.selectbox("Select a player", players)
    player_df = df_players.loc[df_players["Name"] == player].iloc[0]

    return player_df


def display_player_info(player_stats):
    with st.expander(label="Player's details", expanded=True):
        photo = player_stats["Photo"]
        request = requests.get(photo)

        if request.status_code == 200:
            st.image(photo, width=100, caption=player_stats["Name"])
        else:
            st.image(
                "https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png",
                width=100,
                caption=player_stats["Name"],
            )

        st.markdown(
            f"""
            **Club**: :blue[{player_stats["Club"]}] ![]({player_stats["Club Logo"]})\n
            **Nationality**: :blue[{player_stats["Nationality"]}] ![]({player_stats["Flag"]})
            """
        )

        st.dataframe(
            data=pd.DataFrame(
                {
                    "Age": [player_stats["Age"]],
                    "Real Face": [player_stats["Real Face"]],
                    "Joined": [player_stats["Joined"]],
                    "Contract": [player_stats["Contract Valid Until"]],
                    "Loaned From": [player_stats["Loaned From"]],
                    "Position": [player_stats["Position"]],
                    "Preferred Foot": [player_stats["Preferred Foot"]],
                    "Special": [player_stats["Special"]],
                    "Work Rate": [player_stats["Work Rate"]],
                    "Body Type": [player_stats["Body Type"]],
                    "Height(m.)": [player_stats["Height(m.)"]],
                    "Weight(Kg.)": [round(player_stats["Weight(Kg.)"])],
                }
            ),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Age": st.column_config.NumberColumn(
                    format="%d",
                    help="The age of the player at the time of data collection.",
                ),
                "Real Face": st.column_config.CheckboxColumn(
                    help="Indicates whether the player has a real face representation.",
                    width="small",
                ),
                "Joined": st.column_config.DateColumn(
                    format="DD/MM/YYYY",
                    help="The date when the player joined the current club.",
                    width="small",
                ),
                "Contract": st.column_config.NumberColumn(
                    format="%d",
                    help="The date until which the player's contract is valid.",
                    width="small",
                ),
                "Loaned From": st.column_config.TextColumn(
                    help="The club from which the player is currently on loan.",
                    width="small",
                    required=False,
                ),
                "Position": st.column_config.TextColumn(
                    help="The player's preferred playing position.", width="small"
                ),
                "Preferred Foot": st.column_config.TextColumn(
                    help="The player's preferred foot for playing.", width="small"
                ),
                "Special": st.column_config.NumberColumn(
                    format="%d",
                    help="A numerical value representing the player's special abilities.",
                    width="small",
                ),
                "Work Rate": st.column_config.TextColumn(
                    help="The work rate of the player.",
                    width="small",
                ),
                "Body Type": st.column_config.TextColumn(
                    help="The physical build or body type of the player.",
                    width="small",
                ),
                "Height(m.)": st.column_config.NumberColumn(
                    label="Height",
                    format="%.2f m",
                    help="The height of the player in meters.",
                    width="small",
                ),
                "Weight(Kg.)": st.column_config.NumberColumn(
                    label="Weight",
                    format="%d kg",
                    help="The weight of the player in kilograms.",
                    width="small",
                ),
            },
        )

        # Divide os dados em duas partes
        df1 = player_stats[["International Reputation", "Weak Foot", "Skill Moves"]]
        df2 = player_stats[["Overall", "Potential"]]

        fig1 = px.bar(
            df1,
            x=df1.index,
            y=df1.values,
            labels={"index": "Feature", "y": "Value"},
            title="Player Features",
            color=df1.index,
        )
        fig1.update_layout(
            showlegend=False,
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
                title="",
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
            height=400,
        )
        fig1.update_yaxes(range=[1, 5])

        fig2 = px.bar(
            df2,
            x=df2.index,
            y=df2.values,
            labels={"index": "Feature", "y": "Value"},
            title="Player Ratings",
            color=df2.index,
        )
        fig2.update_layout(
            showlegend=False,
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
                title="",
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
            height=400,
        )
        fig2.update_yaxes(range=[1, 100])

        col1, col2 = st.columns(2)
        col1.plotly_chart(fig1, use_container_width=True)
        col2.plotly_chart(fig2, use_container_width=True)


def display_player_values(player_stats) -> None:
    metrics = ["Value(£)", "Wage(£)", "Release Clause(£)"]
    helps = [
        "The estimated market value of the player in pounds (£).",
        "The player's weekly wage in pounds (£).",
        "The release clause value of the player in pounds (£).",
    ]

    for col, metric, help in zip(st.columns(3), metrics, helps):
        delta = (
            0
            if player_stats[metric] == player_stats[f"Previous {metric}"]
            else player_stats[f"Previous {metric}"]
        )
        col.metric(
            label=metric,
            value=f"£ {player_stats[metric]:,.0f}",
            delta=f"{delta:,.0f}" if delta else None,
            help=help,
        )


def main():
    df_data = st.session_state["fifa23"]
    player_stats = select_player(df_data)
    display_player_info(player_stats)
    display_player_values(player_stats)


if __name__ == "__main__":
    try:
        main()
    except KeyError:
        st.error("Please go to the **🏠 Home** first. Then back to this page.")
