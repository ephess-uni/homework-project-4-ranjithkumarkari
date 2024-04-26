from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    reformatted_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        reformatted_date = date_obj.strftime('%d %b %Y')
        reformatted_dates.append(reformatted_date)
    return reformatted_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("Start date should be a string.")
    if not isinstance(n, int):
        raise TypeError("Number of days should be an integer.")
    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees = defaultdict(float)
    with open(infile, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            due_date = datetime.strptime(row['date_due'], '%m/%d/%Y')
            return_date = datetime.strptime(row['date_returned'], '%m/%d/%y')
            if return_date > due_date:
                days_late = (return_date - due_date).days
                late_fee = days_late * 0.25
                patron_id = row['patron_id']
                late_fees[patron_id] += late_fee

    with open(outfile, 'w', newline='') as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': '{:.2f}'.format(fee)})
