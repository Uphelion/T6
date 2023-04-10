seasons = ['02/03', '03/04', '04/05', '05/06', '06/07', '07/08', '08/09', '09/10', '10/11', '11/12', '12/13', '13/14', '14/15', '15/16', '16/17', '17/18', '18/19', '19/20', '20/21', '21/22', '22/23']

import csv

file_path = "/Users/nasif/Documents/Python/T6/big_table.csv"

with open(file_path, newline='') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=',')
    big_array = [row for row in data_reader]

def convert_to_3d_list(data):
    header = ['Team', 'Points', 'Wins', 'Draws', 'Losses', 'GF', 'GA', 'GD']
    tables = []
    current_table = []

    for row in data:
        if row == header:
            if current_table:
                tables.append(current_table)
            current_table = [row]
        else:
            current_table.append(row)

    if current_table:
        tables.append(current_table)

    return tables

table_3d = convert_to_3d_list(big_array)

def search():
    season = input("Season?: ")
    if season in seasons:
        season_index = seasons.index(season)
        return table_3d[season_index]
    else:
        print("Season not found in the list")
        return search()

result = search()
print(result)
