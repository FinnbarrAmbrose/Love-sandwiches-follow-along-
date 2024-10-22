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


def update_sales_worksheet(data):
    """
    update data add new row
    """
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated sussessfully.\n")

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


def main():
    """
    run all programs 
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

print("love sandwichs data auto")
main()
