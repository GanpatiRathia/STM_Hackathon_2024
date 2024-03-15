import re

def extract_date(log):
    match = re.search(r'(\d{2}_\d{2}_\d{2})', log)
    #print(match)
    if match:
        date = match.group()
        formatted_date = date.replace('_', '-')
        return formatted_date
    else:
        return None