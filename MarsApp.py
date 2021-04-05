  
# Dependencies
import pandas as pd
from splinter import Browser 
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager

#Scrape code and return one Python dictionary containing the scraped data.
def scrape():
    # Setup Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

#Dictionary to hold scraped data.
    mars_dict = {}

# Scrape Latest News Title and Paragraph
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find('div', class_ = 'content_title').text
    news_p = soup.find('div', class_ = 'rollover_description_inner').text   

    mars_dict["News Title"] = news_title
    mars_dict["News Paragraph"] = news_p

# Scrape JPL Mars Featured Image
    JPL_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(JPL_url)

    #html = browser.html
    #soup = BeautifulSoup(html, 'html.parser')
    #mars_source_image = soup.find("img", class_='fancybox-image')['src']

    browser.find_link_by_partial_text("FULL IMAGE").click()
    mars_source_image = soup.find("img")['src']
    #mars_source_image = browser.find_by_css("img.fancybox-image")['src']
    #full_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{mars_source_image}"
    
    mars_dict["Featured Image"] = mars_source_image

# Scrape Mars Facts
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    Facts_url ="https://space-facts.com/mars/"
    browser.visit(Facts_url)

    tables = pd.read_html(Facts_url)
    df = tables[0]
    html_table = df.to_html()

    mars_dict["Table"] = html_table

# Scrape Mars Hemispheres
    Hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(Hemi_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    soup.body.find_all('img')

    hemispheres = []
    for x in range(4):
        hemisphere = {}
        hemisphere["title"] = browser.links.find_by_partial_text('Enhanced')[x].text
        browser.links.find_by_partial_text('Enhanced')[x].click()
        hemisphere["url"] = browser.links.find_by_partial_text('Sample')["href"]
        hemispheres.append(hemisphere)
        browser.back()

        mars_dict["Hemispheres"] = hemispheres

# Quit the browser
    browser.quit()

    return mars_dict

    print(mars_dict)
