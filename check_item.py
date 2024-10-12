import pandas

def check_item_in_csv(item_name: str, csv_file: str = 'Compost-Server/compost_data/compost_data.csv') -> bool:
    # Read the CSV file into a DataFrame
    data_frame = pandas.read_csv(csv_file, header=None)
    # Find the row where the first column matches the item name (case-insensitive)
    result = data_frame[data_frame[0].str.strip().str.lower() == item_name.strip().lower()]
    
    # Return True if 'Yes' is found in the second column, otherwise False
    if not result.empty:
        return result.iloc[0, 1].strip().lower() == 'yes'
    return False

# Example usage:
# result = check_item_in_csv('Avocado stones (pits)', 'your_file.csv')
#print(check_item_in_csv('apples','Compost-Server/compost_data/compost_data.csv'))