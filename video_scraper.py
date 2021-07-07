from re import T
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import timedelta, datetime as dt

video = {
    'id': None,
    'length': None,
    'date': None,
    'streamer': None,
    'category': None,
    'title': None,
    'url': None,
    'done': None,
    'favorite': None
}

def scrape_web_data(request_body, video_id):
    video['id'] = video_id
    video['url'] = request_body.url
    video['done'] = 0
    video['favorite'] = 0

    video['date'] = dt.today().date()

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(video['url'])

    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/div[3]/button').click()
    except:
        pass

    while True:
        try:
            if 'twitch.tv/videos' in video['url']:
                video['length'] = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/div[1]/div/div[1]/p[2]').text
                video['streamer'] = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/a/h1').text
                video['title'] = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/h2').text
                video['category'] = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div/div/a/p').text

                if '•' in video['title']:
                    video['date'] = calculate_date(video['title'].split('•')[1])
                    video['title'] = video['title'].split('•')[0]
            elif 'clips.twitch.tv' in video['url']:
                video['length'] = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[4]/div/div[1]/div/div[1]/p').text
                video['streamer'] = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[2]/div[1]/div/div[1]/a/span').text
                video['title'] = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/span').text
                video['category'] = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[2]/div[1]/div/div[1]/div/p/a').text
                video['date'] = calculate_date(driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div/main/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/div/div[1]/span').text)
            if ':' not in video['length']:
                video['length'] = f'00:{video["length"]}'
            driver.close()
            break
        except selenium.common.exceptions.NoSuchElementException:
            continue


    return video

def calculate_date(time_passed):
    d = dt.today()
    if 'yesterday' in time_passed.lower():
        d = dt.today() - timedelta(days=1)
    if 'last month' in time_passed.lower():
        d = dt.today() - timedelta(weeks=4)
    if 'last year' in time_passed.lower():
        d = dt.today() - timedelta(weeks=52)
    if 'days ago' in time_passed.lower():
        time = [int(s) for s in time_passed.lower().split() if s.isdigit()]
        d = dt.today() - timedelta(days=time[0])
    if 'months ago' in time_passed.lower():
        time = [int(s) for s in time_passed.lower().split() if s.isdigit()]
        d = dt.today() - timedelta(weeks=time[0]*4)
    if 'years ago' in time_passed.lower():
        time = [int(s) for s in time_passed.lower().split() if s.isdigit()]
        d = dt.today() - timedelta(weeks=time[0]*52)
    return d.date()