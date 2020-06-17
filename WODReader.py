# goal of this program is to go on the web, access the BION wod list and extract the workouts for the current day

# VERSIONS
# V1 - code to pull text from website, including use of BeautifulSoup
# V2 - copied to OndDrive
# V3 - bundled into functions, build_date, build_url, find_website, pull_text, & extract_todays_wods
# V4 - plan to make main script handle off days

# to do
# handle website not opening error
# create fileIO for storing last correct index


import datetime
import urllib.request
from bs4 import BeautifulSoup

#CONSTANTS
DEBUG = True  # flag for printing debug statements
WOD_TIME = datetime.time(hour=5, minute=30) # hour in 24 hour clock, not set up for seconds
INDEX_FILE = "webpage_index.dat"

# FUNCTIONS


def ordinal(n):
    return "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])


def build_date_l(today=datetime.date.today()):
    # returns a list
    """uses today's date to build what the wod date should be"""
    monday = today + datetime.timedelta(days=-today.weekday())
    saturday = monday + datetime.timedelta(days=5)

    if monday.month != saturday.month:
        r = [monday.strftime("%b") + ". " + str(ordinal(monday.day)) + " - " + \
            saturday.strftime("%b") + ". " + str(ordinal(saturday.day))]
    else:
        r = [monday.strftime("%b") + ". " + str(monday.day) + "-" + str(saturday.day),
             monday.strftime("%B") + " " + str(monday.day) + "-" + str(saturday.day)]

    return r


def build_url(index):
    return "http://www.bioncrossfit.com/wods/" + str(index) + "/"


def find_webpage_m(start_index, search_string):
    # search string will be a list
    """starting at start_index increases index until title matches search_string
    returns url of webpage, if failed returns "" """
    # possible errors: no internet, no page
    if DEBUG: print(["Looking for " + s for s in search_string])
    for i in range(0, 30):  # only try 30 indexes
        url = build_url(start_index+i)
        soup = BeautifulSoup(urllib.request.urlopen(url), features="html.parser")
        if DEBUG: print("Pulled title: " + soup.title.string)
        for s in search_string:
            if s in soup.title.string:
                return url, start_index+i
    print("Unable to find webpage")
    return "", None


def pull_text(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), features="html.parser")
    # remove script and styling elements from html
    for script in soup(["script", "style"]):
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    return "\n".join(chunk for chunk in chunks if chunk)


def extract_todays_wods(text, today):
    """uses the day name of today to get the wods of that day"""
    # will have to handle saturday different, end of wods text is different
    # will also have to handle sunday differently (just print next monday's... (no just there))
    # print next day's wods after certain time...
    start_index = text.find(today.strftime("%A"))
    end_index = text.find((today + datetime.timedelta(days=1)).strftime("%A"))
    return text[(start_index + len(today.strftime("%A"))):end_index]


def choose_day(wo_time):
    # if the current time is past wo_time (work out time, then choose tomorrow)
    now = datetime.datetime.now()
    if now.hour > wo_time.hour or now.hour == wo_time.hour and now.minute >  wo_time.minute:
        return now + datetime.timedelta(days=1)
    else:
        return now


def get_index():
    """reads file to get most recent successful webpage address"""
    default_index = 723
    try:
        f = open(INDEX_FILE, 'r')
    except FileNotFoundError:
        if DEBUG: print("Couldn't find index file")
        return default_index
    i = f.read()
    try:
        i = int(i)
    except ValueError:
        if DEBUG: print("Could not read webpage index")
        return default_index
    finally:
        f.close()
    return i


def save_index(index):
    """saves the index to the index file"""
    if index is None:
        return
    with open(INDEX_FILE, "w") as f:
        f.write(str(index))
        f.close()


# SCRIPT

# open file and read last index/or webpage

# will have to choose day to use, if sunday use monday

# day_to_use = datetime.date.today()
day_to_use = choose_day(WOD_TIME)
# day_to_use = datetime.date(2018, 11, 20)

url, index = find_webpage_m(get_index(), ["CrossFit Wods for " + s for s in build_date_l(day_to_use)])

save_index(index)

if url == "":
    print("give up")
else:
    if DEBUG: print("pulling wods from url: " + url)
    text = pull_text(url)
    wods = extract_todays_wods(text, day_to_use)
    print("\nWODS for " + day_to_use.strftime('%A'))
    print(wods)
