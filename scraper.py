import re, pprint, requests

# https://regex101.com/r/FASLcw/3  # Full Part
# https://regex101.com/r/FASLcw/4  # Extract Numbers
# https://regex101.com/r/FASLcw/5  # Experimental
# https://regex101.com/r/FASLcw/6  # Technically works
# https://regex101.com/r/FASLcw/7  # Same as above, but also selects the numbers
# https://regex101.com/r/FASLcw/9  # Same as above, but actually is able to get most of the entries
# https://regex101.com/r/CcUDpo/1/ # Find dates for quarterly


def extract_from_URL(url: str) -> list:

    # Need a User Agent to tell the server that this is a "real user"
    header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0' }

    # Uses requests for a simple get request
    full_html = requests.get(url, headers=header)

    html_part = ""
    save_enable = False

    # Iterate over every line in the html until the relevant part is extracted. Afterwards it breaks to save cycles.
    for line in full_html.text.splitlines():
        line = str(line)
        # This marks the start of the relevant part
        if "-financial-summary\" >Financial Summary</a>" in line:
            save_enable = True
        # This marks the end of the relevant part
        elif "We encourage you to use comments to engage with users," in line:
            break
        # This check if we are in the relevant part and saves all relevant lines into html_part
        if(save_enable):
            html_part += line + '\n'

    # Logs the resulting part to a file
    with open("tmp.html", "w+") as file:
        file.write(html_part)

    # Create a List with a Dictionary to store the results
    balance_sheet = [{}, {}, {}, {}]

    # Get dates for quarterly
    _quarterly_date_pattern = re.compile("<th><span class=\"bold\">(\d+)</span><div class=\"noBold arial_11\">([0-9/]+)")
    date_match = re.findall(_quarterly_date_pattern, html_part)
    print(date_match[1][0])

    # iterator is needed to get each date
    iterator = 0
    for quarter,  in balance_sheet:
        quarter["Date Tuple"] = date_match[iterator]
        quarter["Date"] = date_match[iterator][1] + '/' + date_match[iterator][0]
        iterator += 1


    # This uses regex to extract all the relevant information from the html using groups. I'm sure this could use some cleanup.
    _table_pattern = re.compile("(<tr class=.+(child grand|parent|child).+\n\s+.+\">([\(\)(.'',\-/&a-zA-Z ]+)<(.|[\n])+?(<td>([0-9-.]+)</td>)\n\s+(<td>([0-9-.]+)</td>)\n\s+(<td>([0-9-.]+)</td>)(\n\s+<td>)([0-9-.]+)(.|[\n])+?</tr>)")
    table = re.findall(_table_pattern, html_part)

    # Indencies 5, 7, 9 and 11 have the numbers. The corresponding regex groups are 6, 8, 10 and 12
    for entry in table:
        category_name = entry[2]
        regex_group = 5
        for quarter in balance_sheet:
            quarter[category_name] = entry[regex_group]
            regex_group += 2

    return balance_sheet


pprint.pprint(extract_from_URL("https://www.investing.com/equities/tesla-motors-balance-sheet"))
