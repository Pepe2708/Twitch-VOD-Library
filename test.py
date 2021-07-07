from datetime import datetime as dt, timedelta
import datetime
# from re import T
# import selenium
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())

# url = 'https://www.twitch.tv/videos/1063237882'
# driver.get(url)

# while True:
#     try:
#         streamer = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/a/h1').text
#         title = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/h2').text
#         category = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div/div/a/p').text
#         duration = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div/div/div[5]/div/div[1]/div/div[1]/p[2]').text

#         print(streamer, title, category, duration)

#         driver.close()
#         break
#     except selenium.common.exceptions.NoSuchElementException:
#         continue





def calculate_date(time_passed):
    d = datetime.datetime.now().strftime("%d.%m.%Y")
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

title = 'VCO World Cup: 12h Donington • 9 days ago'

print(title.split('•')[1])
print(title.split('•')[0])