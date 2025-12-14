import streamlit as st
import processor,helper
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_csv('atlete.csv')
region_df=pd.read_csv('noc_regions.csv')
st.sidebar.title('olympics analysis')
df=processor.preprocess(df,region_df)
user_menu=st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.year_region_list(df)
    selected_year = st.sidebar.selectbox("Select year", years)
    selected_country = st.sidebar.selectbox("Select country", country)
    medal_tally = helper.fetch_all(df, selected_year, selected_country)
    if selected_year==' Overall' and selected_country==' Overall':
        st.title('Overall Analysis')
    if selected_year!='Overall' and selected_country=='Overall':
        st.title('Overall Analysis in ' + str(selected_year))
    if selected_year=='Overall' and selected_country!='Overall':
        st.title('Overall Analysis in '+ selected_country)
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country + ' Performance in '+ str(selected_year)+ ' Olympics ')
    st.table(medal_tally)

if user_menu=='Overall Analysis':
    st.title('Top Statistics')
    edition=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(edition)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])

    pivot = (
        x.pivot_table(
            index='Sport',
            columns='Year',
            values='Event',
            aggfunc='count'
        )
        .fillna(0)
        .astype(int)
    )

    sns.heatmap(pivot, annot=True, fmt="d", cmap="viridis", ax=ax)

    st.pyplot(fig)

    st.title('Most Successful Athlete')

    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')
    selected_sport=st.selectbox("Select a Sport", sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox("Select a country",country_list)
    country_df=helper.yera_wise_medal_tally(df,selected_country)
    st.title(selected_country+" Medal tally over the years")
    fig = px.line(
        country_df,
        x='Year',
        y='Medal',
        markers=True
    )

    fig.update_xaxes(
        tickmode='linear',
        dtick=4
    )

    fig.update_yaxes(
        tickmode='linear',
        dtick=1
    )

    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)
if user_menu == 'Athlete wise Analysis':
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)



