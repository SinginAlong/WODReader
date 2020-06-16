# goal of this program is to go on the web, access the BION wod list and extract the workouts for the current day

# website url is as follows
# http://www.bioncrossfit.com/wods/517/crossfit-wods-for-nov-19-24
# http://www.bioncrossfit.com/wods/515/crossfit-wods-for-nov-12-17
# http://www.bioncrossfit.com/wods/512/crossfit-wods-for-nov-5-10
# http://www.bioncrossfit.com/wods/509/crossfit-wods-for-oct-29-nov-3rd
# http://www.bioncrossfit.com/wods/507/crossfit-wods-for-oct-22-27

import datetime
import urllib.request
import re
from bs4 import BeautifulSoup

# FUNCTIONS


def extract_todays_wod(text, day):
    """takes in wod list text and the current day and returns the workout for that day"""
    text.find(day)


# SCRIPT

now = datetime.datetime.now()

print("The current day is ", str(now.day))

with urllib.request.urlopen("http://www.bioncrossfit.com/wods/517/crossfit-wods-for-nov-19-24") as response:
    html = response.read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()  # remove scripting

    # gest text
    text = soup.get_text()

    # break into lines and remove leading and trailing space
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)

    print(text)


