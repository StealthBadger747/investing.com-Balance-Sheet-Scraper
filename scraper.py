import re, pprint

# https://regex101.com/r/FASLcw/3  # Full Part
# https://regex101.com/r/FASLcw/4  # Extract Numbers
# https://regex101.com/r/FASLcw/5  # Experimental
# https://regex101.com/r/FASLcw/6  # Technically works
# https://regex101.com/r/FASLcw/7  # Same as above, but also selects the numbers
# https://regex101.com/r/FASLcw/9  # Same as above, but actually is able to get most of the entries
# https://regex101.com/r/CcUDpo/1/ # Find dates for quarterly


# Open the file
html_part = ""
with open("tesla-motors-balance-sheet.html", "r") as file:
    save_enable = False
    for line in file:
        if "-financial-summary\" >Financial Summary</a>" in line:
            print("FUCK YEAH")
            save_enable = True
        elif "We encourage you to use comments to engage with users, share your perspective and ask questions of authors and each other. However, in order to maintain the high level of discourse we" in line:
            save_enable = False
        if(save_enable):
            html_part += line

# Create a List with a Dictionary to store the results
balance_sheet = [{}, {}, {}, {}]

# Get dates for quarterly
_quarterly_date_pattern = re.compile("<th><span class=\"bold\">(\d+)</span><div class=\"noBold arial_11\">([0-9/]+)")
date_match = re.findall(_quarterly_date_pattern, html_part)
print(date_match[1][0])

iterator = 0
for quarter in balance_sheet:
    quarter["Date Tuple"] = date_match[iterator]
    quarter["Date"] = date_match[iterator][1] + '/' + date_match[iterator][0]


_table_pattern = re.compile("(<tr class=.+(child grand|parent|child).+\n\s+.+\">([\(\)(.'',\-/&a-zA-Z ]+)<(.|[\n])+?(<td>([0-9-.]+)</td>)\n\s+(<td>([0-9-.]+)</td>)\n\s+(<td>([0-9-.]+)</td>)(\n\s+<td>)([0-9-.]+)(.|[\n])+?</tr>)")
table = re.findall(_table_pattern, html_part)

for entry in table:
    print("-----------------------------------")

    print("Category: ", entry[2])
    category_name = entry[2]

    regex_group = 5
    for quarter in balance_sheet:
        quarter[category_name] = entry[5]
        regex_group += 2

    print("Group 6:  ", entry[5])
    print("Group 8:  ", entry[7])
    print("Group 10: ", entry[9])
    print("Group 12: ", entry[11])

pprint.pprint(balance_sheet)
