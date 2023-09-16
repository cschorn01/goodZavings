''' MySmartPrice Clone Aimed at the United States
    Web Scrape the Info from major brands to find the best deal based
        a search input such as "iphone", or "TV"
    Use affiliate links, ads, and product features to make money

    CLI command to flask run on zsh: python3 -m flask --app goodZavings run

    Author: Christopher Schorn
    
    Date: 8/17/2023

    Version 1.0.0: Runs, get product info and displays it from a few retailers
                   pretty slow though because it uses all python code
                   Next Update is using numpy arrays
                   Numpy Arrays ended up being not much faster, sticking to this, 9/13/2023
'''


'''
"""Print the latest tutorial from Real Python"""

    tic = time.perf_counter()

    tutorial = feed.get_article(0)

    toc = time.perf_counter()

    print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")

'''

''' General Notes

    In search function add a dictionary to add the details about the
        information returned from selenium scraping websites for details
        about the searched product

    Dictionary Structure
        Base Dictionary = { "amazon": "amazon dictionary",
                            "bestbuy": "best buy dictionary",
                            "walmart": "walmart dictionary" 
                          }

        Amazon Dictionary = { "product finding 1": "HTML SCRAPED",
                              "product finding 2": "HTML SCRAPED",
                              "product finding 1": "HTML SCRAPED"
                            }

    Have a loop in the search.html doc outputting each scraped website data in
        an easy to use format for the user to see the products

'''


''' Flask Notes

    Running Flask on the command link
        flask --app <appName> run

    request object 
        request.method: The HTTP method of the current request, such 
                        as "GET", "POST", "PUT", etc.
        request.args: A dictionary-like object that represents the GET 
                      query parameters in the current request.
        request.form: A dictionary-like object that represents the form data 
                      (i.e. the data sent in the request body) in the current request.
        request.headers: A dictionary-like object that represents the 
                         headers in the current request.
        request.cookies: A dictionary-like object that represents the cookies
                         in the current request.
        request.get_json(): A method that parses the JSON data sent in the 
                            request body and returns it as a Python object.

'''

''' Selenium Notes

    Navigation
        Open a website
        Get appends the form-data to the URL in 
            name/value pairs: URL?name=value&name=value
        Post sends the form-data as an HTTP post transaction vi the server
        driver.get( "https://www.selenium.dev/" )
        webDriver.find_elements( By.CSS_SELECTOR, 'input[type="text"]' )

        Pressing the browser’s back button
        driver.back()

        Pressing the browser’s forward button
        driver.forward()

        Refresh the current page
        driver.refresh()

    Get Browser Information
        Current page title from the browser
        driver.title

        Read the current URL from the browser’s address bar
        driver.current_url

    Waiting
        Explicit waits allow you to wait for a condition to occur
        WebDriverWait(driver, timeout=10).until(document_initialised)
        WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.TAG_NAME,"p"))
        waitResult = WebDriverWait( driver, timeout=5 ).until( EC.element_to_be_clickable( ( By.ID, "twotabsearchtextbox" ) ) )

        Expected Conditions
            https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html?highlight=expected

        Implicit Wait
            driver.implicitly_wait( )

    Find an element
        text_box = driver.find_element(by=By.NAME, value="my-text")
        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    End the session
        driver.quit()

'''

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# Flask Imports
from flask import Flask, render_template, request
# Python Imports
import time


app = Flask(__name__)


service = Service( executable_path = './webdrivers/geckodriver' )


