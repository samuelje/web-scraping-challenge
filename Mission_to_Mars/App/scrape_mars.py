# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def init_browser():
    # Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path':'/Users/jeann/git_school/Tools/chromedriver'}
    browser = Browser('chrome', **executable_path)

def scrape():
    browser = init_browser()
    mars_dict ={}

    # Mars news URL of webpage to scrape
    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Obtain the latest news title and paragraph
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text
    # Quit splinter browser
    browser.quit()

    # JPL Mars image to be scraped 
    browser = Browser('chrome', **executable_path)
    jpl_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html 
    images_soup = soup(html, 'html.parser')
    # Image link
    ft_image_path = images_soup.find_all('img')[3]["src"]
    ft_image_url = jpl_url + ft_image_path
    # Quit splinter browser
    browser.quit()

    # Mars facts to scrape and inserted into dataframe
    browser = Browser('chrome', **executable_path)
    facts_url = 'http://space-facts.com/mars/'
    browser.visit(facts_url)
    html = browser.html
    facts_soup = soup(html, 'html.parser')
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)
    mars_table = df.to_html()
    # Quit splinter browser
    browser.quit()

    # Mars hemisphere data to scrape
    browser = Browser('chrome', **executable_path)
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = soup(hemisphere_html, 'html.parser')
    # Mars hemispheres data 
    all_mars_hemispheres = hemisphere_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    # Create dictionary for hemispheres URLs
    hemi_image_urls = []
    # Obtain a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")
    
    # Loop through links and click the link then return href
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        # Get hemi title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        # Append hemi to list
        hemi_image_urls.append(hemisphere)
        # Move back a page for next iteration
        browser.back()
    # Quit splinter browser
    browser.quit()

    # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "ft_image_url": ft_image_url,
        "fact_table": str(mars_table),
        "hemi_images": hemi_image_urls
    }

    return mars_dict



