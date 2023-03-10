
import pymongo
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date
from io import StringIO

st.title("Tweeter scrape")

maxTweets = 1000

tweets_list1 = []
hashtag=st.sidebar.text_input("Enter the User_Hashtag:")
fromdate=st.sidebar.date_input("From_date(YYYY-MM-DD):")
enddate=st.sidebar.date_input("End_date(YYYY-MM-DD):")
tweets_count=st.sidebar.number_input("enter the count:",min_value=1,max_value=100)

if st.button('Click'):
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"from:{hashtag} since:{fromdate} until:{enddate}").get_items()):
        if i>maxTweets:
            break
        tweets_list1.append([ tweet.id,
                        tweet.user.username,
                        tweet.url,
                        tweet.rawContent,
                        tweet.replyCount,
                        tweet.retweetCount,
                        tweet.likeCount,
                        tweet.lang,
                        tweet.source,
                        tweet.date,])


tweets_df1 = pd.DataFrame(tweets_list1, columns=['Tweet Id','Username', 'URL', 'Content', 'Replay Count', 'Re Tweet', 'Like Count', 'Lang', 'Source','Datetime'])
tweets_df1

myDict1=tweets_df1.to_dict('list')

client=pymongo.MongoClient('mongodb+srv://Ranjith:25081998@cluster0.kk7aaab.mongodb.net')
db=client.guvitask
records=db.tweet

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)
    dataframe = pd.read_csv(uploaded_file)
    myDict1=dataframe.to_dict('list')
    records.insert_one(myDict1)
    st.success('Upload to MongoDB Successful!', icon="✅")
    
  #Download file  
def convert_df(dataframe):

    return dataframe.to_csv().encode('utf-8')

mycsv = convert_df(tweets_df1)

st.download_button(
    label="Download data as CSV",
    data=mycsv,
    file_name='scraped_data.csv',
    mime='text/csv',
)
