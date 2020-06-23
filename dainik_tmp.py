import requests
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator
from datetime import date
import copy
import re
''' 
URL of the archive web-page which provides link to 
all video lectures. It would have been tiring to 
download each video manually. 
In this example, we first crawl the webpage to extract 
all the links and then download videos. 
'''

# specify the URL of the archive here
# archive_url = "https://www.bhaskar.com/mp/ashoknagar/"


def transgo(data):
    translatedList = []
    for index, row in data.iterrows():
        # REINITIALIZE THE API
        translator = Translator()
        newrow = copy.deepcopy(row)
        # print(row['News_Headlines'])
        try:
            # translate the 'text' column
            translated_head = translator.translate(row['News_Headlines'], dest='en')
            translated_article = translator.translate(row['Article'], dest='en')
            newrow['HeadLine_Translation'] = translated_head.text
            newrow['Article_Translation'] = translated_article.text
        except Exception as e:
            print(str(e))
            continue
        translatedList.append(newrow)
    return translatedList


def translate(hindi_texts):
    translator = Translator()
    translations = translator.translate(hindi_texts, dest='en')
    # english_trans = translations.text
    # for translation in translations:
    #     print(translation.text)
    return translations.text


def get_news_links(dist_url):
    # create response object
    r = requests.get(dist_url)

    # create beautiful-soup object
    soup = BeautifulSoup(r.content, 'lxml')

    # find all links on web-page
    links = soup.findAll(attrs={"class": "list_text"})

    # filter the link sending with .html
    # final_links = [link for link in links if 'class' in str(link)]
    news_links = [dist_url + link['href'] for link in links]
    news_headline = [headline['title'] for headline in links]
    # print(news_headline)
    # headlines_translation = [translate(headline['title']) for headline in links]


    return news_links,news_headline#, headlines_translation

def download_news_article(news_links):
    for link in news_links:

        '''iterate through all links in news_links
        and download them one by one'''

        # obtain filename by splitting url and getting
        # last string
        file_name = link.split('/')[-1]

        print("Downloading file:%s" % file_name)

        # create response object
        r = requests.get(link, stream=True)

        # download started
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        print("%s downloaded!\n" % file_name)

    print("All news downloaded!")
    return


def news_scrapping(links):
    paragraphs = []
    for link in links:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'lxml')
        contents = soup.findAll(attrs={"class": "db_storycontent"})[0]
        news = re.sub(r'[a-zA-Z-/<>._=""]', '', str(contents))
        paragraphs.append(str(news))
    return paragraphs


if __name__ == "__main__":
    link = ['https://www.bhaskar.com/mp/indore/news/shivraj-said-there-will-be-fire-of-agitation-in-the-entire-state-126475988.html',
            'https://www.bhaskar.com/mp/indore/news/indore-bjp-congress-on-deepika-padukone-chhapaak-movie-bjp-workers-protest-against-film-126483935.html']
    # para = news_scrapping(link)
    # getting all video links
    base_url = "https://www.bhaskar.com/mp/"
    dist_list = ['ashoknagar', 'bhopal', 'indore', 'gwalior', 'jabalpur', 'hoshangabad',
                 'khandwa', 'ratlam', 'Guna', 'ujjain', 'vidisha', 'raisen', 'rajgarh',
                 'sehore', 'bhind', 'datia', 'murena', 'sheopur', 'shivpuri', 'betul', 'harda',
                 'dewas', 'dhar', 'jhabua', 'indore-zila/burhanpur', 'khargon', 'mandsour',
                 'neemuch', 'chhatarpur', 'damoh', 'sagar', 'nagada', 'shajapur']
    contnt = []
    news_dist = []
    news_links = []
    news_headlines = []
    headlines_translation = []
    for dist in dist_list:
        dist_url = f'{base_url}{dist}'
        print(dist_url)
        news_link, news_headline = get_news_links(dist_url)
        news_dist.append([dist.title()]*len(news_link))
        news_links.append(news_link)
        news_headlines.append(news_headline)
        coll_content = news_scrapping(news_link)

        contnt.append(coll_content)
        # headlines_translation.append(headline_translation)
        print(f'The {dist.title()} News has been scrapped!')
        # data = pd.DataFrame(list(zip(news_headline, news_link, headline_translation)),
        #                     columns=['news_headlines', 'news_links', 'headlines_translation'])
        # data.to_csv(f'/Windows/Data/Dainik_bhaskar/{dist}.csv', index=False)
    contnts = [item for news in contnt for item in news]
    news_dist_list = [item for news in news_dist for item in news]
    news_headlines_list = [item for news in news_headlines for item in news]
    news_link_list = [item for news in news_links for item in news]
    # news_translation_list = [item for news in headlines_translation for item in news]
    data = pd.DataFrame(list(zip(news_dist_list, news_headlines_list, contnts, news_link_list)), columns=['District', 'News_Headlines', 'Article', 'News_Links'])
    data.to_csv(f'/Windows/Data/News_Scrapping/Dainik_bhaskar/Madhya_Pradesh_{date.today()}.csv', index=False)
    # # # download all videos
    # download_video_series(video_links)
