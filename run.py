import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get data from useer 
    """

    while True:
        print("please enter sales date from the last market")
        print("data should be six number, separated by commas")
        print("example: 10,20,30,40,50,60\n")

        data_str = input("enter your date here")

        sales_data = data_str.split(",")
    

        if validate_data(sales_data):
            print("Data is valid!")
            break
            
    return sales_data 
   
def validate_data(values):
    """
    inside the try, comverts all string values into intagers. 
    raises valueError if string cannot be converted into int,
    or if there anen't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"exactly 6 values required, you provided {len(values)}"
        )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
        return False

    return True

"""
refactered 
def update_sales_worksheet(data):
  
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated sussessfully.\n")

def update_surplus_worksheet(data):
    
    print("updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("surplus worksheet updated sussessfully.\n")
"""
def update_worksheet(data, worksheet):
    """
    update data add new row
    """
    print("updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated sussessfully.\n")


def calculate_surplus_data(sales_row):
    """
    surpluse sums
    """
    print("calculating suplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - int(sales)
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """
    collect collom data not row data
    """
    sales = SHEET.worksheet("sales")
    #column = sales.col_values(3)
    #print(column)

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    calculating avg stock 
    """
    print("calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

    print(new_stock_data)
def main():
    """
    run all programs 
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    


print("love sandwichs data auto")
main()

