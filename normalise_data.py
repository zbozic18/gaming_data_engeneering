import csv
import pandas as pd


# The bellow function is used in the game_reviews.csv data set in order to lose the months and only get years
def find_year(date):
    indexes = len(date) - 1
    found_year = date[indexes - 3] + date[indexes - 2] + date[indexes - 1] + date[indexes]
    return found_year


# Fixes the vg_sales file by filtering out the entries which fall into one of the following categories:
# year = 'N/A', critic_count = 'tbd', platform = '2600' or '3600', len(name) = 4
# The function appends all of the filtered rows on a new list and saves it on a a new csv document: 'vg_sales_fixed.csv
def fix_vg_sales():
    new_rows = []
    names = ['Name', 'Platform', 'Year_of_Release', 'Genre', 'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales',
             'Other_Sales', 'Global_Sales', 'Critic_Score', 'Critic_Count', 'User_Score', 'User_Count', 'Developer',
             'Rating'
             ]
    with open('gaming_data/vg_sales.csv', 'r') as file:
        data = csv.reader(file)
        starter = True
        for row in data:
            if not starter:
                year = row[2]
                if year != 'N/A':
                    if row[12] != 'tbd':
                        if row[1] != 2600:
                            if row[1] != 3600:
                                if len(row[0]) != 4:
                                    new_rows.append(row)
            starter = False

    with open('vg_sales_fixed.csv', 'w') as file:
        csvw = csv.writer(file)
        csvw.writerow(names)
        csvw.writerows(new_rows)


# This function fills all the empty value in the csv with 0.0 in order to enable mysql operations
# It does so by checking every value in every row of the Console_Sales.csv for missing values, substituting them w/ 0.0
# It appends all the new rows onto a new list and writes them onto a new csv file: 'console_sales_fixed.csv'
# Finally it calls the function reverse_console_sales() which saves the amended data onto a new csv file
def fix_empty_values():
    fixed_data = []
    with open('gaming_data/Console_Sales.csv', 'r') as file:
        data = csv.reader(file)
        first = True
        for row in data:
            if not first:
                fixed_row = []
                for i in row:
                    if i == '':
                        fixed_row.append(0.0)
                    else:
                        fixed_row.append(i)
                fixed_data.append(fixed_row)
            elif first:
                print(row)
                first_row = row
                first = False

    with open('console_sales_fixed.csv', 'w') as file:
        csvw = csv.writer(file)
        csvw.writerow(first_row)
        csvw.writerows(fixed_data)

    reverse_console_sales()


# This function uses the pandas data frame in order to rotate the columns and the rows of the csv file.
# This makes the columns of the data set switch from consoles to years for easier mysql querrying.
def reverse_console_sales():
    sales = pd.read_csv('console_sales_fixed.csv')
    print(sales)
    sales = sales.T
    print(sales)
    sales.to_csv('console_s.csv')
