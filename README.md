# icm-stats
A simple unofficial iCheckMovies statistics tool. 

## Usage
Run the script with Python3 and provide optional username as a command-line argument or edit the eligible username in code. The scripts writes a textfile (year-month-day-icm-stats-username.txt) by default but changing the variable _write_results_to_file_ to False lets the program just print the statistics out.

## Statistics
* Top unfinished lists by completion percentage
* Top lists by rank
* Bottom lists by rank
* Lists under rank #1000
* Lists between ranks #1000 and #2000
* Big lists (1000+ movies) by rank
* Top lists by number of checked films
* Completed lists
* Unstarted lists
* All lists (in HTML output mode)

## Requirements
* Requests
* BeautifulSoup
