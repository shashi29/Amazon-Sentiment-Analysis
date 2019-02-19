from lxml import html  
import requests
import pandas as pd

count = 0
reviews_df = pd.DataFrame()

for i in range(1,100):
    #amazon_url = 'https://www.amazon.com/product-reviews/B01DFKC2SO?pageNumber='+str(i)
    amazon_url = 'https://www.amazon.in/Orient-Electric-Apex-FX-1200mm-Ceiling/product-reviews/B01M0505SJ/ref=cm_cr_arp_d_paging_btm_next_2?showViewpoints=1&pageNumber='+str(i)
    print(amazon_url)

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    
    headers = {'User-Agent': user_agent}
    page = requests.get(amazon_url, headers = headers)
    parser = html.fromstring(page.content)
    
    xpath_reviews = '//div[@data-hook="review"]'
    reviews = parser.xpath(xpath_reviews)
    
    xpath_rating  = './/i[@data-hook="review-star-rating"]//text()' 
    xpath_title   = './/a[@data-hook="review-title"]//text()'
    xpath_author  = './/a[@data-hook="review-author"]//text()'
    xpath_date    = './/span[@data-hook="review-date"]//text()'
    xpath_body    = './/span[@data-hook="review-body"]//text()'
    xpath_helpful = './/span[@data-hook="helpful-vote-statement"]//text()'
    
    
    for review in reviews:
        count = count + 1
        rating  = review.xpath(xpath_rating)
        title   = review.xpath(xpath_title)
        author  = review.xpath(xpath_author)
        date    = review.xpath(xpath_date)
        body    = review.xpath(xpath_body)
        helpful = review.xpath(xpath_helpful)
    
        review_dict = {'rating': rating,
                       'title': title,
                       #'author': author,             
                       'date': date,
                       'body': body
                       #'helpful': helpful
                       }
        #print(review_dict)
        reviews_df = reviews_df.append(review_dict ,ignore_index=True)
        
reviews_df.to_csv("orient.csv")        
print(count)
