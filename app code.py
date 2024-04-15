import ssl
import time
import streamlit as st
import pandas as pd
import mysql.connector
import altair as alt

st.title("KNOT MY TYPE")
st.markdown("Embroidery Tutorials Database")
chosen_task=st.radio("Would you like individual?", ["Individual channel information", "Comparison of data of channels"])
st.divider()

if chosen_task == "Individual channel information":
    mydb = mysql.connector.connect(
            host='YOUR HOST',
            user='YOUR USER NAME',
            password='**********',
            database='capstone1'
        )
    
    cursor = mydb.cursor()
    cursor.execute("use capstone1")
    query = "SELECT DISTINCT channel_name FROM channels;"
    cursor.execute(query)
    data= cursor.fetchall()
    values = [row[0] for row in data] # type: ignore
    

    chosen_channel=st.selectbox("Pick a channel:",values)
    if chosen_channel:
        chosen_action=st.selectbox("What would you like to konw about the channel?",
                                ['---------','How many comments were made on each video, and what are their corresponding video names?',
                                 'Which video has the highest number of likes?',
                                 'Total number of likes and dislikes for each video, and what are their corresponding video names?',
                                 'Number of subscribers',
                                 'Total number of channel views', 'Channel published date'])

        if chosen_action == 'How many comments were made on each video, and what are their corresponding video names?':
            st.subheader("fetching...") 
            with st.spinner('wait for it...'):
                time.sleep(5)
            a=(f"select `video_comment_count`, `video_title` from `videos` where `channel_name`='{chosen_channel}' order by video_comment_count desc; ")
            df=pd.read_sql(a,mydb)
            st.write(df)
        if chosen_action == 'Which video has the highest number of likes?':
            b=(f"select `video_title`,`video_likes_count` from `videos` where `channel_name`='{chosen_channel}' order by `video_likes_count` desc limit 1 ; ")
            df=pd.read_sql(b,mydb)
            st.write(df)
        if chosen_action== 'Total number of likes and dislikes for each video, and what are their corresponding video names?':
            c=(f"select `video_title`, `video_likes_count`, `video_dislikes_count` from `videos` where `channel_name`='{chosen_channel}' order by video_likes_count desc; ")
            df=pd.read_sql(c,mydb)
            st.write(df)   
        if chosen_action == "Number of subscribers":
            d=(f"select channel_subscribers_count from channels where channel_name='{chosen_channel}'")
            df=pd.read_sql(d,mydb)
            st.write("Number of subscribers=",df)
        if chosen_action == "Total number of channel views":
            e=(f"select channel_views from channels where channel_name='{chosen_channel}'")
            df=pd.read_sql(e,mydb)
            st.write("Number of Views=",df)
        if chosen_action == "Channel published date":
            f=(f"select channel_pat from channels where channel_name='{chosen_channel}' ")
            df=pd.read_sql(f,mydb)
            st.write("Channel Published On:",df)
            


