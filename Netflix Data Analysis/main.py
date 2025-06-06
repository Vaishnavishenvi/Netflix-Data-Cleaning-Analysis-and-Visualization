# main.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io

# Set page config
st.set_page_config(page_title="Netflix Data Analysis", layout="wide")

st.title("🎬 Netflix Data Analysis Dashboard")
st.markdown("Upload your **Netflix dataset CSV file** to explore the data visually.")

# File uploader
uploaded_file = st.file_uploader("📁 Upload a CSV file", type="csv")

# Run if file is uploaded
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Data Preview
    st.subheader("🔍 Data Preview")
    st.dataframe(data.head())

    # Dataset Info
    st.subheader("ℹ️ Dataset Info")
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())

    # Dataset Shape
    st.write("**Shape of the dataset:**", data.shape)

    # Drop duplicates
    data = data.drop_duplicates()

    # Type Distribution
    st.subheader("📊 Content Type Distribution")
    if 'type' in data.columns:
        freq = data['type'].value_counts()

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        sns.countplot(data=data, x='type', ax=axes[0])
        axes[0].set_title("Count of Movies and TV Shows")
        axes[1].pie(freq, labels=freq.index, autopct='%.0f%%')
        axes[1].set_title("Percentage of Content Types")
        st.pyplot(fig)
    else:
        st.warning("Column 'type' not found in dataset.")

    # Rating Distribution
    st.subheader("⭐ Ratings Distribution")
    if 'rating' in data.columns:
        ratings = data['rating'].value_counts().reset_index()
        ratings.columns = ['rating', 'count']
        ratings = ratings.sort_values(by='count', ascending=False)

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.bar(ratings['rating'], ratings['count'])
        plt.xticks(rotation=45, ha='right')
        plt.xlabel("Rating Types")
        plt.ylabel("Count")
        plt.title("Rating on Netflix")
        st.pyplot(fig2)

        fig3, ax3 = plt.subplots()
        plt.pie(ratings['count'][:8], labels=ratings['rating'][:8], autopct='%.0f%%')
        plt.title("Top 8 Ratings Distribution")
        st.pyplot(fig3)
    else:
        st.warning("Column 'rating' not found in dataset.")

    # Date conversion
    if 'date_added' in data.columns:
        data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')

    # Top Countries
    st.subheader("🌍 Top 10 Countries with Most Content")
    if 'country' in data.columns:
        top_countries = data['country'].value_counts().reset_index()
        top_countries.columns = ['country', 'count']
        top_countries = top_countries[:10]

        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.bar(top_countries['country'], top_countries['count'])
        plt.xticks(rotation=45, ha='right')
        plt.xlabel("Country")
        plt.ylabel("Content Count")
        plt.title("Top 10 Countries")
        st.pyplot(fig4)
    else:
        st.warning("Column 'country' not found in dataset.")

    # Top Genres
    st.subheader("🎭 Top Genres")
    if 'type' in data.columns and 'listed_in' in data.columns:
        movie_genres = data[data['type'] == 'Movie'].groupby('listed_in').size().sort_values(ascending=False)[:10]
        tv_genres = data[data['type'] == 'TV Show'].groupby('listed_in').size().sort_values(ascending=False)[:10]

        st.markdown("**Top 10 Movie Genres**")
        fig5, ax5 = plt.subplots()
        ax5.bar(movie_genres.index, movie_genres.values)
        plt.xticks(rotation=45, ha='right')
        plt.title("Movie Genres")
        st.pyplot(fig5)

        st.markdown("**Top 10 TV Show Genres**")
        fig6, ax6 = plt.subplots()
        ax6.bar(tv_genres.index, tv_genres.values)
        plt.xticks(rotation=45, ha='right')
        plt.title("TV Show Genres")
        st.pyplot(fig6)
    else:
        st.warning("Required columns ('type' and 'listed_in') not found.")

    # Top Directors
    st.subheader("🎬 Top 15 Directors on Netflix")
    if 'director' in data.columns:
        directors = data['director'].value_counts().reset_index()
        directors.columns = ['director', 'count']
        directors = directors[1:16]

        fig7, ax7 = plt.subplots()
        ax7.bar(directors['director'], directors['count'])
        plt.xticks(rotation=45, ha='right')
        plt.title("Top Directors")
        st.pyplot(fig7)
    else:
        st.warning("Column 'director' not found in dataset.")

else:
    st.info("Please upload a CSV file to begin the analysis.")
