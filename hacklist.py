import requests
from bs4 import BeautifulSoup
import argparse

####
# Usage: `python hacklist.py jul [aug sep oct]`
# Purpose: returns a -newsletter ready- list in (HTML) of in-person hackathons that occur during the selected months.
####

# DEFINE months to check via CLI
parser = argparse.ArgumentParser(description='Get a list of Hackathons in months X, Y, Z....')
parser.add_argument('months', metavar='Months', type=str, nargs='+', help='list of 3 char month codes (e.g. jul, aug, sep)')
args = parser.parse_args()
#months = ["jul", "aug"]
months = (args.months)
print "Listing Hackathons in: "+ str(months)

# SCRAPE Hackathons from pages 1-10
api = "https://devpost.com/hackathons?utf8=%E2%9C%93&search=&challenge_type=in-person&sort_by=Submission+Deadline&page="
req_html = ""
html = "<ul>\n"

for i in range(1,11):
  #print "page:" + str(i)
  req = requests.get( api+str(i) )
  req_html = req_html + req.text

soup = BeautifulSoup(req_html, 'html.parser')
rows = soup.find_all("article", class_="challenge-listing")

# EXTRACT data from each row and add to hackathons list
for i, r in enumerate(rows):
    #print "\n"+str(i)
    #print r

    name = r.find_all('h2')[0].text.strip()
    print "\n"+name

    if any(month in r.find_all("span", class_="value date-range")[0].text.strip().lower() for month in months):
        dates = r.find_all("span", class_="value date-range")[0].text.strip()
        #print dates
    else:
        print "OUTSIDE OF DATE RANGE"
        continue # just skip out of loop if no date

    url = (r.find_all('a', class_="clearfix", href=True)[0]['href']).strip().replace("/?ref_content=featured&ref_feature=challenge&ref_medium=discover", "").replace("/?ref_content=default&ref_feature=challenge&ref_medium=discover", "")
    print url

    if r.find_all("p", class_="challenge-location"):
        location = r.find_all("p", class_="challenge-location")[0].text.strip().replace(", US", "")
        print location
    else:
        location = ""

    hack = {
        "name" : name,
        "url" : url,
        "dates" : dates,
        "location" : location
        }

    #print hack
    html = html + "  <li><a href=\""+url+"\">"+name+"</a>, "+location+"</li>\n"

# PRINT final data / HTML to console
html = html + "</ul>"
print "\n\nNewsletter HTML:\n\n" + html
