import streamlit as st


def set_page():
    st.set_page_config(page_title="Teams", page_icon="👤", layout="wide")


def select_player(df_data):
    club = st.sidebar.selectbox("Select a club", df_data["club"].unique())
    df_players = df_data[df_data["club"] == club]
    players = df_players["name"].value_counts().index
    player = st.sidebar.selectbox("Select a player", players)
    return df_data[df_data["name"] == player].iloc[0]


def display_player_info(player_stats):
    st.image(player_stats["photo"], width=100)
    st.title(player_stats["name"])
    st.markdown(f"**Club:** {player_stats['club']}")
    st.markdown(f"**Position:** {player_stats['position']}")
    # convert height(cm.) to height(m.) and weight(lbs.) to weight(kg.)
    height = player_stats["height(cm.)"] / 100
    weight = player_stats["weight(lbs.)"] * 0.45359237
    col1, col2, col3, _ = st.columns(4)
    with col1:
        st.markdown(f"**Age:** {player_stats['age']}")
    with col2:
        st.markdown(f"**Height(m):** {height:.2f}")
    with col3:
        st.markdown(f"**Weight(kg):** {weight:.2f}")


def display_player_stats(player_stats):
    st.divider()
    st.subheader(f"Overall {player_stats['overall']}")
    st.progress(int(player_stats["overall"]))
    col1, col2, col3, _ = st.columns(4)
    with col1:
        st.metric("Market value", f"£ {player_stats['value(£)']:,.0f}")
    with col2:
        st.metric("Weekly wage", f"£ {player_stats['wage(£)']:,.0f}")
    with col3:
        st.metric("Release clause", f"£ {player_stats['release clause(£)']:,.0f}")


def main():
    set_page()
    df_data = st.session_state["df_data"]
    player_stats = select_player(df_data)
    display_player_info(player_stats)
    display_player_stats(player_stats)


if __name__ == "__main__":
    try:
        main()
    except KeyError:
        st.error("Please go to the **🏠 Home** first. Then back to this page.")
