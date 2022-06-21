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

# Print the movie lists with different options
def print_list(topic, input_list, type, amount):
    i = 0
    returned = []
    print_list = []
    returned.append(topic)
    returned.append("-"*len(topic))
    for l in input_list:        
        if ((type == 'rank' and l.rank > 0) or (type == 'percentage' and (l.checked < l.total_checks)) or (type == 'completed' and (l.checked == l.total_checks)) or (type == 'unstarted' and (l.checked == 0)) or (type == 'under1000' and l.rank < 1000 and l.checked > 0) or (type == "biglists" and l.total_checks > 999)):
            i = i + 1            
            print_list.append(f"{'0' + str(i) if (i<10) else i}. {l.name} ({l.checked}/{l.total_checks}) #{l.rank} ({round(l.percentage, 1)}%)")
        if (i > (amount - 1)):
            break
    if len(print_list) > 0:
        for pl in print_list:
            returned.append(pl)
    else:
        returned.append("<No lists.>")
    returned.append("\n")
    return returned

# get username's progress on official lists
# Use command-line argument if available
try:
    username = sys.argv[1]
except:
    username = ''

URL = f"https://www.icheckmovies.com/profiles/progress/?user={username}"
try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="progressall")
    lists = []
    final_print = []

    # Save a reference to the original standard output
    original_stdout = sys.stdout
    write_results_to_file = True


    # scrape top list names and create TopList objects and append them on lists array
    lists_temp = results.find_all("h3")
    for list_name in lists_temp:
        lists.append(TopList(list_name.text.strip()))

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

    lists.sort(key=lambda x: x.percentage, reverse=True)
    final_print.append(print_list("Top unfinished lists by completion percentage:", lists, "percentage", 10))

    lists.sort(key=lambda x: x.rank, reverse=False)
    final_print.append(print_list("Top lists by rank:", lists, "rank", 10))

    lists.sort(key=lambda x: x.rank, reverse=True)
    final_print.append(print_list("Bottom lists by rank:", lists, "rank", 10))

    lists.sort(key=lambda x: x.rank, reverse=False)
    final_print.append(print_list("Top lists under rank #1000:", lists, "under1000", 300))

    lists.sort(key=lambda x: x.rank, reverse=False)
    final_print.append(print_list("Big lists (1000+ movies) by rank:", lists, "biglists", 300))

    lists.sort(key=lambda x: x.checked, reverse=True)
    final_print.append(print_list("Top lists by number of checked films:", lists, "rank", 10))

    lists.sort(key=lambda x: x.name.upper(), reverse=False)
    final_print.append(print_list("Completed lists:", lists, "completed", 300))

    # No need to sort the list again
    final_print.append(print_list("Unstarted lists:", lists, "unstarted", 300))


    if (write_results_to_file):   
        e = datetime.datetime.now()
        fn = f"{e.year}-{'0' + str(e.month) if (int(e.month) < 10) else e.month}-{e.day}-icm-stats-{username}.txt"  
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
    print("No results with given username.")

