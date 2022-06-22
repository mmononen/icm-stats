import requests
from bs4 import BeautifulSoup
import sys
import datetime
import codecs

# The class TopList is a class that has a name, a total number of checks, a number of checked items, a
# number of unchecked items, and a rank
class TopList:
    def __init__(self, name):
        self.name = name
        self.total_checks = 0
        self.checked = 0
        self.unchecked = 0
        self.rank = 0
        self.percentage = 0
        self.url = ''

# Print the movie lists with different options
def print_list(topic, input_list, type, amount):
    i = 0
    returned = []
    print_list = []
    if (to_html):
        s = f'<button class="accordion">&emsp;{topic}</button>\n<div class="panel">\n<p>\n'
        returned.append(s)
    else:
        returned.append(topic)
    if not to_html:
        returned.append("-"*len(topic))
    for l in input_list:        
        if ((type == 'rank' and l.rank > 0) or (type == 'percentage' and (l.checked < l.total_checks)) or (type == 'completed' and (l.checked == l.total_checks)) or (type == 'unstarted' and (l.checked == 0)) or (type == 'under1000' and l.rank < 1000 and l.checked > 0) or (type == "biglists" and l.total_checks > 999)  or (type == "between1000and2000" and 1000 <= l.rank <= 2000)):
            i = i + 1
            print_list.append(f"{'0' + str(i) if (i<10) else i}. {'<strong>' if to_html else ''}<a href='{l.url}'>{l.name}</a>{'</strong>' if to_html else ''} ({l.checked}/{l.total_checks}) #{l.rank} ({round(l.percentage, 1)}%){'<br>' if to_html else ''}")
        if (i > (amount - 1)):
            break
    if len(print_list) > 0:
        for pl in print_list:
            returned.append(pl)
    else:
        if (to_html):
            returned.append("<p>No lists.</p>")
        else:
            returned.append("<No lists.>")
    if (to_html):
        returned.append("\n</p>\n</div>\n")
    else:
        returned.append("\n")
    return returned

# get username's progress on official lists
# Use command-line argument if available
try:
    username = sys.argv[1]
except:
    username = ''

URL = f"https://www.icheckmovies.com/profiles/progress/?user={username}"
e = datetime.datetime.now()
year_month_day = f"{e.year}-{'0' + str(e.month) if (int(e.month) < 10) else e.month}-{e.day}"
try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="progressall")
    lists = []
    final_print = []

    # Save a reference to the original standard output
    original_stdout = sys.stdout
    # True = write results to a file. False = print results to the screen
    write_results_to_file = True
    # True = output to html, use with included css and js files. False = output is a plain text file
    to_html = True
    # html header
    html_header = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<meta http-equiv="X-UA-Compatible" content="IE=edge">\n\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html_header += f"\t<title>ICM stats for {username}</title>\n"
    html_header += f'\t<link rel="stylesheet" href="style.css">\n'
    html_header += f'<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />\n'
    html_header += f"</head>\n<body>\n"
    # html footer
    html_footer = f'<script src="script.js"></script><p class="footer">Stats generated {year_month_day} by <a href="https://github.com/mmononen/icm-stats">ICM stats script</a></p></body>\n</html>\n'
    # scrape top list names and create TopList objects and append them on lists array
    lists_temp = results.find_all("h3")
    for list_name in lists_temp:
        lists.append(TopList(list_name.text.strip()))
    
    lists_temp = results.find_all("a", class_="title")
    i = 0
    for list_item in lists_temp:        
        list_item = list_item.get("href")
        lists[i].url = f'https://www.icheckmovies.com{list_item}'
        i = i + 1


    # populate rest of the TopList object properties
    lists_temp = results.find_all("span", class_="rank")
    i = 0
    for list_item in lists_temp:
        for l in list_item:
            temp = l.text.strip()
            temp = temp.split(" / ")
            if len(temp) > 1:
                lists[i].total_checks = int(temp[1])
                lists[i].checked = int(temp[0])
                lists[i].unchecked = lists[i].total_checks - lists[i].checked
                lists[i].percentage = lists[i].checked / lists[i].total_checks * 100
            else:
                if len(temp[0]) > 1:
                    s = temp[0]
                    lists[i].rank = int(s[1:])
        i = i + 1

    #uncomment to print all the lists in alphabetical order
    #lists.sort(key=lambda x: x.name.upper(), reverse=False)
    if to_html:
        final_print.append([html_header])
        final_print.append([f'<h2><a href="https://www.icheckmovies.com/">ICM</a> Statistics for <a href="{URL}">{username}</a></h2>'])

    lists.sort(key=lambda x: x.percentage, reverse=True)
    final_print.append(print_list("Top unfinished lists by completion percentage:", lists, "percentage", 20))

    lists.sort(key=lambda x: x.rank, reverse=False)
    final_print.append(print_list("Top lists by rank:", lists, "rank", 20))

    lists.sort(key=lambda x: x.rank, reverse=True)
    final_print.append(print_list("Bottom lists by rank:", lists, "rank", 20))

    lists.sort(key=lambda x: x.rank, reverse=False)
    final_print.append(print_list("Lists under rank #1000:", lists, "under1000", 300))

    final_print.append(print_list("Lists between ranks #1000 and #2000:", lists, "between1000and2000", 300))

    lists.sort(key=lambda x: x.rank, reverse=False)
    final_print.append(print_list("Big lists (1000+ movies) by rank:", lists, "biglists", 300))

    lists.sort(key=lambda x: x.checked, reverse=True)
    final_print.append(print_list("Top lists by number of checked films:", lists, "rank", 20))

    lists.sort(key=lambda x: x.name.upper(), reverse=False)
    final_print.append(print_list("Completed lists:", lists, "completed", 300))

    # No need to sort the list again
    final_print.append(print_list("Unstarted lists:", lists, "unstarted", 300))

    if to_html:
        lists.sort(key=lambda x: x.percentage, reverse=True)
        final_print.append(print_list("All lists:", lists, "percentage", 500))
        final_print.append([html_footer])

    if (write_results_to_file):   
        
        fn = f"{year_month_day}-icm-stats-{username}.{'html' if to_html else 'txt'}"
        with codecs.open(fn, 'w', 'utf-8') as f:
            sys.stdout = f
            for list_lines in final_print:
                for lines in list_lines:
                    print(lines)
            sys.stdout = original_stdout
    else:
        for list_lines in final_print:
            for lines in list_lines:
                print(lines)
except:
    print(f"{'Username is <blank>.' if len(username) < 1 else 'No results with given username.'}")