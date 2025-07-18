import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="NBA Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample NBA data (in a real app, you'd connect to NBA API)
@st.cache_data
def load_team_data():
    teams = {
        'Team': ['Lakers', 'Warriors', 'Celtics', 'Nets', 'Heat', 'Bucks', 'Nuggets', 'Suns', 
                'Clippers', 'Mavericks', 'Knicks', 'Sixers', 'Grizzlies', 'Pelicans', 'Timberwolves'],
        'Conference': ['West', 'West', 'East', 'East', 'East', 'East', 'West', 'West', 
                      'West', 'West', 'East', 'East', 'West', 'West', 'West'],
        'Wins': [45, 42, 48, 32, 44, 49, 53, 45, 44, 38, 47, 54, 51, 42, 56],
        'Losses': [37, 40, 34, 50, 38, 33, 29, 37, 38, 44, 35, 28, 31, 40, 26],
        'Win_Percentage': [0.549, 0.512, 0.585, 0.390, 0.537, 0.598, 0.646, 0.549, 
                          0.537, 0.463, 0.573, 0.659, 0.622, 0.512, 0.683],
        'PPG': [118.2, 117.5, 120.6, 112.5, 110.5, 118.6, 114.8, 115.8, 
               117.0, 117.1, 112.8, 114.6, 113.1, 115.0, 113.9],
        'City': ['Los Angeles', 'San Francisco', 'Boston', 'Brooklyn', 'Miami', 'Milwaukee', 
                'Denver', 'Phoenix', 'Los Angeles', 'Dallas', 'New York', 'Philadelphia', 
                'Memphis', 'New Orleans', 'Minneapolis']
    }
    return pd.DataFrame(teams)

@st.cache_data
def load_player_data():
    players = {
        'Player': ['LeBron James', 'Stephen Curry', 'Jayson Tatum', 'Kevin Durant', 'Jimmy Butler',
                  'Giannis Antetokounmpo', 'Nikola Jokic', 'Devin Booker', 'Kawhi Leonard', 
                  'Luka Doncic', 'Jalen Brunson', 'Joel Embiid', 'Ja Morant', 'Zion Williamson', 
                  'Anthony Edwards'],
        'Team': ['Lakers', 'Warriors', 'Celtics', 'Nets', 'Heat', 'Bucks', 'Nuggets', 'Suns', 
                'Clippers', 'Mavericks', 'Knicks', 'Sixers', 'Grizzlies', 'Pelicans', 'Timberwolves'],
        'Position': ['F', 'G', 'F', 'F', 'G', 'F', 'C', 'G', 'F', 'G', 'G', 'C', 'G', 'F', 'G'],
        'PPG': [25.7, 26.4, 26.9, 27.1, 20.8, 31.1, 26.4, 27.1, 23.7, 32.4, 28.7, 34.7, 25.1, 22.9, 25.9],
        'RPG': [7.3, 4.5, 8.1, 6.7, 5.3, 11.0, 12.4, 4.5, 6.1, 8.2, 3.7, 11.0, 5.6, 5.8, 5.4],
        'APG': [8.3, 5.1, 4.9, 5.0, 5.0, 5.7, 9.0, 6.2, 3.6, 9.8, 6.7, 5.8, 8.1, 2.8, 5.1],
        'Age': [39, 36, 26, 35, 34, 29, 29, 27, 32, 25, 27, 30, 24, 24, 22]
    }
    return pd.DataFrame(players)

# Load data
teams_df = load_team_data()
players_df = load_player_data()

# Main app
st.title("🏀 NBA Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Overview", "Team Stats", "Player Stats", "Comparisons"])

if page == "Overview":
    st.header("NBA Season Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Teams", len(teams_df))
    with col2:
        st.metric("Average PPG", f"{teams_df['PPG'].mean():.1f}")
    with col3:
        st.metric("Highest Win %", f"{teams_df['Win_Percentage'].max():.3f}")
    with col4:
        st.metric("Total Players", len(players_df))
    
    st.subheader("Conference Standings")
    
    # Conference standings
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Eastern Conference**")
        east_teams = teams_df[teams_df['Conference'] == 'East'].sort_values('Win_Percentage', ascending=False)
        east_teams['Rank'] = range(1, len(east_teams) + 1)
        st.dataframe(east_teams[['Rank', 'Team', 'Wins', 'Losses', 'Win_Percentage']].reset_index(drop=True))
    
    with col2:
        st.write("**Western Conference**")
        west_teams = teams_df[teams_df['Conference'] == 'West'].sort_values('Win_Percentage', ascending=False)
        west_teams['Rank'] = range(1, len(west_teams) + 1)
        st.dataframe(west_teams[['Rank', 'Team', 'Wins', 'Losses', 'Win_Percentage']].reset_index(drop=True))
    
    # Win percentage visualization
    st.subheader("Team Win Percentages")
    fig = px.bar(teams_df.sort_values('Win_Percentage', ascending=True), 
                 x='Win_Percentage', y='Team', 
                 color='Conference',
                 title="Win Percentage by Team",
                 labels={'Win_Percentage': 'Win Percentage', 'Team': 'Team'})
    st.plotly_chart(fig, use_container_width=True)

