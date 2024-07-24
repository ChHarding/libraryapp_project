import tkinter as tk
from tkinter import ttk
import pandas as pd
import requests


class LibApp(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("My Book Shelf")
    self.geometry("400x300")

    # Create notebook
    self.notebook = ttk.Notebook(self)
    self.notebook.pack(pady=10)

    # Create tabs
    self.add_tab = tk.Frame(self.notebook)
    self.view_tab = tk.Frame(self.notebook)
    self.search_tab = tk.Frame(self.notebook)

    self.add_tab.pack(fill="both", expand=True)
    self.view_tab.pack(fill="both", expand=True)
    self.search_tab.pack(fill="both", expand=True)

    # Add tabs to notebook
    self.notebook.add(self.view_tab, text="View Library")
    self.notebook.add(self.add_tab, text="Add/Edit Book")
    self.notebook.add(self.search_tab, text="Search Book")

    try: # CH: better: make new df if file does not exist
        self.df = pd.read_csv('myShelf.csv')  
    except:
        # create a new dataframe with the correct columns
        self.df = pd.DataFrame(columns=['title','author','type','note'])

    #CH check that we have the right columns
    for col in ['title', 'author', 'type', 'note']:
        if col not in self.df.columns:
            messagebox.showerror("Error", "The CSV file must have columns: title, author, type, note")
            self.destroy()
    #self.result = None  # will store search result

    self.create_view_library_gui()
    self.create_add_book_gui()
    self.create_search_gui()

    self.notebook.select(self.view_tab)  # needed to switch to the add tab

    self.mainloop()

  def create_add_book_gui(self, event=None):
    #add_book_window = tk.Toplevel(self)
    #add_book_window.title("Add Book")
    parent = self.add_tab

    self.title_label = tk.Label(parent,
                                text="Title:",
                                font="Helvetica 10 bold")
    self.title_label.grid(row=0, column=0, padx=5, pady=5)
    self.title_entry = tk.Entry(parent)
    self.title_entry.grid(row=0, column=1, padx=5, pady=5)
    self.author_label = tk.Label(parent,
                                 text="Author:",
                                 font="Helvetica 10 bold")
    self.author_label.grid(row=1, column=0, padx=5, pady=5)
    self.author_entry = tk.Entry(parent)
    self.author_entry.grid(row=1, column=1, padx=5, pady=5)

    self.type_label = tk.Label(parent, text="Type:", font="Helvetica 10 bold")
    self.type_label.grid(row=2, column=0, padx=5, pady=5)
    self.type_var = tk.StringVar(parent)
    self.type_var.set("paper")  # Default value
    self.type_options = ["paper", "digital", "audio"]
    self.type_dropdown = ttk.Combobox(parent,
                                      textvariable=self.type_var,
                                      values=self.type_options)
    self.type_dropdown.grid(row=2, column=1, padx=5, pady=5)

    self.note_label = tk.Label(parent, text="Note:", font="Helvetica 10 bold")
    self.note_label.grid(row=3, column=0, padx=5, pady=5)
    self.note_entry = tk.Text(parent, height=5, width=30)
    self.note_entry.grid(row=3, column=1, padx=5, pady=5)

    self.submit_button = tk.Button(parent,
                                   text="Submit",
                                   command=self.submit_book)
    self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

  def create_view_library_gui(self, event=None):
    #view_window = tk.Toplevel(root)
    #view_window.title("Library")
    parent = self.view_tab

    self.tree = ttk.Treeview(parent,
                             columns=("Title", "Author", "Type", "Note"),
                             show="headings")
    self.tree.heading("Title", text="Title")
    self.tree.heading("Author", text="Author")
    self.tree.heading("Type", text="Type")
    self.tree.heading("Note", text="Note")

    for index, row in self.df.iterrows():
      self.tree.insert("",
                       "end",
                       values=(row['title'], row['author'], row['type'],
                               row['note']))

    # CH shrink the columns to fit the data, by finding the max width of each column
    for col in "title", "author", "type", "note":
        # create a list of the lengths of the strings in the column and get the largest with max()
        width = max([len(str(x)) for x in self.df[col]]) 
        self.tree.column(col.title(), width=width*5) # col.title() make sure the first 
    self.tree.pack()

    # Add functionality to edit entries in the treeview
    self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
    self.edit_button = tk.Button(parent,
                                 text="Edit",
                                 command=self.edit_selected_book)
    self.edit_button.pack(side="right")
    self.delete_button = tk.Button(parent,
                                   text="Delete",
                                   command=self.delete_selected_book)
    self.delete_button.pack(side="right")

    self.selected_item = None

  def create_search_gui(self, event=None):
    #search_window = tk.Toplevel(self)
    #search_window.title("Search Book")

    parent = self.search_tab
    self.search_label = tk.Label(parent, text="Enter Book Title:")
    self.search_label.grid(row=0, column=0, padx=5, pady=5)

    self.search_entry = tk.Entry(parent)
    self.search_entry.grid(row=0, column=1, padx=5, pady=5)

    self.search_button = tk.Button(parent,
                                   text="Search",
                                   command=self.search_book)
    self.search_button.grid(row=0, column=2, padx=5, pady=5)

    self.search_result = tk.StringVar()
    #self.search_result_entry = tk.Entry(parent, width=40,
    #state="disabled", textvariable=self.search_result,
    #font="Helvetica 10 bold")
    #self.search_result_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    self.add_to_library_button = tk.Button(
        parent,
        text="Add to Library",
        command=self.put_result_in_add_book_form)
    self.add_to_library_button.grid(row=2, column=2, padx=5, pady=5)

    # Create a listbox to display search results
    self.results_listbox = tk.Listbox(parent, height=10, width=65)
    self.results_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

  def on_tree_select(self, event):
    self.selected_item = self.tree.selection()[0]

    self.delete_button = tk.Button(parent,
                                   text="Delete",
                                   command=self.delete_selected_book)
    self.delete_button.pack(side="right")
    self.edit_button = tk.Button(parent,
                                 text="Edit",
                                 command=self.edit_selected_book)
    self.edit_button.pack(side="right")



  def edit_selected_book(self):
    if self.selected_item:
      # Get the values of the selected row
      values = self.tree.item(self.selected_item, "values")
      # Populate the entry fields in the add_book_gui with the values
      self.title_entry.delete(0, tk.END)
      self.title_entry.insert(0, values[0])
      self.author_entry.delete(0, tk.END)
      self.author_entry.insert(0, values[1])
      self.type_var.set(values[2])
      self.note_entry.delete("1.0", tk.END)
      self.note_entry.insert(tk.END, values[3])
      # Switch to the add_book_gui tab
      self.notebook.select(self.add_tab)
      # Update the submit button to edit the selected book
      self.submit_button.config(command=self.update_selected_book)

  def update_selected_book(self):
    # Get the updated values from the entry fields
    title = self.title_entry.get()
    author = self.author_entry.get()
    book_type = self.type_var.get()
    note = self.note_entry.get("1.0", "end-1c")
    # Update the dataframe
    row_index = int(self.selected_item[1:])
    self.df.loc[row_index - 1] = [title, author, book_type, note]
    # Update the treeview
    self.tree.item(self.selected_item, values=(title, author, book_type, note))
    # Save the dataframe to the CSV file
    self.df.to_csv('myShelf.csv', index=False)
    # Switch back to the view_library_gui tab
    self.notebook.select(self.view_tab)
    # Reset the submit button to add a new book
    self.submit_button.config(command=self.submit_book)

      

  def delete_selected_book(self):
    if self.selected_item:

      # Delete from treeview
      self.tree.delete(self.selected_item)
      # Delete from dataframe
      row_index = int(self.selected_item[0:])  # Extract row index from treeview id
      self.df = self.df.drop(index=row_index-1)  # CH treeview starts at 1, df at 0
      self.df.to_csv('myShelf.csv', index=False)
      # Clear the selected item
      self.selected_item = None


  def search_book(self, event=None):
    title_search = self.search_entry.get()
    if title_search:
      openlibrary = "https://openlibrary.org/search.json?title=" + title_search
      response = requests.get(openlibrary)
      info = response.json()
      if info['docs']:
        self.results_listbox.delete(0, tk.END)  # Clear previous results
        for i in range(min(5, len(info['docs']))):  # Show up to 5 results

          # CH if you use a long expression multiple times, it's better to store it in a variable
          curr = info['docs'][i]
          author = curr.get('author_name', ["N/A"])[0] # CH: if author_name is not present, return ["N/A"] and take the first element
          publish_year = curr.get('first_publish_year', "N/A") # CH: if first_publish_year is not present, return "N/A"

          self.results_listbox.insert(tk.END,
              f"{info['docs'][i]['title']} by {author} ({publish_year})")


      else:
        self.results_listbox.delete(0, tk.END)  # Clear previous results
        self.results_listbox.insert(tk.END, f"Nothing found for {title_search}")

  def submit_book(self):
    title = self.title_entry.get()
    author = self.author_entry.get()
    book_type = self.type_var.get()
    note = self.note_entry.get("1.0", "end-1c")

    if title and author:
      data = {
          'title': [title],
          'author': [author],
          'type': [book_type],
          'note': [note]
      }
      new_df = pd.DataFrame(data)
      self.df = pd.concat([self.df, new_df], ignore_index=True)
      self.df.to_csv('myShelf.csv', index=False)
      #messagebox.showinfo("Success", "Book added to your library!")

      # Insert the new book into the treeview
      self.tree.insert("", "end", values=(title, author, book_type, note))

      # Clear the form
      self.title_entry.delete(0, tk.END)
      self.author_entry.delete(0, tk.END)
      self.type_var.set("paper")
      self.note_entry.delete("1.0", tk.END)
      #self.result = None

  def put_result_in_add_book_form(self):
    if self.results_listbox:  # Check if self.result is not None
      selected_index = self.results_listbox.curselection()
      if selected_index:
        selected_item = self.results_listbox.get(selected_index[0])
        # Assuming the listbox items are in the format "Title by Author (Year)"
        title, author = selected_item.split(" by ", 1)
        author = author.split(" (")[0]  # Remove the year

        self.title_entry.delete(0,
                                tk.END)  # Clear any existing text in the entry
        self.title_entry.insert(0, title)
        self.author_entry.delete(0, tk.END)
        self.author_entry.insert(0, author)
    self.notebook.select(self.add_tab)




if __name__ == "__main__":
  LibApp()
