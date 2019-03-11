from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import os
import requests
import time



def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

      
    # Run the function below:
    title, paragraph = mars_news()
    
    # Run the functions below and store into a dictionary
    results = {
        "title": title,
        "paragraph": paragraph,
        "image_url": featured_image(browser),
        "weather": mars_weather(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
    }

    # Quit the browser and return the scraped results
    browser.quit()
    return results


    #read html file into jupyter
    filepath = os.path.join('nasa.html')
    with open(filepath) as file:
        html = file.read()


        url = 'https://mars.nasa.gov/news/?'
    browser.visit(url)
    time.sleep(2)
    #scrape through with soup :) 
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find('div',class_ = 'content_title').text.strip()
    news_p = soup.find('div', class_="article_teaser_body").text.strip()
    print(f'The Current News Title: {news_title}.')
    print(f'The opening to the paragraph is: {news_p}')


    #JPL Mars Space Images - Featured Image
    #scrape through JPL to pull latest photos :) gotta stick to master splinter yo.
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(4) 
    browser.click_link_by_partial_text('more info')
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")
    img_path = jpl_soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov" + img_path
    print(featured_image_url)

    #Mars Weather from Twitter
    #straight up shout out to medium for comeing through with this. 

    twt_url = u'https://twitter.com/marswxreport?lang=en'
    re = requests.get(twt_url)
    twt_soup = bs(re.text, 'html.parser')

    mars_weather= [p.text.strip() for p in twt_soup.find_all('p',class_='TweetTextSize')]
    mars_weather


    # Mars Facts
    # Panda scraping.... nuff said

    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    tables
    df = tables[0]

    df.rows = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons','Orbit Period', 'Surface Temperature', 'First Record', 'Recorded By']
    df.columns = ["Property", "Value"]
    df.head(9)

    #make dataframes as html
    html_table = df.to_html()
    html_table  
    #strip new lines
    html_table.replace('\n', '')

    #save table
    df.to_html('table.html')

    #open table 
    !open table.html

    #Mars Hemispheres

    usgs_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

    html = browser.html
    usgs_soup = BeautifulSoup(html, 'html.parser')

    mars_hemi = []

    # begin rightous for loop 

    for i in range(4): 
        time.sleep(5)
        images = browser.find_by_tag("h3")
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        part = soup.find("img", class_="wide-image")["src"]
        title = soup.find("h2", class_ = "title").text
        usg_url = "https://astrogeology.usgs.gov" + part
        dicey ={"title":title, "usg_url":usg_url}
        mars_hemi.append(dicey)
        browser.back()

    mars_hemi

     if __name__  ==  "__main__":
        print(scrape())

