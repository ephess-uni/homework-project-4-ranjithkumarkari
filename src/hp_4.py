from datetime import datetime
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


def detect_date_format(date_str):
    """Detects the date format of a given date string."""
    formats_to_try = ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d']
    for date_format in formats_to_try:
        try:
            datetime.strptime(date_str, date_format)
            return date_format
        except ValueError:
            continue
    raise ValueError("Unable to detect date format for date string: {}".format(date_str))


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees = defaultdict(float)
    with open(infile, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            due_date = datetime.strptime(row['date_due'], '%m/%d/%Y')
            return_date_format = detect_date_format(row['date_returned'])
            return_date = datetime.strptime(row['date_returned'], return_date_format)
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
