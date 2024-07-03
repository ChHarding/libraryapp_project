import pandas as pd
import requests
import sys

def add_book():
  title_input = input("Enter title of book: ")
  author_input = input("Enter author of book: ")
  type_input = input("Enter type of book (paper, digital, or audio): ")
  # data of Player and their performance CH: please lne up you comment with the next line
  data = {
        'title': [title_input],
        'author': [author_input],
        'type': [type_input]
    }
  
  # Make data frame of above data
  df = pd.DataFrame(data)
  
  # append data frame to CSV file
  df.to_csv('myShelf.csv', mode='a', index=False, header=False)
  
  # print message
  print("Book added to your collection.")
  print("\033[1;31;40m Do you want to go back to the menu?\033[0m") # color is a nice touch :)
  exit_option = input("Enter 'yes' or 'no': ")
  if exit_option == "yes":
    menu_input()
  else:
    print("Goodbye!") # that will just return to whoever called that function
    # if you're really done you could use sys.exit("Goodbye!") instead.
    # or as not using return will return a None, you could catch that at the caller 
    # and terminate the app there.
    # And you could have a exit option in your main menu
  
def view_library():
  df = pd.read_csv('myShelf.csv')
  #print(df)
  print(df.to_string(index=False)) # no index
  print("\033[1;31;40m Do you want to go back to the menu?\033[0m")
  exit_option = input("Enter 'yes' or 'no': ")
  if exit_option == "yes":
    menu_input()
  else:
    print("Goodbye!")

  
def menu_input():
    print("\033[1;35;40m Menu Options \033[0m")
    print("1. Add book")
    print("2. View library")
    print("3. Search for a book")
    print("4. Exit")
    while True:
        menu_input = input("Please enter a number corresponding to your menu option:")
        print("You selected option:", menu_input)
        if menu_input == "1":
          if add_book() == None:
            return
          break
        elif menu_input == "2":
            if view_library() == None:
              return
            break 
        elif menu_input == "3":
          if search_for_book() == None:
            return
          break
        else:
          return

def search_for_book():
  title_search = input("Enter the title of the book you want to search for: ")
  openlibrary = "https://openlibrary.org/search.json?title=" + title_search
  response = requests.get(openlibrary)
  response.raise_for_status()
  info = response.json() 
  
  if len(info['docs']) > 0:  # protect against nothing found
    print(len(info['docs']), "book found, using first")
    print(info['docs'][0]['author_name'][0], info['docs'][0]['first_publish_year'])
    if 'id_goodreads' in info['docs'][0]: # do we have goodreads?
        print(f"https://www.goodreads.com/book/show/{info['docs'][0]['id_goodreads'][0]}")

    print("\033[1;31;40m Do you want to add this book to your library?\033[0m")
    search_input = input("Enter 'yes' or 'no': ")
    if search_input == "yes":
      type_input = input("Enter type of book (paper, digital, or audio): ")
      data = {
        'title': [title_search],
        'author': [info['docs'][0]['author_name'][0]],
        'type': [type_input]
      }

      # Make data frame of above data
      df = pd.DataFrame(data)

      # append data frame to CSV file
      df.to_csv('myShelf.csv', mode='a', index=False, header=False)
      print ("would you like to search for another book?")
      search_input2 = input("Enter 'yes' or 'no': ")
      if search_input2 == "yes":
        search_for_book()
      else:
        menu_input()

    elif search_input == "no":
      print("\033[1;31;40m Do you want to go back to the menu?\033[0m")
    exit_option = input("Enter 'yes' or 'no': ")
    if exit_option == "yes":
        menu_input()
    else:
        print("Goodbye!")
  else:
    print("Nothing found")
    menu_input()    

menu_input()
