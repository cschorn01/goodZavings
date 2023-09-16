''' MySmartPrice Clone Aimed at the United State
    Web Scrape the Info from major brands to find the best deal based
        a search input such as "iphone", or "TV"
    Use affiliate links, ads, and product features to make money

    CLI command to flask run on zsh: python3 -m flask --app goodZavings run

    Version : Numpy Library Use, 25 to 30 seconds
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
import numpy as np


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
            innerHTML = np.array( [i.get_attribute( "innerHTML" )] )
            # print( innerHTML )

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
            if np.char.find( innerHTML,  htmlDict[l][2] ) > ( -1 ) and len( scrapedInfo ) > 0:
                ratingBeginning = np.char.find( innerHTML,  htmlDict[l][2] )[0] + len( htmlDict[l][2] )
                ratingEnd = np.char.find( innerHTML,  htmlDict[l][3], ratingBeginning, -1 )[0]
                print("Rating Beginning: " + str( ratingBeginning ) + str( type( ratingBeginning ) ) )
                print("Rating End: " + str( ratingEnd ) + str( type( ratingEnd ) ) )
                scrapedInfo.append( str( innerHTML[ ratingBeginning : ratingEnd ] ) )
                for q in scrapedInfo:
                    print( "RATING: " + str( q ) )
            elif np.char.find( innerHTML,  htmlDict[l][2] ) == ( -1 ) and len( scrapedInfo) > 0:
                scrapedInfo.append( "No Reviews" )

            #---------------------------Finding the price---------------------------------#
            if np.char.find( innerHTML,  htmlDict[l][4] ) > ( -1 ) and len( scrapedInfo ) > 0: 
                priceBeginning = np.char.find( innerHTML,  htmlDict[l][4] )[0] + len( htmlDict[l][4] )
                priceEnd = np.char.find( innerHTML,  htmlDict[l][5], priceBeginning, -1 )[0]
                print("Price Beginning: " + str( priceBeginning ) + str( type( priceBeginning ) ) )
                print("Price End: " + str( priceEnd ) + str( type( priceEnd ) ) )
                scrapedInfo.append( str( innerHTML[ priceBeginning : priceEnd ] ) )
                for q in scrapedInfo:
                    print( "PRICE: " + str( q ) )
            elif np.char.find( innerHTML,  htmlDict[l][4] ) == ( -1 ) and len( scrapedInfo) > 0:
                scrapedInfo.append( "No Price" )

            #----------------------------Finding product image-----------------------------#
            if np.char.find( innerHTML,  'img' ) > ( -1 ) and len( scrapedInfo ) > 0:
                imgBeginning = np.char.find( innerHTML,  "src=\"", np.char.find( innerHTML,  "img" )[0] + 5, -1 )[0]
                imgEnd = np.char.find( innerHTML, "\"", imgBeginning, -1 )[0]
                print("Image Beginning: " + str( imgBeginning ) + str( type( imgBeginning ) ) )
                print("Image End: " + str( imgEnd ) + str( type( imgEnd ) ) )
                scrapedInfo.append( str( innerHTML[ imgBeginning : imgEnd ] ) )
                for q in scrapedInfo:
                    print( "IMAGE: " + str( q ) )
            elif np.char.find( innerHTML,  "img" ) == ( -1 ) and len( scrapedInfo ) > 0:
                scrapedInfo.append( "No Product Image" )

            #--------------------Finding the link to the product page----------------------#
            if np.char.find( innerHTML,  htmlDict[l][6] ) > ( -1 ) and len( scrapedInfo ) > 0:
                linkBeginning = np.char.find( innerHTML, "href", np.char.find( innerHTML,  htmlDict[l][6] ), -1 )[0] + 6
                linkEnd = np.char.find( innerHTML, "\"", linkBeginning, -1 )[0]
                print("Link Beginning: " + str( linkBeginning ) + str( type( linkBeginning ) ) )
                print("Link End: " + str( linkEnd ) + str( type( linkEnd ) ) )
                scrapedInfo.append( htmlDict[l][7] + str( innerHTML[ linkBeginning : linkEnd ]))
                for q in scrapedInfo:
                    print( "PRODUCT LINK: " + str( q ) )
            elif np.char.find( innerHTML,  htmlDict[l][6] ) == ( -1 ) and len( scrapedInfo) > 0:
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
    return """<html>
                <head>
                  <style>
                    form {
                      display: flex; /* defines flex container */
                      flex-direction: row; /* establishes the flexbox main-axis */
                      flex-wrap: nowrap; /* allow the items to wrap as needed */
                      justify-content: center; /* defines alignment on flexbox main axis */
                      align-items: stretch; /* defines behavior for flex items on cross axis */
                      align-content: center; /* aligns flexbox lines through extra space */
                      width: 100%;
                      /* height: 30%; */
                    }
                  </style>
                  <title> Search </title>
                </head>
                <body>
                  <form  action="/search" method="get">
                    <input type="text" name="input_text" placeholder="Search...">
                    <input type="submit" value="Submit">
                  </form>
                </body>
              </html> """


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

'<div class="sg-col-inner"><div cel_widget_id="MAIN-SEARCH_RESULTS-3" class="s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results_1" data-csa-c-pos="1" data-csa-c-item-id="amzn1.asin.1.B005HG9ESG" data-csa-op-log-render="" data-csa-c-type="item">\n\n\n<div data-component-type="s-impression-logger" data-component-props="{&quot;percentageShownToFire&quot;:&quot;50&quot;,&quot;batchable&quot;:true,&quot;requiredElementSelector&quot;:&quot;.s-image:visible&quot;,&quot;url&quot;:&quot;https://unagi-na.amazon.com/1/events/com.amazon.eel.SponsoredProductsEventTracking.prod?qualifier=1693169832&amp;id=1531710636623603&amp;widgetName=sp_atf&amp;adId=200028189557171&amp;eventType=1&amp;adIndex=0&quot;}" class="rush-component s-expand-height">\n    \n\n\n<div data-component-type="s-impression-counter" data-component-props="{&quot;presenceCounterName&quot;:&quot;sp_delivered&quot;,&quot;testElementSelector&quot;:&quot;.s-image&quot;,&quot;hiddenCounterName&quot;:&quot;sp_hidden&quot;}" class="rush-component s-featured-result-item s-expand-height">\n    <div class="s-card-container s-overflow-hidden aok-relative puis-expand-height puis-include-content-margin puis puis-v1g4cn23aiw4pq21ytu1qia8qu3 s-latency-cf-section s-card-border"><div class="a-section a-spacing-base"><div class="s-product-image-container aok-relative s-text-center s-image-overlay-grey puis-image-overlay-grey s-padding-left-small s-padding-right-small puis-spacing-small s-height-equalized puis puis-v1g4cn23aiw4pq21ytu1qia8qu3"><span data-component-type="s-product-image" class="rush-component" data-version-id="v1g4cn23aiw4pq21ytu1qia8qu3" data-render-id="r113fnfs2i4fdc2pmd08slejs25"><a class="a-link-normal s-no-outline" href="/sspa/click?ie=UTF8&amp;spc=MToxNTMxNzEwNjM2NjIzNjAzOjE2OTMxNjk4MzI6c3BfYXRmOjIwMDAyODE4OTU1NzE3MTo6MDo6&amp;url=%2FEssentia-Water-Electrolytes-Rehydration-Overachievers%2Fdp%2FB005HG9ESG%2Fref%3Dsr_1_1_sspa%3Fkeywords%3Dwater%26qid%3D1693169832%26rdc%3D1%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1"><div class="a-section aok-relative s-image-square-aspect"><img class="s-image" src="https://m.media-amazon.com/images/I/81QJejt5LrL._AC_UL320_.jpg" srcset="https://m.media-amazon.com/images/I/81QJejt5LrL._AC_UL320_.jpg 1x, https://m.media-amazon.com/images/I/81QJejt5LrL._AC_UL480_FMwebp_QL65_.jpg 1.5x, https://m.media-amazon.com/images/I/81QJejt5LrL._AC_UL640_FMwebp_QL65_.jpg 2x, https://m.media-amazon.com/images/I/81QJejt5LrL._AC_UL800_FMwebp_QL65_.jpg 2.5x, https://m.media-amazon.com/images/I/81QJejt5LrL._AC_UL960_FMwebp_QL65_.jpg 3x" alt="Sponsored Ad - Essentia Bottled Water, 1 Liter, 12-Pack, Ionized Alkaline Water:99.9% Pure, Infused With Electrolytes, 9.5..." data-image-index="1" data-image-load="" data-image-latency="s-product-image" data-image-source-density="1"></div></a></span></div><div class="a-section a-spacing-small puis-padding-left-small puis-padding-right-small"><div class="a-section a-spacing-none a-spacing-top-small s-title-instructions-style"><div class="a-row a-spacing-micro"><span class="a-declarative" data-version-id="v1g4cn23aiw4pq21ytu1qia8qu3" data-render-id="r113fnfs2i4fdc2pmd08slejs25" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;name&quot;:&quot;sp-info-popover-B005HG9ESG&quot;,&quot;position&quot;:&quot;triggerVertical&quot;,&quot;closeButton&quot;:&quot;true&quot;,&quot;dataStrategy&quot;:&quot;preload&quot;}"><a href="javascript:void(0)" role="button" style="text-decoration: none;" aria-label="View Sponsored information or leave ad feedback" class="puis-label-popover puis-sponsored-label-text"><span class="puis-label-popover-default"><span class="a-color-secondary">Sponsored</span></span><span class="puis-label-popover-hover"><span class="a-color-base">Sponsored</span></span> <span class="aok-inline-block puis-sponsored-label-info-icon"></span></a></span><div class="a-popover-preload" id="a-popover-sp-info-popover-B005HG9ESG"><div class="puis puis-v1g4cn23aiw4pq21ytu1qia8qu3"><span>You’re seeing this ad based on the product’s relevance to your search query.</span><div class="a-row"><span class="a-declarative" data-version-id="v1g4cn23aiw4pq21ytu1qia8qu3" data-render-id="r113fnfs2i4fdc2pmd08slejs25" data-action="s-safe-ajax-modal-trigger" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-s-safe-ajax-modal-trigger" data-s-safe-ajax-modal-trigger="{&quot;header&quot;:&quot;Leave feedback&quot;,&quot;dataStrategy&quot;:&quot;ajax&quot;,&quot;ajaxUrl&quot;:&quot;/af/sp-loom/feedback-form?pl=%7B%22adPlacementMetaData%22%3A%7B%22searchTerms%22%3A%22d2F0ZXI%3D%22%2C%22pageType%22%3A%22Search%22%2C%22feedbackType%22%3A%22sponsoredProductsLoom%22%2C%22slotName%22%3A%22TOP%22%7D%2C%22adCreativeMetaData%22%3A%7B%22adProgramId%22%3A1024%2C%22adCreativeDetails%22%3A%5B%7B%22asin%22%3A%22B005HG9ESG%22%2C%22title%22%3A%22Essentia+Bottled+Water%2C+1+Liter%2C+12-Pack%2C+Ionized+Alkaline+Water%3A99.9%25+Pure%2C+Infused+With+Electrolyt%22%2C%22priceInfo%22%3A%7B%22amount%22%3A23.77%2C%22currencyCode%22%3A%22USD%22%7D%2C%22sku%22%3A%22B005HG9ESG%22%2C%22adId%22%3A%22A00182693CDBXTCH369CN%22%2C%22campaignId%22%3A%22A04332396898N104O7N4%22%2C%22advertiserIdNS%22%3Anull%2C%22selectionSignals%22%3Anull%7D%5D%7D%7D&quot;}"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style" href="#"><span>Leave ad feedback</span> </a> </span></div></div></div></div><h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-3"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" href="/sspa/click?ie=UTF8&amp;spc=MToxNTMxNzEwNjM2NjIzNjAzOjE2OTMxNjk4MzI6c3BfYXRmOjIwMDAyODE4OTU1NzE3MTo6MDo6&amp;url=%2FEssentia-Water-Electrolytes-Rehydration-Overachievers%2Fdp%2FB005HG9ESG%2Fref%3Dsr_1_1_sspa%3Fkeywords%3Dwater%26qid%3D1693169832%26rdc%3D1%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1"><span class="a-size-base-plus a-color-base a-text-normal">Essentia Bottled Water, 1 Liter, 12-Pack, Ionized Alkaline Water:99.9% Pure, Infused With Electrolytes, 9.5 pH Or Higher With A Clean, Smooth Taste</span> </a> </h2><div class="a-row a-size-base a-color-secondary"><div class="a-row a-color-base"><span class="a-size-base a-color-base s-background-color-platinum a-padding-mini aok-nowrap aok-align-top aok-inline-block a-spacing-top-micro puis-medium-weight-text">Alkaline</span><span class="a-letter-space"></span><span class="a-size-base a-color-base s-background-color-platinum a-padding-mini aok-nowrap aok-align-top aok-inline-block a-spacing-top-micro puis-medium-weight-text">33.8 Fl Oz (Pack of 12)</span></div></div></div><div class="a-section a-spacing-none a-spacing-top-micro"><div class="a-row a-size-small"><span aria-label="4.8 out of 5 stars"><span class="a-declarative" data-version-id="v1g4cn23aiw4pq21ytu1qia8qu3" data-render-id="r113fnfs2i4fdc2pmd08slejs25" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;position&quot;:&quot;triggerBottom&quot;,&quot;popoverLabel&quot;:&quot;&quot;,&quot;url&quot;:&quot;/review/widgets/average-customer-review/popover/ref=acr_search__popover?ie=UTF8&amp;asin=B005HG9ESG&amp;ref=acr_search__popover&amp;contextId=search&quot;,&quot;closeButton&quot;:false,&quot;closeButtonLabel&quot;:&quot;&quot;}"><a href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative"><i class="a-icon a-icon-star-small a-star-small-5 aok-align-bottom"><span class="a-icon-alt">4.8 out of 5 stars</span></i><i class="a-icon a-icon-popover"></i></a></span> </span><span aria-label="36,628"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style" href="/sspa/click?ie=UTF8&amp;spc=MToxNTMxNzEwNjM2NjIzNjAzOjE2OTMxNjk4MzI6c3BfYXRmOjIwMDAyODE4OTU1NzE3MTo6MDo6&amp;url=%2FEssentia-Water-Electrolytes-Rehydration-Overachievers%2Fdp%2FB005HG9ESG%2Fref%3Dsr_1_1_sspa%3Fkeywords%3Dwater%26qid%3D1693169832%26rdc%3D1%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1#customerReviews"><span class="a-size-base s-underline-text">36,628</span> </a> </span></div><div class="a-row a-size-base"><span class="a-size-base a-color-secondary">40K+ bought in past month</span></div></div><div class="a-section a-spacing-none a-spacing-top-small s-price-instructions-style"><div class="a-row a-size-base a-color-base"><a class="a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal" href="/sspa/click?ie=UTF8&amp;spc=MToxNTMxNzEwNjM2NjIzNjAzOjE2OTMxNjk4MzI6c3BfYXRmOjIwMDAyODE4OTU1NzE3MTo6MDo6&amp;url=%2FEssentia-Water-Electrolytes-Rehydration-Overachievers%2Fdp%2FB005HG9ESG%2Fref%3Dsr_1_1_sspa%3Fkeywords%3Dwater%26qid%3D1693169832%26rdc%3D1%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1"><span class="a-price" data-a-size="xl" data-a-color="base"><span class="a-offscreen">$23.77</span><span aria-hidden="true"><span class="a-price-symbol">$</span><span class="a-price-whole">23<span class="a-price-decimal">.</span></span><span class="a-price-fraction">77</span></span></span> <span class="a-size-base a-color-secondary">($0.06/Fl Oz)</span> </a> </div><div class="a-row a-size-base a-color-secondary"><div class="a-row"><span>$22.58 with Subscribe &amp; Save discount</span></div><div class="a-row"><span data-component-type="s-coupon-component" class="rush-component" data-component-props="{&quot;asin&quot;:&quot;B005HG9ESG&quot;}" data-version-id="v1g4cn23aiw4pq21ytu1qia8qu3" data-render-id="r113fnfs2i4fdc2pmd08slejs25"><span class="s-coupon-clipped aok-hidden"><span class="a-color-base">&lt;label&gt;Extra 20% off&lt;/label&gt; when you subscribe</span></span><span class="s-coupon-unclipped"><span class="a-size-base s-highlighted-text-padding aok-inline-block s-coupon-highlight-color">Extra 20% off</span> <span class="a-color-base"> when you subscribe</span></span></span> </div></div><div class="a-row a-size-base a-color-secondary"><span class="a-text-bold">SNAP EBT eligible</span></div></div><div class="a-section a-spacing-none a-spacing-top-micro"><div class="a-row a-size-base a-color-secondary s-align-children-center"><div class="a-row s-align-children-center"><span class="aok-inline-block s-image-logo-view"><span class="aok-relative s-icon-text-medium s-prime"><i class="a-icon a-icon-prime a-icon-medium" role="img" aria-label="Amazon Prime"></i></span><span></span></span> </div><div class="a-row"><span aria-label="FREE delivery Sat, Sep 2 on $35 of items shipped by Amazon"><span class="a-color-base">FREE delivery </span><span class="a-color-base a-text-bold">Sat, Sep 2 </span><span class="a-color-base">on $35 of items shipped by Amazon</span></span></div><div class="a-row"><span aria-label="Or fastest delivery Wed, Aug 30 "><span class="a-color-base">Or fastest delivery </span><span class="a-color-base a-text-bold">Wed, Aug 30 </span></span></div></div></div></div></div></div>\n</div>\n\n</div>\n</div></div>'