elif page == "Team Stats":
    st.header("Team Statistics")
    
    # Team selector
    selected_team = st.selectbox("Select a team", teams_df['Team'].tolist())
    team_data = teams_df[teams_df['Team'] == selected_team].iloc[0]
    
    # Team info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Wins", team_data['Wins'])
    with col2:
        st.metric("Losses", team_data['Losses'])
    with col3:
        st.metric("Win Percentage", f"{team_data['Win_Percentage']:.3f}")
    
    st.metric("Points Per Game", f"{team_data['PPG']:.1f}")
    
    # Team comparison chart
    st.subheader("Team Comparison")
    stat_option = st.selectbox("Select statistic to compare", ["Win_Percentage", "PPG", "Wins", "Losses"])
    
    fig = px.bar(teams_df.sort_values(stat_option, ascending=False), 
                 x='Team', y=stat_option,
                 color='Conference',
                 title=f"{stat_option} by Team")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show team roster
    st.subheader(f"{selected_team} Roster")
    team_players = players_df[players_df['Team'] == selected_team]
    if len(team_players) > 0:
        st.dataframe(team_players[['Player', 'Position', 'PPG', 'RPG', 'APG', 'Age']])
    else:
        st.write("No player data available for this team.")

elif page == "Player Stats":
    st.header("Player Statistics")
    
    # Player selector
    selected_player = st.selectbox("Select a player", players_df['Player'].tolist())
    player_data = players_df[players_df['Player'] == selected_player].iloc[0]
    
    # Player info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Points Per Game", f"{player_data['PPG']:.1f}")
    with col2:
        st.metric("Rebounds Per Game", f"{player_data['RPG']:.1f}")
    with col3:
        st.metric("Assists Per Game", f"{player_data['APG']:.1f}")
    with col4:
        st.metric("Age", player_data['Age'])
    
    st.write(f"**Team:** {player_data['Team']}")
    st.write(f"**Position:** {player_data['Position']}")
    
    # Top performers
    st.subheader("League Leaders")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Top Scorers**")
        top_scorers = players_df.nlargest(5, 'PPG')[['Player', 'PPG']]
        st.dataframe(top_scorers.reset_index(drop=True))
    
    with col2:
        st.write("**Top Rebounders**")
        top_rebounders = players_df.nlargest(5, 'RPG')[['Player', 'RPG']]
        st.dataframe(top_rebounders.reset_index(drop=True))
    
    with col3:
        st.write("**Top Assisters**")
        top_assisters = players_df.nlargest(5, 'APG')[['Player', 'APG']]
        st.dataframe(top_assisters.reset_index(drop=True))
    
    # Player stats scatter plot
    st.subheader("Player Statistics Scatter Plot")
    x_stat = st.selectbox("X-axis", ["PPG", "RPG", "APG", "Age"], key="x_stat")
    y_stat = st.selectbox("Y-axis", ["PPG", "RPG", "APG", "Age"], key="y_stat", index=1)
    
    fig = px.scatter(players_df, x=x_stat, y=y_stat, 
                     color='Position', hover_data=['Player', 'Team'],
                     title=f"{x_stat} vs {y_stat}")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Comparisons":
    st.header("Player & Team Comparisons")
    
    # Player comparison
    st.subheader("Player Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("Select first player", players_df['Player'].tolist(), key="player1")
    with col2:
        player2 = st.selectbox("Select second player", players_df['Player'].tolist(), key="player2", index=1)
    
    if player1 != player2:
        p1_data = players_df[players_df['Player'] == player1].iloc[0]
        p2_data = players_df[players_df['Player'] == player2].iloc[0]
        
        comparison_data = pd.DataFrame({
            'Statistic': ['PPG', 'RPG', 'APG', 'Age'],
            player1: [p1_data['PPG'], p1_data['RPG'], p1_data['APG'], p1_data['Age']],
            player2: [p2_data['PPG'], p2_data['RPG'], p2_data['APG'], p2_data['Age']]
        })
        
        fig = px.bar(comparison_data, x='Statistic', y=[player1, player2],
                     title=f"{player1} vs {player2}",
                     barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed comparison
        st.subheader("Detailed Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{player1}**")
            st.write(f"Team: {p1_data['Team']}")
            st.write(f"Position: {p1_data['Position']}")
            st.write(f"PPG: {p1_data['PPG']}")
            st.write(f"RPG: {p1_data['RPG']}")
            st.write(f"APG: {p1_data['APG']}")
            st.write(f"Age: {p1_data['Age']}")
        
        with col2:
            st.write(f"**{player2}**")
            st.write(f"Team: {p2_data['Team']}")
            st.write(f"Position: {p2_data['Position']}")
            st.write(f"PPG: {p2_data['PPG']}")
            st.write(f"RPG: {p2_data['RPG']}")
            st.write(f"APG: {p2_data['APG']}")
            st.write(f"Age: {p2_data['Age']}")
    
    # Team comparison
    st.subheader("Team Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Select first team", teams_df['Team'].tolist(), key="team1")
    with col2:
        team2 = st.selectbox("Select second team", teams_df['Team'].tolist(), key="team2", index=1)
    
    if team1 != team2:
        t1_data = teams_df[teams_df['Team'] == team1].iloc[0]
        t2_data = teams_df[teams_df['Team'] == team2].iloc[0]
        
        team_comparison = pd.DataFrame({
            'Statistic': ['Wins', 'Losses', 'Win_Percentage', 'PPG'],
            team1: [t1_data['Wins'], t1_data['Losses'], t1_data['Win_Percentage'], t1_data['PPG']],
            team2: [t2_data['Wins'], t2_data['Losses'], t2_data['Win_Percentage'], t2_data['PPG']]
        })
        
        fig = px.bar(team_comparison, x='Statistic', y=[team1, team2],
                     title=f"{team1} vs {team2}",
                     barmode='group')
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("📊 NBA Dashboard | Built with Streamlit")
st.markdown("*Note: This app uses sample data for demonstration purposes.*")