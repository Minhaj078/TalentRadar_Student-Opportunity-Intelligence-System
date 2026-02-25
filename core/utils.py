import requests
from bs4 import BeautifulSoup
from .models import Opportunity

UNIVERSITIES = {
    "Harvard": "https://careerservices.fas.harvard.edu/channels/internships/",
    "Stanford": "https://studentaffairs.stanford.edu/opportunities",
    "Princeton": "https://careerdevelopment.princeton.edu/students/internships",
    "Columbia": "https://careerservices.columbia.edu/resources/internships",
    "Yale": "https://ocs.yale.edu/channels/internships/",
    "MIT": "https://capd.mit.edu/jobs-internships/",
    "Cornell": "https://career.cornell.edu/resources/internships",
    "Brown": "https://careers.brown.edu/channels/internships/",
    "Dartmouth": "https://students.dartmouth.edu/ugar/careers/internships",
    "UPenn": "https://careerservices.upenn.edu/preparing-for-internships/",
    "Caltech": "https://career.caltech.edu/opportunities",
    "Duke": "https://careerhub.students.duke.edu/channels/internships/",
    "UCLA": "https://career.ucla.edu/resources/internships/",
    "Berkeley": "https://career.berkeley.edu/internships",
    "Oxford": "https://www.careers.ox.ac.uk/internships",
    "Cambridge": "https://www.careers.cam.ac.uk/internships",
    "Chicago": "https://careeradvancement.uchicago.edu/channels/internships/",
    "NYU": "https://www.nyu.edu/students/student-information-and-resources/career-development-and-jobs.html",
    "GeorgiaTech": "https://career.gatech.edu/students/internships-co-ops",
    "Michigan": "https://careercenter.umich.edu/content/internships",
    "Toronto": "https://studentlife.utoronto.ca/task/internships/",
    "CarnegieMellon": "https://www.cmu.edu/career/students-and-alumni/find-a-job-or-internship/index.html",
    "JohnsHopkins": "https://studentaffairs.jhu.edu/careers/students/internships/",
    "USC": "https://careers.usc.edu/students/find-an-internship/",
    "Northwestern": "https://www.northwestern.edu/careers/students/find-jobs-internships/"
}

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# def real_scraper():
#     for uni_name, url in UNIVERSITIES.items():
#         try:
#             response = requests.get(
#                 url,
#                 timeout=10,
#                 verify=False,
#                 headers={"User-Agent": "Mozilla/5.0"}
#             )

#             soup = BeautifulSoup(response.text, "html.parser")
#             headlines = soup.find_all("h2")[:3]

#             for h in headlines:
#                 title = h.get_text(strip=True)

#                 if title and not Opportunity.objects.filter(title=title).exists():
#                     domain = classify_domain(title)

#                     Opportunity.objects.create(
#                         title=title,
#                         university=uni_name,
#                         description=f"Latest update from {uni_name}",
#                         domain=domain,
#                         link=url
#                     )

#         except Exception as e:
#             print(f"Skipping {uni_name}: {e}")
#             continue

def real_scraper():
    for uni_name, url in UNIVERSITIES.items():
        try:
            response = requests.get(
                url,
                timeout=10,
                verify=False,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            soup = BeautifulSoup(response.text, "html.parser")
            headlines = soup.find_all("h2")[:3]

            for h in headlines:
                title = h.get_text(strip=True)

                if title and not Opportunity.objects.filter(title=title).exists():

                    domain = classify_domain(title)
                    type_value = classify_type(title)   # 👈 IMPORTANT

                    Opportunity.objects.create(
                        title=title,
                        university=uni_name,
                        description=f"Latest update from {uni_name}",
                        domain=domain,
                        type=type_value,               # 👈 IMPORTANT
                        link=url
                    )

        except Exception as e:
            print(f"Skipping {uni_name}: {e}")
            continue


def classify_domain(title):
    title = title.lower()

    if "ai" in title or "machine" in title:
        return "AI"
    elif "law" in title:
        return "Law"
    elif "engineer" in title:
        return "Engineering"
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