import datetime
import xlrd

def _convert_row(row):
    return [cell.value for cell in row]

def _convert_date(data, sheet):
    time_tuple = xlrd.xldate_as_tuple(data, sheet.book.datemode)
    date = datetime.datetime(*time_tuple)
    return datetime.date(date.year, date.month, date.day)

def _convert_datetime(data, sheet):
    time_tuple = xlrd.xldate_as_tuple(data, sheet.book.datemode)
    return datetime.datetime(*time_tuple)

def my_xls_reader(filename):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)
    header = _convert_row(sheet.row(0))
    for row_number in range(1, sheet.nrows):
        data = _convert_row(sheet.row(row_number))
        row = dict(zip(header, data))
        row['vencimento'] = _convert_date(row['vencimento'], sheet)
        row['timestamp'] = _convert_datetime(row['timestamp'], sheet)
        yield row

filename = 'examples/data/tesouro-direto.xls'
for row in my_xls_reader(filename):
    print(row)
