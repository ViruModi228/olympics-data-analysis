import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

athletes = pd.read_csv('athlete_events.csv')
regions = pd.read_csv('noc_regions.csv')

athletes = preprocessor.preprocess(athletes,regions)

st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(athletes)
    selected_years = st.sidebar.selectbox("Select Years",years)
    selected_country = st.sidebar.selectbox("Select Country",country)
    medal_tally = helper.fetch_medal_tally(athletes,selected_years,selected_country)

    if selected_years == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    
    elif selected_years == '!Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + selected_years + " olympics ")
    
    elif selected_years == 'Overall' and selected_country == '!Overall':
        st.title(selected_country + " Overall Medal Tally")
    
    elif selected_years == '!Overall' and selected_country == '!Overall':
        st.title("Medal Tally of " + selected_country + " in " + selected_years + " olympics ")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = athletes['Year'].unique().shape[0]-1
    cities = athletes['City'].unique().shape[0]
    sports = athletes['Sport'].unique().shape[0]
    events = athletes['Event'].unique().shape[0]
    athletes_name = athletes['Name'].unique().shape[0]
    nations = athletes['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes_name)
    with col3:
        st.header("Nations")
        st.title(nations)

    data_over_time = helper.nations_per_time(athletes,"region")
    # using plotly for better visualization

    fig = px.line(data_over_time,x='Year',y='region')
    st.title('Participating Nations over years')
    st.plotly_chart(fig)

    
    event_over_time = helper.nations_per_time(athletes,"Event")
    
    fig = px.line(event_over_time,x='Year',y='Event')
    st.title('Events over years')
    st.plotly_chart(fig)

    
    athletes_over_time = helper.nations_per_time(athletes,"Name")
    
    fig = px.line(athletes_over_time,x='Year',y='Name')
    st.title('Athletes over years')
    st.plotly_chart(fig)

    st.title('No. of Events per year(For Every Sports)')
    fig,ax = plt.subplots(figsize=(20,20))
    heat_df = athletes.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(heat_df.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = athletes['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    most_successfull = helper.most_successful(athletes,selected_sport,'Overall')
    st.table(most_successfull)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = athletes['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country_3 = st.sidebar.selectbox('Select a Country',country_list)

    country_medals = helper.fetch_medal_tally(athletes,'Overall',selected_country_3)
    fig = px.line(country_medals,x='Year',y='Total')
    st.title('Medal Tally of ' + selected_country_3)
    st.plotly_chart(fig)

    new_df = helper.country_sport_heat(athletes,selected_country_3)
    st.title('Performance in sports(Medals)')
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0),annot=True)
    st.pyplot(fig)

    sport_list = athletes['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport_3 = st.selectbox('Select a Sport',sport_list)
    if selected_sport_3 == 'Overall':
        st.title('Top 10 Athletes of '+ selected_country_3)
    else:
        st.title('Top Athletes of '+ selected_country_3+' in '+selected_sport_3)            
    most_successfull_3 = helper.most_successful(athletes,selected_sport_3,selected_country_3)
    st.table(most_successfull_3)

if user_menu == 'Athlete-wise Analysis':
    st.sidebar.title('Athlete-wise Analysis')
    country_list = athletes['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0, 'Overall')
    selected_country_4 = st.sidebar.selectbox('Select a Country', country_list)

    sport_list = athletes['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport_4 = st.sidebar.selectbox('Select a Sport', sport_list)

    if selected_sport_4 == 'Overall' and selected_country_4 == 'Overall':
        st.title('Age Distribution of Medal Winning Athletes')
    elif selected_sport_4 == 'Overall' and selected_country_4 != 'Overall':
        st.title('Age Distribution of Medal Winning Athletes in ' + selected_country_4)
    elif selected_sport_4 != 'Overall' and selected_country_4 == 'Overall':
        st.title('Age Distribution of Medal Winning Athletes in ' + selected_sport_4)
    elif selected_sport_4 != 'Overall' and selected_country_4 != 'Overall':
        st.title('Age Distribution of Medal Winning Athletes in ' + selected_country_4 + ' in ' + selected_sport_4)

    x1, x2, x3, x4 = helper.get_age_distribution(athletes, selected_sport_4, selected_country_4)

    data = [x for x in [x1, x2, x3, x4] if not x.empty]
    labels = ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist']
    non_empty_labels = [labels[i] for i, x in enumerate([x1, x2, x3, x4]) if not x.empty]

    if data:
        fig = ff.create_distplot(data, non_empty_labels, show_hist=False, show_rug=False)
        st.plotly_chart(fig)
    else:
        st.write("No data available.")

    if selected_sport_4 == 'Overall' and selected_country_4 == 'Overall':
        st.title('Weight-Height Distribution of All Athletes')
    elif selected_sport_4 == 'Overall' and selected_country_4 != 'Overall':
        st.title('Weight-Height Distribution of All Athletes in ' + selected_country_4)
    elif selected_sport_4 != 'Overall' and selected_country_4 == 'Overall':
        st.title('Weight-Height Distribution of All Athletes in ' + selected_sport_4)
    elif selected_sport_4 != 'Overall' and selected_country_4 != 'Overall':
        st.title('Weight-Height Distribution of All Athletes in ' + selected_country_4 + ' in ' + selected_sport_4)


    temp_df = helper.weight_height(athletes,selected_sport_4,selected_country_4)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal',style='Sex' ,data=temp_df,s=100)
    st.pyplot(fig)

    if selected_sport_4 == 'Overall' and selected_country_4 == 'Overall':
        st.title('Total/Medal Athletes')
    elif selected_sport_4 == 'Overall' and selected_country_4 != 'Overall':
        st.title('Total/Medal Athletes in ' + selected_country_4)
    elif selected_sport_4 != 'Overall' and selected_country_4 == 'Overall':
        st.title('Total/Medal Athletes in ' + selected_sport_4)
    elif selected_sport_4 != 'Overall' and selected_country_4 != 'Overall':
        st.title('Total/Medal Athletes in ' + selected_country_4 + ' in ' + selected_sport_4)

    medal_winning_athletes = athletes.dropna(subset=['Medal'])
    medal_winning_athletes.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    final_athletes = helper.athletes_country(athletes,medal_winning_athletes,selected_sport_4,selected_country_4)

    fig = px.line(final_athletes,x='Year',y=['total_athletes','medal_athletes'])
    st.plotly_chart(fig)

    if selected_sport_4 == 'Overall' and selected_country_4 == 'Overall':
        st.title('Total/Medal Men-Women Athletes')
    elif selected_sport_4 == 'Overall' and selected_country_4 != 'Overall':
        st.title('Total/Medal Men-Women Athletes in ' + selected_country_4)
    elif selected_sport_4 != 'Overall' and selected_country_4 == 'Overall':
        st.title('Total/Medal Men-Women Athletes in ' + selected_sport_4)
    elif selected_sport_4 != 'Overall' and selected_country_4 != 'Overall':
        st.title('Total/Medal Men-Women Athletes in ' + selected_country_4 + ' in ' + selected_sport_4)

    final_medal = helper.men_women(athletes,medal_winning_athletes,selected_sport_4,selected_country_4)
    fig = px.line(final_medal,x='Year',y=['Male','Female','Medal_Male','Medal_Female'])
    st.plotly_chart(fig)
