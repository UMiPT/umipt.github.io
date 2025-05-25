templatefilename = "./summertemplate.html"
datafilename = "./summer2025.csv"

import requests
from bs4 import BeautifulSoup

def getkattisscore(username="xizheli"):
    url = f"https://open.kattis.com/users/{username}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        score_element = soup.find('span', string='Score')
        #print(score_element)
        if score_element:
            score_value_element = score_element.find_next_sibling('span')
            #print(score_value_element)
            if score_value_element:
                #print("test", score_value_element.text.strip())
                return float(score_value_element.text.strip())
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the URL: {e}")
        return None


def printrow(a, header=False):
    print("<tr>")
    for x in a:
        if header:
            print("<th>" + str(x) + "</th>")
        else:
            print("<td>" + str(x) + "</td>")
    print("</tr>")

def printtable():
    print("<table>")

    printrow(["Name", "Kattis", "Codeforces", "Weekly", "Misc", "Total"], True)

    data = []
    with open(datafilename) as dfile:
        for line in dfile.read().split('\n'):
            a = line.split(',')
            kscore = round(max(0, getkattisscore(a[1]) - float(a[3])), 2)
            cscore = int(a[4])
            mscore = int(a[5])
            weeklyscore = int(a[6])
            data.append((a[0], kscore, cscore, weeklyscore, mscore, kscore+cscore+mscore+weeklyscore))
    data.sort(key=lambda x: -1*x[4])
    for a in data:
        printrow(a)

    print("</table>")


with open(templatefilename) as template:
    for line in template.read().split('\n'):
        if "INDICATOR" in line:
            printtable()
        else:
            print(line)