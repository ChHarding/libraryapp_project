import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import requests


def add_book_gui():
    def submit_book():
        title = title_entry.get()
        author = author_entry.get()
        book_type = type_var.get()
        note = note_entry.get("1.0", "end-1c")

        if title and author:
            df = pd.read_csv('myShelf.csv')
            data = {
                'title': [title],
                'author': [author],
                'type': [book_type],
                'note': [note]
            }
            new_df = pd.DataFrame(data)
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_csv('myShelf.csv', index=False)
            messagebox.showinfo("Book added to your library!")
            add_book_window.destroy()
        else:
            messagebox.showerror("Please fill in all fields")

    add_book_window = tk.Toplevel(root)
    add_book_window.title("Add Book")

    title_label = tk.Label(add_book_window, text="Title:", font="Helvetica 10 bold")
    title_label.grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(add_book_window)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    author_label = tk.Label(add_book_window, text="Author:", font="Helvetica 10 bold")
    author_label.grid(row=1, column=0, padx=5, pady=5)
    author_entry = tk.Entry(add_book_window)
    author_entry.grid(row=1, column=1, padx=5, pady=5)

    type_label = tk.Label(add_book_window, text="Type:", font="Helvetica 10 bold")
    type_label.grid(row=2, column=0, padx=5, pady=5)
    type_var = tk.StringVar(add_book_window)
    type_var.set("paper")  # Default value
    type_options = ["paper", "digital", "audio"]
    type_dropdown = ttk.Combobox(add_book_window, textvariable=type_var, values=type_options)
    type_dropdown.grid(row=2, column=1, padx=5, pady=5)

    note_label = tk.Label(add_book_window, text="Note:", font="Helvetica 10 bold")
    note_label.grid(row=3, column=0, padx=5, pady=5)
    note_entry = tk.Text(add_book_window, height=5, width=30)
    note_entry.grid(row=3, column=1, padx=5, pady=5)

    submit_button = tk.Button(add_book_window, text="Submit", command=submit_book)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

def view_library_gui():
    view_window = tk.Toplevel(root)
    view_window.title("Library")

    df = pd.read_csv('myShelf.csv')
    tree = ttk.Treeview(view_window, columns=("Title", "Author", "Type", "Note"), show="headings")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Type", text="Type")
    tree.heading("Note", text="Note")

    for index, row in df.iterrows():
        tree.insert("", "end", values=(row['title'], row['author'], row['type'], row['note']))

    tree.pack()

def search_for_book_gui():
    def search_book():
        title_search = search_entry.get()
        if title_search:
            openlibrary = "https://openlibrary.org/search.json?title=" + title_search
            response = requests.get(openlibrary)
            info = response.json()
            if info['docs']:
                author = info['docs'][0]['author_name'][0] if 'author_name' in info['docs'][0] else "N/A"
                publish_year = info['docs'][0]['first_publish_year'] if 'first_publish_year' in info['docs'][0] else "N/A"
                
                search_result_window = tk.Toplevel(root)
                search_result_window.title("Search Results")
                
                result_label = tk.Label(search_result_window, text=f"Title: {title_search}\nAuthor: {author}\nPublished: {publish_year}")
                result_label.pack(pady=10)
                
                def add_to_library():
                    def submit_book_details():
                        book_type = type_var.get()
                        note = note_entry.get("1.0", "end-1c")
                        
                        df = pd.read_csv('myShelf.csv')
                        data = {
                            'title': [title_search],
                            'author': [author],
                            'type': [book_type],
                            'note': [note]
                        }
                        new_df = pd.DataFrame(data)
                        df = pd.concat([df, new_df], ignore_index=True)
                        df.to_csv('myShelf.csv', index=False)
                        messagebox.showinfo("Success", "Book added to your library!")
                        add_book_details_window.destroy()
                        search_result_window.destroy()

                    add_book_details_window = tk.Toplevel(search_result_window)
                    add_book_details_window.title("Add Book Details")
                    
                    type_label = tk.Label(add_book_details_window, text="Type:")
                    type_label.grid(row=0, column=0, padx=5, pady=5)
                    type_var = tk.StringVar(add_book_details_window)
                    type_var.set("paper")  # Default value
                    type_options = ["paper", "digital", "audio"]
                    type_dropdown = ttk.Combobox(add_book_details_window, textvariable=type_var, values=type_options)
                    type_dropdown.grid(row=0, column=1, padx=5, pady=5)
                    
                    note_label = tk.Label(add_book_details_window, text="Note:")
                    note_label.grid(row=1, column=0, padx=5, pady=5)
                    note_entry = tk.Text(add_book_details_window, height=5, width=30)
                    note_entry.grid(row=1, column=1, padx=5, pady=5)
                    
                    submit_button = tk.Button(add_book_details_window, text="Submit", command=submit_book_details)
                    submit_button.grid(row=2, column=0, columnspan=2, pady=10)
                
                add_button = tk.Button(search_result_window, text="Add to Library", command=add_to_library)
                add_button.pack(pady=5)
            else:
                messagebox.showinfo("Not Found", "Book not found in Open Library")
        else:
            messagebox.showerror("Error", "Please enter a book title")

    search_window = tk.Toplevel(root)
    search_window.title("Search Book")

    search_label = tk.Label(search_window, text="Enter Book Title:")
    search_label.grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(search_window)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    search_button = tk.Button(search_window, text="Search", command=search_book)
    search_button.grid(row=1, column=0, columnspan=2, pady=10)

# Create the main window
root = tk.Tk()
root.title("My Book Shelf")

# Create menu buttons
add_button = tk.Button(root, text="Add Book", command=add_book_gui)
add_button.pack(pady=5)
view_button = tk.Button(root, text="View Library", command=view_library_gui)
view_button.pack(pady=5)
search_button = tk.Button(root, text="Search Book", command=search_for_book_gui)
search_button.pack(pady=5)

root.mainloop()

