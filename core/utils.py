from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from .models import Opportunity
import time
from webdriver_manager.chrome import ChromeDriverManager


UNIVERSITIES = {
    "Harvard": "https://careerservices.fas.harvard.edu/channels/internships/",
    "Stanford": "https://careercenter.umich.edu/content/internships",
    "MIT": "https://capd.mit.edu/jobs-internships/",
    "Oxford": "https://www.careers.ox.ac.uk/internships",
}


def real_scraper():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without opening browser
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service("chromedriver.exe")  # Make sure driver exists
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
    )

    for uni_name, url in UNIVERSITIES.items():
        try:
            driver.get(url)
            time.sleep(3)  # wait for JS content to load

            soup = BeautifulSoup(driver.page_source, "html.parser")

            headlines = soup.find_all("h2")[:5]

            for h in headlines:
                title = h.get_text(strip=True)

                if title and not Opportunity.objects.filter(title=title).exists():

                    domain = classify_domain(title)
                    type_value = classify_type(title)

                    Opportunity.objects.create(
                        title=title,
                        organization=uni_name,
                        source=uni_name,
                        description=f"Opportunity from {uni_name}",
                        domain=domain,
                        type=type_value,
                        link=url
                    )

        except Exception as e:
            print(f"Skipping {uni_name}: {e}")
            continue

    driver.quit()


def classify_domain(title):
    title = title.lower()

    if "ai" in title or "machine" in title:
        return "AI"
    elif "law" in title:
        return "Law"
    elif "engineer" in title:
        return "Engineering"
    elif "bio" in title or "medical" in title:
        return "Biomedical"
    else:
        return "General"


def classify_type(title):
    title = title.lower()

    if "hackathon" in title:
        return "Hackathon"
    elif "internship" in title:
        return "Internship"
    elif "research" in title:
        return "Research"
    elif "conference" in title:
        return "Conference"
    else:
        return "General"