htmlDict = { "amazon": [    # Search URL [0]
                            'https://www.amazon.com/s?k=',  
                            # Product Listing CSS Selector to grab html of product container [1]
                            '[data-component-type="s-search-result"]',
                            # Product Rating String Start [2]
                            'class="a-icon-alt">',
                            # Product Rating String End [3]
                            '<',
                            # Price String Start [4]
                            'class=\"a-price-whole\">',
                            #Price String End [5]
                            '<',
                            # Product Listing Link CSS Selector [6]
                            'class=\"a-link-normal',
                            # If not empty this is prefixed to the product listing link [7]
                            'https://www.amazon.com' ],

            "bestbuy": [    # Search URL [0]
                            'https://www.bestbuy.com/site/searchpage.jsp?st=',
                            # Product Listing CSS Selector to grab html of product container [1]
                            '[class="sku-item"]',
                            # Product rating String Start [2]
                            'class="visually-hidden">',
                            # Product Rating String End [3]
                            '<',
                            # Price String Start [4]
                            #'<div class="priceView-hero-price priceView-customer-price"><span aria-hidden="true">',
                            'data-testid="customer"-price"><span aria-hidden="true">',
                            #Price String End [5]
                            '</span',
                            # Product Listing Link CSS Selector [6]
                            'class="image-link"',
                            # If not empty this is prefixed to the product listing link [7]
                            'https://www.bestbuy.com' ],

            "newegg": [     # Search URL [0]
                            'https://www.newegg.com/p/pl?d=',
                            # Product Listing CSS Selector to grab html of product container [1]
                            '[class="item-cell"]',
                            # Product rating String Start [2]
                            'aria-label="rated',
                            # Product Rating String End [3]
                            '\"></',
                            # Price String Start [4]
                            '<span class="price-current-label"></span>$<strong>',
                            # Price String End [5]
                            '</strong>',
                            # Product Listing Link CSS Selector [6]
                            '<a',
                            # If not empty this is prefixed to the product listing link [7]
                            '' ],

            "walmart": [   # Search URL [0]
                            'https://www.walmart.com/search?q=',
                            # Product Listing CSS Selector to grab html of product container [1]
                            '[class="mb1 ph1 pa0-xl bb b--near-white w-25"]',
                            # Product rating String Start [2]
                            '<spand class="w_iUH7">',
                            # Product Rating String End [3]
                            'Stars.',
                            # Price String Start [4]
                            '<span class="w_iUH7">current price Now $',
                            # Price String End [5]
                            '</span>',
                            # Product Listing Link CSS Selector [6]
                            '<a',
                            # If not empty this is prefixed to the product listing link [7]
                            '' ]
            #"etsy": [],
            #"macys": [],
            #"rei":[]
            #"backcountry": []
           }

htmlInfoDict = {
                "amazon": [ #[ 0 ]: Product Listing Title
                            #[ 1 ]: Product Listing Rating
                            #[ 2 ]: Product Listing Price
                            #[ 3 ]: Product Listing Image src
                            #[ 4 ]: Product Listing Link 
                          ],
                "bestbuy": [],
                "newegg": [],
                "walmart": []
                #"etsy": [],
                #"macys": [],
                #"rei":[]
               }


