from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict
import os

def reformat_dates(old_dates):
    """Reformat date strings in 'yyyy-mm-dd' format to 'dd mmm yyyy'."""
    return [datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y') for date in old_dates]

def date_range(start, n):
    """Return a list of n datetime objects starting from start."""
    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]

def add_date_range(values, start_date):
    """Add a daily date range to the list of values starting from start_date."""
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    return [(start_datetime + timedelta(days=i), value) for i, value in enumerate(values)]

def fees_report(infile, outfile):
    """Calculate late fees per patron id and write a summary report to outfile."""
    late_fees = defaultdict(float)
    with open(infile, mode='r') as file:
        reader = DictReader(file)
        for row in reader:
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fees[row['patron_id']] += days_late * 0.25

    # Include all patrons in the output, even if they have no late fees
    all_patrons = set()
    with open(infile, mode='r') as file:
        reader = DictReader(file)
        for row in reader:
            all_patrons.add(row['patron_id'])

    with open(outfile, mode='w', newline='') as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id in all_patrons:
            writer.writerow({'patron_id': patron_id, 'late_fees': '{:.2f}'.format(late_fees.get(patron_id, 0.00))})


if __name__ == '__main__':
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # Specify the input file path
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')
    # Specify the output file name
    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
