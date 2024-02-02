import requests
from bs4 import BeautifulSoup

# url= 'https://www.ecb.europa.eu/press/pr/date/html/index.en.html'
def get_get_all_ecb_meeting(url : str) : 

    # Get the page content thanks to a HTTP request
    response = requests.get(url)

    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

        section_div = soup.find('div', class_= 'definition-list -filter')

        lazyload_container = section_div.find('dl', id= "lazyload-container" )

        snippets_urls = lazyload_container['data-snippets'].split(',')

        for snippet_url in snippets_urls:
            full_url = "https://www.ecb.europa.eu/press/pr/date/" +  snippet_url[3:]
            
            snippet_response = requests.get(full_url)

            if snippet_response.status_code == 200:
                # Parsez le contenu et ajoutez-le à votre document
                snippet_soup = BeautifulSoup(snippet_response.content, 'html.parser')
                lazyload_container.append(snippet_soup)
                
    return lazyload_container
            

def get_link_monetary_policy_decision(container, dates_press_conferences, target_category :str = "MONETARY POLICY DECISION"):
    
    date_tags = container.find_all('dt', {'isodate': dates_press_conferences})

    links_to_visit = []
    monetary_policy_decision_dates = []

    for date_tag in date_tags:
        dd_tag = date_tag.find_next('dd')

        category_div = dd_tag.find('div', class_='category')
        title_div = dd_tag.find('div', class_='title')

        if category_div and title_div:
            if category_div.get_text() == target_category:
                # Find the link within the title_div
                link = title_div.find('a')
                if link is not None:
                    href_value = link.get('href')
                    href_ecb = "https://www.ecb.europa.eu"+href_value
                    links_to_visit.append(href_ecb)
                    monetary_policy_decision_dates.append(date_tag)

    return links_to_visit, monetary_policy_decision_dates


def scrapping_load_text(url):
    stop_text="The President of the ECB will comment" # Get the page content thanks to a HTTP request
    response = requests.get(url)

    # Verify the request is satisfied
    if response.status_code == 200:
        # Analyze the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p', class_=lambda x: x != 'ecb-publicationDate')
    
    # create concatenated storage
        concatenated_text = ""

        for paragraph in paragraphs:
            # Check if the text contains "disclaimer"
            if stop_text.lower() in paragraph.text.lower():                
                break  # Stop scraping when disclaimer is found

            # Check if the text contains '*', and skip the paragraph if it does
            if '*' in paragraph.text:
                continue

            concatenated_text += paragraph.text

        return concatenated_text