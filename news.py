import requests
import random

def do_news_work(list_iit):
    answer = ''
    short_iit, full_iit = random.choice(list(list_iit.items()))
    url = "https://newsapi.org/v2/everything?q=" + full_iit.title(
    ) + "&domains=indianexpress.com,timesofindia.indiatimes.com,thehindu.com,techcrunch.com,techcrunch.cn&sources=google-news-in&sortBy=publishedAt&apiKey=3a0de736571043489ce4fc07a059cb87"

    response = requests.get(url)
    data = response.json()
    len_news = len(data["articles"])
    print(url)
    print(len_news)
    while (len_news < 2):
        short_iit, full_iit = random.choice(list(list_iit.items()))
        url = "https://newsapi.org/v2/everything?q=" + full_iit.title(
        ) + "&domains=indianexpress.com,timesofindia.indiatimes.com,thehindu.com,techcrunch.com,techcrunch.cn&sources=google-news-in&sortBy=publishedAt&apiKey=3a0de736571043489ce4fc07a059cb87"
        response = requests.get(url)
        data = response.json()
        len_news = len(data["articles"])
        print(url)
        print(len_news)

    short_iit = (short_iit[:3]).upper() + "-" + (short_iit[3:]).upper()
    # print(data)
    count = 1
    get_random_news_index = random.randint(0, len_news - 1)
    while (
            'IIT' not in data["articles"][get_random_news_index]['description']
    ) and ('IIT' not in data["articles"][get_random_news_index]['title']) and (
            'IIT' not in data["articles"][get_random_news_index]['content']
    ) and ('Indian Institute of' not in data["articles"][get_random_news_index]
           ['description']) and ('Indian Institute of' not in data["articles"]
                                 [get_random_news_index]['title']) and (
                                     'Indian Institute of' not in
                                     data["articles"][get_random_news_index]
                                     ['content']) or count < (len_news * 2):
        print(count)
        get_random_news_index = random.randint(0, len_news - 1)
        count += 1
    else:
        answer = answer + "\nBut,Do you know..." + str(
            data["articles"][get_random_news_index]['content'])
        answer = answer + "\nFor more details visit\n" + str(
            data["articles"][get_random_news_index]['url'])
    return answer