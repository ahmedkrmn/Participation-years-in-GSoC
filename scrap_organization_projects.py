import re
import requests
import csv
from bs4 import BeautifulSoup

year, organizations_url, organizations_html = "", "", ""

with open('GSoC_archives.csv', 'r') as csv_read_file:
    csv_reader = csv.reader(csv_read_file)
    next(csv_reader)  # Skip the header
    row = next(csv_reader)  # Read last year's GSoC organizations url
    year, organizations_url, organizations_html = row[0], row[1], requests.get(
        row[1]).text

# construct GSoC archive url: protocol + subdomain + domain
organizations_url = organizations_url.split('/')
gsoc_archive_url = organizations_url[0] + "//" + organizations_url[2]

soup = BeautifulSoup(organizations_html, 'html.parser')
names = soup.find_all(class_="organization-card__link")

organizations = {}

for name in names:
    organizations[name.h4.text] = gsoc_archive_url + name["href"]
#organizations = {organization_name: organization_url}

for org_name, org_url in organizations.items():
    print("parsing " + org_name)
    soup = BeautifulSoup(requests.get(org_url).text, 'html.parser')
    names = soup.find_all(class_="archive-project-card")
    organizations[org_name] = [org_url, len(names)]
#organizations = {organization_name: [organization_url, organization_project_count]}

with open('organization_projects.csv', 'w', newline='') as csv_write_file:
    csv_writer = csv.writer(csv_write_file)
    csv_writer.writerow(['Organization', 'URL', 'Number of Projects in ' + year])
    # csv_writer.writerow(['Organization', 'Number of Projects in ' + year])
    for org_name, [org_url, project_count] in sorted(organizations.items(), key=lambda x: (-x[1][1], x[0])):
        csv_writer.writerow([org_name, org_url, project_count])
        # csv_writer.writerow(["[" + org_name + "](" + org_url + ")", project_count])
