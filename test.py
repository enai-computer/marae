from bs4 import BeautifulSoup
import requests

if __name__ == "__main__":
    
    # load html from file
    with open('test.html', 'r') as file:
        web_html = file.read()
        soup = BeautifulSoup(web_html, 'html.parser')
        content = soup.get_text()
        print(content)

