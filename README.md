# libraryapp_project

#####USER GUIDE#######

# Summary
LibraryApp is an app designed for book enthusiasts to search for books, add them to a personal digital library, sort them by type, and add notes. Users can search for books by title and organize their library by type (paper, digital, or audio). The notes feature allows users to add personal annotations. Using the OpenLibrary API users have access to thousands of books to navigate through.

# Requirements
- Python 3.10 or higher

# Recommendations
- Some sort of software to open database files (.db)
  - This is so you can add field, delete content, etc.
  - I use db browser for sqlite (https://sqlitebrowser.org/)

# Functionality

<img width="1366" alt="Screenshot 2024-07-31 at 9 28 48 PM" src="https://github.com/user-attachments/assets/35813c7c-2bc8-41b6-8f35-819873fe932d">

1. Add a Book    
- This button opens the window for you to add a book. You can either type in the booko details manually or "Search the Web" for the book.
- <img width="650"         alt="Screenshot 2024-07-31 at 9 29 04 PM" src="https://github.com/user-attachments/assets/62edfbf1-1298-4e5d-916f-205c297984b2">
- If you choose to search the web:
-   type in the title, select the book you like from the options provided and then add selection.
-   <img width="617" alt="Screenshot 2024-07-31 at 9 37 50 PM" src="https://github.com/user-attachments/assets/90617323-6470-4076-bc19-6a0ddf13b6c8">

3. Search Bar
- This search allows you to look through your personal library on the left hand side of the screen.
   
4. Sort
- This allows you to sort your personal library by "Book Type"
   
6. Your Personal Library
- These are all your books that are in the library database.
   
7. Library Stats
- <img width="1354" alt="Screenshot 2024-07-31 at 9 36 31 PM" src="https://github.com/user-attachments/assets/79749ea7-754d-474e-9cce-2842d2d1a5d7">
- If you select the details tab you will open the statistics.
- This shows details about your personal library.
- <img width="1349" alt="Screenshot 2024-07-31 at 9 36 43 PM" src="https://github.com/user-attachments/assets/d915a1fe-ba6c-42c2-9233-1c47724dfb9e">

# Bugs
- The edit selection is not currently functioning as intended.
- There is currently no way to delete a book without editing the database file.
- When you add a book you have to switch between tabs to update your library and see the most recently added book(s).
