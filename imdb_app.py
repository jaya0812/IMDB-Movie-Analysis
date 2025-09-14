import streamlit as st
import pandas as pd
import mysql.connector

# MySQL connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0123456789",
    database="Guvi_proj1"
)
mycursor = connection.cursor(dictionary=True)
mycursor.execute("SELECT * FROM imdb")
rows = mycursor.fetchall()
connection.close()

# Load into DataFrame
df = pd.DataFrame(rows)

st.title("🎬 IMDB Movies Explorer")

# Ensure correct datatypes
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Genre"] = df["Genre"].astype(str)
df["Movie"] = df["Movie"].astype(str)
df["Voting_counts"] = df["Voting_counts"].astype(int)


# --- Sidebar filters inside a form ---
with st.sidebar.form("filters_form"):
    st.header("🔍 Filters")

    # Movie search
    search_movie = st.text_input("Search Movie by Name:")

    # Rating slider
    min_rating = float(df["Rating"].min())
    max_rating = float(df["Rating"].max())
    rating_range = st.slider(
        "Select Rating Range:",
        min_value=min_rating,
        max_value=max_rating,
        value=(min_rating, max_rating),
        step=0.1
    )

    # Genre dropdown (multi-select)
    all_genres = sorted(df["Genre"].unique())
    selected_genres = st.multiselect("Select Genre(s):", options=all_genres, default=all_genres)

    # Duration
    min_duration = float(df["Total_hours"].min())
    max_duration = float(df["Total_hours"].max())
    duration_range = st.slider(
        "Select Total_hours Range:",
        min_value=min_duration,
        max_value=max_duration,
        value=(min_duration, max_duration),
        step=.1   
    )
    #Voting counts
    min_vote = int(df["Voting_counts"].min())
    max_vote = int(df["Voting_counts"].max())
    vote_range = st.slider(
        "Select Voting counts Range:",
        min_value=min_vote,
        max_value=max_vote,
        value=(min_vote, max_vote),
        step=1000   
    )
    
    # Submit button
    submitted = st.form_submit_button("Search")    


# --- Apply filters only when button is clicked ---
if submitted:
    filtered_df = df[
        (df["Rating"] >= rating_range[0]) &
        (df["Rating"] <= rating_range[1]) &
        (df["Genre"].isin(selected_genres)) &
        (df["Total_hours"] >= duration_range[0]) &
        (df["Total_hours"] <= duration_range[1]) &
        (df["Voting_counts"] >= vote_range [0]) &
        (df["Voting_counts"] <= vote_range [1]) 
    ]

    if search_movie:
        filtered_df = filtered_df[filtered_df["Movie"].str.contains(search_movie, case=False, na=False)]

     # Add row numbers
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df.index = filtered_df.index + 1
    filtered_df.index.name = "Row No"

    st.write("### Filtered Movies")
    column_order = ["Movie", "Genre", "Rating", "Voting_counts", "Total_hours"]
    filtered_df = filtered_df[column_order]
    st.dataframe(filtered_df)
    st.write(f"✅ {len(filtered_df)} movies found")

