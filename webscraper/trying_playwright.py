from playwright.sync_api import sync_playwright
import time

import threading
import csv

def page_scrape(links):
  # Start Playwright and open the browser
  with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Get Content
    for link in links:
      page.goto(link)

      imgs = page.query_selector_all('img.x5yr21d')
      img_links = set()

      for img in imgs:
          src = img.get_attribute('src')
          img_links.add(src)

      set_str = ','.join(map(str, img_links))

      pageText = page.locator('h1')
      parent_div = pageText.locator('xpath=ancestor::div[2]')
      try:
        page.locator('"See more"').click()
      except:
        print('see more no work')
      house_content = parent_div.inner_text()

      fields = [str(link), set_str, str(house_content)]
      with open('data.csv', 'a', newline='') as f:
          writer = csv.writer(f)
          writer.writerow(fields)

    # Close the browser
    browser.close()

def ads_scape():
  with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Navigate to the page
    page.goto('https://www.facebook.com/marketplace/kingston-ca/propertyrentals?exact=false&latitude=44.2417&longitude=-76.4918&radius=6')

    hrefs = []

    for i in range(5): #make the range as long as needed
      page.wait_for_selector('[class="x1xfsgkm xqmdsaz x1cnzs8 x1mtsufr x1w9j1nh"]')
      locators = page.locator('[class="x1xfsgkm xqmdsaz x1cnzs8 x1mtsufr x1w9j1nh"] a')
     
      el_count = locators.count()

      for index in range(el_count):
          element = locators.nth(index)
          href = element.get_attribute('href')
          hrefs.append(f"https://www.facebook.com{href}" )
      
      page.mouse.wheel(0, 15000)
      time.sleep(4)

    print(el_count)
    browser.close() 
    return hrefs
  
# def img_scrape():
#   # Start Playwright and open the browser
#   with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto('https://www.facebook.com/marketplace/item/834003301733362/?ref=browse_tab&referral_code=marketplace_top_picks&referral_story_type=top_picks')

#     imgs = page.query_selector_all('img.x5yr21d')

#     img_links = set()

#     for img in imgs:
#         src = img.get_attribute('src')
#         img_links.add(src)
        
#     # Close the browser
#     browser.close()

#     return img_links
  
links = ads_scape()
# links = ['https://www.facebook.com/marketplace/item/1030218307743179/?ref=category_feed&referral_code=undefined&referral_story_type=listing&tracking=%7B%22qid%22%3A%22-2601182824120432955%22%2C%22mf_story_key%22%3A%224666578103365823%22%2C%22commerce_rank_obj%22%3A%22%7B%5C%22target_id%5C%22%3A4666578103365823%2C%5C%22target_type%5C%22%3A0%2C%5C%22primary_position%5C%22%3A0%2C%5C%22ranking_signature%5C%22%3A1206448138199904941%2C%5C%22commerce_channel%5C%22%3A504%2C%5C%22value%5C%22%3A0.0033120060136327%2C%5C%22candidate_retrieval_source_map%5C%22%3A%7B%5C%224666578103365823%5C%22%3A204%7D%7D%22%2C%22ftmd_400706%22%3A%22111112l%22%7D', 'https://www.facebook.com/marketplace/item/872224390762876/?ref=category_feed&referral_code=undefined&referral_story_type=listing&tracking=%7B%22qid%22%3A%22-2601182824120432955%22%2C%22mf_story_key%22%3A%226912205375540831%22%2C%22commerce_rank_obj%22%3A%22%7B%5C%22target_id%5C%22%3A6912205375540831%2C%5C%22target_type%5C%22%3A0%2C%5C%22primary_position%5C%22%3A27%2C%5C%22ranking_signature%5C%22%3A1206448138199904941%2C%5C%22commerce_channel%5C%22%3A504%2C%5C%22value%5C%22%3A0.0023700778720468%2C%5C%22candidate_retrieval_source_map%5C%22%3A%7B%5C%226912205375540831%5C%22%3A204%7D%7D%22%2C%22ftmd_400706%22%3A%22111112l%22%7D']
length = len(links) // 2
# page_scrape(links)

thread1 = threading.Thread(target=page_scrape, args=(links[:length],))
thread2 = threading.Thread(target=page_scrape, args=(links[length:],))

# Start the threads
thread1.start()
thread2.start()

# Wait for the threads to finish
thread1.join()
thread2.join()