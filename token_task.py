# import module
import os
import pandas as pd
import numpy as np

# funtion to convert file from .xls to .xlsx
def convert_to_xlsx(df):
  df['Instant debit amount'] = df['Instant debit amount'].astype(str)
  df['Instant debit amount'].fillna('', inplace=True)
  df['Instant debit amount'].replace('nan', '', inplace=True)
  columns_to_convert = ['Card_Number', 'Payment gateway response code']
  df[columns_to_convert] = df[columns_to_convert].astype(str)
  
  return df

# function to build dataframe with new column format
def initalize_tokenfile_format():
  tokenfile_format = {
      'External Pledge Reference Id' : [],
      'First_Name' : [],
      'Last_Name' : [],
      'Card_Number' : [],
      'Expiry Date' : [],
      'CardHolder Name' : [],
      'Donation Date' : [],
      'Donation Amount' : [],
      'Email' : [],
      'Mobile_Phone' : [],
      'Location' : [],
      'Office Name' : [],
      'Fundraiser full name' : [],
      'Team Leader' : [],
      'Campaign Manager' : [],
      'Supporter Payment method' : [],
      'Credit Card Type' : [],
      'Payment Type' : [],
      'Instant debit amount' : [],
      'Successful instant debit' : [],
      'Payment gateway message' : [],
      'Payment gateway response code' : [],
      'Reconciliation ID' : [],
      }
  return pd.DataFrame(tokenfile_format)

# function to copy data from old dataframe to new dataframe
def copy_data(new_df, df):
  new_df['External Pledge Reference Id'] = df['Pledge ID']
  new_df['First_Name'] = df['First Name']
  new_df['Last_Name'] = df['Last Name']
  new_df['Card_Number'] = df['PAN 16/15 digits'].astype(str)
  new_df['Expiry Date'] = df['Expiry Date MM/YY format']
  new_df['CardHolder Name'] = df['CardHolder Name']
  new_df['Donation Date'] = '12/01/2023'
  new_df['Donation Amount'] = 60
  new_df['Email'] = 'joharisuleiman87@gmail.com'
  new_df['Mobile_Phone'] = '017-3316286'
  new_df['Location'] = 'Mydin Subang Jaya'
  new_df['Office Name'] = 'KL Office 1'
  new_df['Fundraiser full name'] = 'Malliga A/P Munusamy'
  new_df['Team Leader'] = 'Malliga A/P Munusamy'
  new_df['Campaign Manager'] = 'Mohamad Syukran Bin Anuar'
  new_df['Supporter Payment method'] = 'Credit Card'
  new_df['Credit Card Type'] = 'VS'
  new_df['Payment Type'] = 'VS'
  new_df['Instant debit amount'] = ''
  new_df['Successful instant debit'] = 'No'
  new_df['Payment gateway message'] = 'Insufficient funds in the account'
  new_df['Payment gateway response code'] = '204'
  new_df['Reconciliation ID'] = ''

  return new_df

# function to reformat card type based on card number
def change_card_type(new_df):
   conditions = [
      new_df['Card_Number'].str.startswith('4'),
      new_df['Card_Number'].str.startswith('5'),
      new_df['Card_Number'].str.startswith('3')
      ]
   choices = ['VS', 'MC', 'AX']
   
   new_df['Credit Card Type'] = np.select(conditions, choices, default = '')
   new_df['Payment Type'] = new_df['Credit Card Type']
   
   return new_df

# main function
def main():
    # input folder path. Edit path accordingly
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\Tokenization\2024\Jan\3'

    files = os.listdir(folder_path)

    # using for loop to detect file based on file name and process accordingly
    for file_name in files:
        if 'vsmc' in file_name.lower():
            
            file_path = os.path.join(folder_path, file_name)

            df = pd.read_excel(file_path)

            df = convert_to_xlsx(df)

            # rename the file
            new_file_name = file_name.split('.')[0] + '.xlsx'
            new_file_path = os.path.join(folder_path,new_file_name)

            # save file
            df.to_excel(new_file_path, index=False)

            print(f'{new_file_name} has been successfully created!')

        elif 'new card' in file_name.lower():
            
            file_path = os.path.join(folder_path, file_name)

            df = pd.read_excel(file_path, dtype={'PAN 16/15 digits': str})
            
            new_df = initalize_tokenfile_format()
            new_df = copy_data(new_df, df)
            new_df = change_card_type(new_df)

            new_file_name = file_name.split('.')[0] + ' - To Token.xlsx'
            new_file_path = os.path.join(folder_path,new_file_name)

            new_df.to_excel(new_file_path, index=False)

            print(f'{new_file_name} has been successfully created!')

        else:
            print('No File Available')

if __name__ == "__main__":
   main()