if chosen_task == "Comparison of data of channels":
    mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ne09ft#rt12gs',
            database='capstone1'
        )

    cursor = mydb.cursor()
    cursor.execute("use capstone1")
    chosen_action=st.selectbox("What would you like to konw?",
                                ["---------","What are the names of all the videos and their corresponding channels?",
                                 "Which channels have the most number of videos, and how many videos do they have?",
                                 "What are the top 10 most viewed videos and their respective channels?",
                                 "How many comments were made on each video, and what are their corresponding video names?",
                                 "Which videos have the highest number of likes, and what are their corresponding channel names?",
                                 "What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                 "What is the total number of views for each channel, and what are their corresponding channel names?",
                                 "What are the names of all the channels that have published videos in the year 2022? ",
                                 "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                 "Which videos have the highest number of comments, and what are their corresponding channel names?",
                                 "Subscribers count of each channel",])

    if chosen_action == "What are the names of all the videos and their corresponding channels?":
        sql="select channel_name,video_title from videos;"
        df=pd.read_sql(sql,mydb)
        st.write(df)
    if chosen_action == "Which channels have the most number of videos, and how many videos do they have?":
        sql="select channel_name,videos_count from channels order by videos_count desc;"
        df=pd.read_sql(sql,mydb)
        st.title("Bar Chart of Videos Count by Channel")
        st.write("Data:", df)
        color = st.color_picker("Select Color", "#1f77b4")
        st.bar_chart(df.set_index("channel_name"), color=color)
    if chosen_action == "What are the top 10 most viewed videos and their respective channels?" :
        sql="select c.channel_name,v.video_title,v.video_view_count from videos as v join channels as c on v.channel_id = c.channel_id order by video_view_count desc limit 10;"
        df=pd.read_sql(sql,mydb)
        st.write("Data:", df)
        chart = alt.Chart(df).mark_circle(color="green").encode(
            x='video_title',
            y='video_view_count',
            tooltip=['channel_name']
            ).interactive()
        st.altair_chart(chart, use_container_width=True)
    if chosen_action == "How many comments were made on each video, and what are their corresponding video names?":
        sql="select video_title, video_comment_count from videos; "
        df=pd.read_sql(sql,mydb)
        color = st.color_picker("Select Color", "#1f77b4")
        st.bar_chart(df.set_index("video_title"), color=color)
    if chosen_action == "Which videos have the highest number of likes, and what are their corresponding channel names?":
        sql="select c.channel_name, v.video_title, v.video_likes_count from videos v join channels c ON v.channel_id = c.channel_id where (v.channel_id, v.video_likes_count) in (select channel_id, max(video_likes_count)from videos group by channel_id);"
        df=pd.read_sql(sql,mydb)
        st.write(df)
        chart = alt.Chart(df).mark_circle(color="green").encode(
            x='channel_name',
            y='video_comment_count',
            tooltip=['video_id']
            ).interactive()
        st.altair_chart(chart, use_container_width=True)
    if chosen_action == "What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
        sql="select video_title,video_likes_count,video_dislikes_count from videos order by video_likes_count desc;"
        df=pd.read_sql(sql,mydb)
        st.write(df)
    if chosen_action == "What is the total number of views for each channel, and what are their corresponding channel names?":
        sql="select channel_name, channel_views from channels order by channel_views;"
        df=pd.read_sql(sql,mydb)
        st.write(df)
    if chosen_action == "What are the names of all the channels that have published videos in the year 2022?":
       sql="select distinct channel_name from videos where video_pat = '2022%';"
       df=pd.read_sql(sql,mydb)
       st.write(df)
    if chosen_action == "What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        sql="SELECT c.channel_name, sec_to_time(Avg(v.duration_seconds)) AS average_duration FROM channels c JOIN video_dur_info v ON c.channel_id = v.channel_id GROUP BY v.channel_id, v.channel_name;"
        df=pd.read_sql(sql,mydb)
        st.write(df)
    if chosen_action == "Which videos have the highest number of comments, and what are their corresponding channel names?":
        sql="select c.channel_name, v.video_id, v.video_comment_count from videos v join channels c on c.channel_id=v.channel_id where (v.channel_name, v.video_comment_count) in (select channel_name, max(video_comment_count) from videos GROUP BY channel_name);"
        df=pd.read_sql(sql,mydb)
        chart = alt.Chart(df).mark_circle(color="green").encode(
            x='channel_name',
            y='video_comment_count',
            tooltip=['video_id']
            ).interactive()
        st.altair_chart(chart, use_container_width=True)
    if chosen_action == "Subscribers count of each channel":
        sql="select channel_name,channel_subscribers_count from channels order by channel_subscribers_count desc;"
        df=pd.read_sql(sql,mydb)
        color = st.color_picker("Select Color", "#1f77b4")
        st.bar_chart(df.set_index("channel_name"), color=color)
    
