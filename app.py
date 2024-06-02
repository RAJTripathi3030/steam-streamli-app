import streamlit as st 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
from wordcloud import WordCloud 
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from PIL import Image 
import time 
st.title("EDA on Steam Gaming Data 🎮")
df = pd.read_csv("steam-games.csv")
st.dataframe(df)

# Idea-1 : add a slider for number of awards and return the number of/ list of all those games which recieved that particular number of awards - DONE 

st.title("General Analysis")
col1, col2 = st.columns([1,1])
with col1 :
    st.write(((df.isnull().sum()/df.shape[0])*100).reset_index().rename(columns = {'index': 'Column Name', 0: ' Percentage of NULL values'}))
    st.write("Following columns have hign number of missing values")
    if st.checkbox("Show the columns with percentage of missing values"):
        st.code("original_price : 88.56%")
        st.code("discount_percentage : 88.56%")
        st.code("content_descriptor : 94.41%")
        st.code("recent_review : 87.05%")
        st.code("recent_review_% : 87.05%")
        st.code("recent_review_count : 87.05%")
        # Performing Feature engineering here
        columns_to_drop = ["original_price", "discount_percentage", "content_descriptor", "recent_review", "recent_review_%", "recent_review_count"]
        df = df.drop(columns=columns_to_drop)
        
with col2 :
    "Rows : ", df.shape[0]
    "Cols : ", df.shape[1]
    options = ["View Covariance", "View Columns", "View Description", "View info", "View Dtypes"]
    selected_option = st.selectbox("Select from following", options)


    if selected_option == "View Covariance":
        numeric_df = df.select_dtypes(include = ['float64', 'int64'])
        st.write(numeric_df.cov())
    elif selected_option == "View Correlation":
        numeric_df = df.select_dtypes(include = ['float64', 'int64'])
        st.write(numeric_df.corr())
    elif selected_option == "View Columns":
        st.write(df.columns)
    elif selected_option == "View Description":
        st.write(df.describe())
    elif selected_option == "View info":
        st.write(df.info())
    else :
        st.write(df.dtypes.reset_index().rename(columns = {'index': 'Column Name', 0: 'Data Type'}))

if st.checkbox("Are you someone who judges a game by the number of awards it won? If yes then select me! 🏆"):
    award_count = st.sidebar.slider('Choose the number of awards ', min_value = 0, max_value = 41)
    list_of_games = []
    for i in range(df.shape[0]):
        if df['awards'][i] == award_count:
            list_of_games.append(df['title'][i])
    if len(list_of_games) > 0:
        st.table(list_of_games)
    else:
        st.warning("No game has won this number of awards")
# Idea-2 : Add a slider for number of DLCs and return the number of/ list of all those games which have that particular number of DLCs - DONE
if st.checkbox("Are you someone who judges a game by the number of DLCs it has? If yes then select me! 🎮"):
    dlc_count = st.sidebar.slider('Choose the number of DLCs ', min_value = 0, max_value = 41)
    list_of_games = []
    for i in range(df.shape[0]):
        if df['dlc_available'][i] == dlc_count:
            list_of_games.append(df['title'][i])
    if len(list_of_games) > 0:
        st.table(list_of_games)
    else:
        st.warning("No game has this number of DLCs")
# Analysis----------------------------------------------------------------------------------------------------------------
# making a word cloud for generes using plotly
if st.sidebar.checkbox("View Analysis"):
    with st.spinner(text='In progress'):
        time.sleep(3)
        st.success('Done')
    st.balloons()
    st.subheader("1. Word Cloud for game genres")
    wordcloud = WordCloud(width = 1000, height = 500).generate(' '.join(str(genre) for genre in df['genres']))
    
    # Convert the WordCloud to an image and then to a numpy array
    image = wordcloud.to_image()
    z = np.array(image)
    
    fig = go.Figure(data = go.Image(z=z))
    plt.imshow(wordcloud)
    plt.axis('off')
    st.pyplot(plt)
    
    st.subheader("2. Word Cloud for game categories")
    wordcloud1 = WordCloud(width = 1000, height = 500).generate(' '.join(str(category) for category in df['categories']))
    
    # Convert the WordCloud to an image and then to a numpy array
    image = wordcloud1.to_image()
    z = np.array(image)
    
    fig = go.Figure(data = go.Image(z = z))
    plt.imshow(wordcloud1)
    plt.axis('off')
    st.pyplot(plt)
    
    st.subheader("3. Most Common Developers")
    developer_bar = df.groupby('developer')['title'].count().sort_values(ascending = False).head(10)
    st.bar_chart(developer_bar)
    
    st.subheader("4. Most Common Publishers")
    publisher_bar = df.groupby('publisher')['title'].count().sort_values(ascending = False).head(10)
    st.bar_chart(publisher_bar)

    st.subheader("5. Reviews Analysis")
    review_bar = df.groupby("overall_review")['title'].count().sort_values(ascending = False)
    st.bar_chart(review_bar)
    
    # Age rated games vs non age rated games
    st.subheader("6. Age Rated Games VS Non-Age Rated Games")
    age_rated_bar = df.groupby('age_rating')['awards'].count().sort_values(ascending = False)
    st.bar_chart(age_rated_bar)
    st.write("From above visualization it is clear that, games with no age rating have earned most awards in total as compared to games with games with age rating")
    
    # awards vs dlc
    st.subheader("7. Awards vs DLC")
    fig = px.scatter(df, x = 'awards', y = 'dlc_available', labels = {'awards': 'Awards', 'dlc_available': 'DLC Count'})
    st.plotly_chart(fig)
    st.write("From the visualization above, it is visible that games with high number of DLCs have won less awards")
    
    # developer line chart
    st.subheader("8. Top developers with highest number of awards")
    line_chart = df.groupby('developer')['awards'].sum().sort_values(ascending = False).head(10)
    st.line_chart(line_chart)
    
    # publisher line chart
    st.subheader("9. Top publishers with highest number of awards")
    line_chart = df.groupby('publisher')['awards'].sum().sort_values(ascending = False).head(10)
    st.line_chart(line_chart)
   