def amazon( webDriver, searchTerm ):

    # list to insert into the corresponding dictionary list
    scrapedInfo = []
    # list to hold strings grabbed as text info from product listing html elements
    scrapedStringHolder = []
    searchTermSplit = searchTerm.rsplit( " ", -1 )

    fullTime = 0

    for l in htmlDict.keys():

        websiteTimeStart = time.perf_counter()

        # Searching the retailer corresponding to the current loop's dictionary key
        print( htmlDict[ l ][ 0 ].upper() + searchTerm.upper() )
        webDriver.get( htmlDict[ l ][ 0 ] + searchTerm )
        
        # Grabbing each product listing's HTML
        amazonResults = webDriver.find_elements( By.CSS_SELECTOR, htmlDict[ l ][ 1 ] )

        # Looping through each search result entry, should correspond to each product listing
        # Should have the name, price, and reviews of each product
        for i in amazonResults:
            if len( htmlInfoDict[ l ] ) > 15:
                break

            # Grabbing the HTML for the current product listing 
            innerHTML = i.get_attribute( "innerHTML" )
            # print( l + ": " + innerHTML )

            # print("Product Text: " + i.text)
            # print("--------------------------------------")

            #-------------------------Finding the Title---------------------------------#
            # Looping over each product listing text split by a newline character in a list
            # SHOULD PROBABLY USE SET OR UNION INSTEAD OF LOOPING
            for j in i.text.rsplit( "\n" ):
                # Looping over searchTerm finding the string with all tags included
                for k in searchTermSplit:
                    # Checking to see if every word in the search term is in a string from the
                    #       product listing
                    if j.upper().find( k.upper() ) == ( -1 ):
                        # If there is a search term not in the current product listing string
                        #       the loop is broken out of
                        #print( "I AM NOT THE TITLE: " + j )
                        break
                #print( "SEARCHTERMSPLIT[ -1 ]: " + searchTermSplit[-1] )
                #print( "K: " + k )
                if k.upper() == searchTermSplit[-1].upper() and j.upper().find( k.upper() ) != ( -1 ):
                    #add it to the dictionary
                    #print( "I AM THE TITLE: " + j )
                    scrapedInfo.append( j )
                    break

            #---------------------------Finding the rating--------------------------------#
            if innerHTML.find( htmlDict[l][2] ) > ( -1 ) and len( scrapedInfo ) > 0:
                ratingBeginning = innerHTML.find( htmlDict[l][2] ) + len( htmlDict[l][2] )#innerHTML[ innerHTML.find( htmlDict[l][2] ) : -1 ].find( ">" ) + 1
                ratingEnd = innerHTML.find( htmlDict[l][2] ) + innerHTML[ innerHTML.find( htmlDict[l][2] ) : -1 ].find( htmlDict[l][3] )
                #print( "RATING: " + innerHTML[ ratingBeginning : ratingEnd ] )
                scrapedInfo.append( innerHTML[ ratingBeginning : ratingEnd ] )
            elif innerHTML.find( htmlDict[l][2] ) == ( -1 ) and len( scrapedInfo ) > 0:
                scrapedInfo.append( "No Reviews" )

            #---------------------------Finding the price---------------------------------#
            if innerHTML.find( htmlDict[l][4] ) > ( -1 ) and len( scrapedInfo ) > 0: 
                priceBeginning = innerHTML.find( htmlDict[l][4] ) + len( htmlDict[l][4] ) #innerHTML[ innerHTML.find( htmlDict[l][3] ) : -1 ].find( ">" ) + 1
                priceEnd = innerHTML.find( htmlDict[l][4] ) + innerHTML[ innerHTML.find( htmlDict[l][4] ) : -1 ].find( htmlDict[l][5] )
                #print( "PRICE: " + innerHTML[ priceBeginning : priceEnd ] )
                scrapedInfo.append( innerHTML[ priceBeginning : priceEnd ].strip( '$' ) )
            elif innerHTML.find( htmlDict[l][4] ) == ( -1 ) and len( scrapedInfo ) > 0:
                scrapedInfo.append( "No Price Somehow" )

            #----------------------------Finding product image-----------------------------#
            if innerHTML.find( 'img' ) > ( -1 ) and len( scrapedInfo ) > 0:
                imgBeginning = innerHTML.find( "img" ) + innerHTML[ innerHTML.find( "img" ) : -1 ].find( "src=\"" ) + 5
                imgEnd = innerHTML.find( "img" ) + innerHTML[ innerHTML.find( "img" ) : -1 ].find( "src=\"" ) + 5 + innerHTML[ innerHTML.find( "img" ) + innerHTML[ innerHTML.find( "img" ) : -1 ].find( "src=\"" ) + 5 : -1 ].find( "\"" )
                #print( "IMAGE: " + innerHTML[ imgBeginning : imgEnd ] )
                scrapedInfo.append( innerHTML[ imgBeginning : imgEnd ] )
            elif innerHTML.find( "img" ) == ( -1 ) and len( scrapedInfo ) > 0:
                scrapedInfo.append( "No Product Image" )

            #--------------------Finding the link to the product page----------------------#
            if innerHTML.find( htmlDict[l][6] ) > ( -1 ) and len( scrapedInfo ) > 0:
                linkBeginning = innerHTML.find( htmlDict[l][6] ) + innerHTML[ innerHTML.find( htmlDict[l][6] ) : -1 ].find( "href" ) + 6
                linkEnd = innerHTML.find( htmlDict[l][6] ) + innerHTML[ innerHTML.find( htmlDict[l][6] ) : -1 ].find( "href" ) + 6 + innerHTML[ innerHTML.find( htmlDict[l][6] ) + innerHTML[ innerHTML.find( htmlDict[l][6] ) : -1 ].find( "href" ) + 6 : -1 ].find( "\"" )
                #print( "PRODUCT LINK: " + innerHTML[ linkBeginning : linkEnd ] )
                scrapedInfo.append( htmlDict[l][7] + innerHTML[ linkBeginning : linkEnd ] )
            elif innerHTML.find( htmlDict[l][6] ) == ( -1 ) and len( scrapedInfo ) > 0:
                scrapedInfo.append( "No Product Link" )

            #print( "scrapedInfo: " + str( scrapedInfo ) )

            if len( scrapedInfo ) > 0:
                htmlInfoDict[l].append( scrapedInfo.copy() ) 
                #print( "HTMLINFODICT[" + l + "]: " + str( htmlInfoDict[l] ) )

            scrapedInfo.clear()
            # print( "----------------" + l + "-------------------" )
        websiteTimeEnd = time.perf_counter()
        print(l + " Processing Time: "+ str(websiteTimeEnd - websiteTimeStart) +" seconds")
        fullTime = fullTime + ( websiteTimeEnd - websiteTimeStart )
    print("Total Processing Time: " + str(fullTime) + " seconds")
        


@app.route("/", methods=[ "GET" ] )
def index():
    #userInput = "Search"
    #return render_template( "search.html", input_text=userInput )
    return render_template( "index.html" )


@app.route( "/search", methods=[ "GET" ] )
def search():
    userInput = request.args.get( "input_text" )
    print( "Text input received: ", userInput )
    
    for i in htmlInfoDict.keys():
        htmlInfoDict[ i ].clear()

    # Using Selenium to grab info from marketplace and retailer websites
    driver = webdriver.Firefox( service = service )
    driver.minimize_window()
    amazon( driver, userInput )
    driver.close()
    #driver.quit() #cannot quit while still wanting to use the webdriver

    return render_template( "search.html", input_text=userInput, htmlInfoDict=htmlInfoDict )


