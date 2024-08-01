#Overview
Connected to the OpenLibrary API
Created the function to look up and store books to your personal library
Made the ability to view the whole library

#Database

The .db file will automatically generate if there is not one already in the repo. If this happen you must open the .db file and create the fields used.

#Recommendations -Some sort of software to open database files (.db) -This is so you can add field, delete content, etc. -I use db browser for sqlite (https://sqlitebrowser.org/)

<img width="1038" alt="Screenshot 2024-08-01 at 12 05 11 AM" src="https://github.com/user-attachments/assets/cea3d7e7-8a9b-4e8f-89b3-97a029f26015">

1. Create a Table called Books
2. You will create the following fields:
   - book_id (integars)
   - book_name (text)
   - book_author (text)
   - book_type (text)
   - book_notes (text)
3. Save your changes.


#Flow

<img width="1349" alt="Screenshot 2024-07-31 at 9 36 09 PM" src="https://github.com/user-attachments/assets/d8c87cc1-18c5-4a99-9b5b-e0056b0abbd2">

1. There is one main screen that allows the user to open multiple windows.
2. The main screen include:
   - Add Book (button that opens new window)
   - Edit Selection (button currently does not work)
   - Users Library
   - Detail panel about selected book
   - A search section for the user library
   - A sort section for user library
   - A details tab for overall stats about the user's library
3. The Add Book screen includes:
   - Search Web (button that opens window for search)
   - entry fields for metadata
   - Add Book
4. Search the Web screen includes:
   - Title search
   - Search box that populates 5 results
   - Add Selection button (this populates the Add Book Screen
5. Dialogue boxes populate if there are errors/to confirm a process

#Known Issues
- The edit selection is not currently functioning as intended.
- There is currently no way to delete a book without editing the database file.
- When you add a book you have to switch between tabs to update your library and see the most recently added book(s).
