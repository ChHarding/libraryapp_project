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
    self.notebook.add(self.add_tab, text="Add Book")
    self.notebook.add(self.search_tab, text="Search Book")

    self.df = pd.read_csv('myShelf.csv')  # should exit if not found
    self.result = None  # will store search result

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

  def on_tree_select(self, event):
    self.selected_item = self.tree.selection()[0]

  def edit_selected_book(self):

    if self.selected_item:
      values = self.tree.item(self.selected_item, "values")
      # Create a new window for editing
      edit_window = tk.Toplevel(self)
      edit_window.title("Edit Book")

      title_label = tk.Label(edit_window, text="Title:")
      title_label.grid(row=0, column=0, padx=5, pady=5)
      title_entry = tk.Entry(edit_window)
      title_entry.insert(0, values[0])
      title_entry.grid(row=0, column=1, padx=5, pady=5)

      author_label = tk.Label(edit_window, text="Author:")
      author_label.grid(row=1, column=0, padx=5, pady=5)
      author_entry = tk.Entry(edit_window)
      author_entry.insert(0, values[1])
      author_entry.grid(row=1, column=1, padx=5, pady=5)

      type_label = tk.Label(edit_window, text="Type:")
      type_label.grid(row=2, column=0, padx=5, pady=5)
      type_var = tk.StringVar(edit_window)
      type_var.set(values[2])  # Default value
      type_options = ["paper", "digital", "audio"]
      type_dropdown = ttk.Combobox(edit_window,
                                   textvariable=type_var,
                                   values=type_options)
      type_dropdown.grid(row=2, column=1, padx=5, pady=5)

      note_label = tk.Label(edit_window, text="Note:")
      note_label.grid(row=3, column=0, padx=5, pady=5)
      note_entry = tk.Text(edit_window, height=5, width=30)
      note_entry.insert("1.0", values[3])
      note_entry.grid(row=3, column=1, padx=5, pady=5)

      def save_changes():
        new_title = title_entry.get()
        new_author = author_entry.get()
        new_type = type_var.get()
        new_note = note_entry.get("1.0", "end-1c")

        # Update the treeview
        self.tree.item(self.selected_item,
                       values=(new_title, new_author, new_type, new_note))

        # Update the DataFrame
        self.df.loc[int(self.selected_item[1:])] = [
            new_title, new_author, new_type, new_note
        ]
        self.df.to_csv('myShelf.csv', index=False)

        edit_window.destroy()

      save_button = tk.Button(edit_window, text="Save", command=save_changes)
      save_button.grid(row=4, column=0, columnspan=2, pady=10)

  def delete_selected_book(self):
    if self.selected_item:

      # Delete from treeview
      self.tree.delete(self.selected_item)
      # Delete from dataframe
      row_index = int(
          self.selected_item[1:])  # Extract row index from treeview id
      self.df = self.df.drop(index=row_index)
      self.df.to_csv('myShelf.csv', index=False)
      # Clear the selected item
      self.selected_item = None

    self.edit_button.pack()
    self.delete_button = tk.Button(self.view_tab,
                                   text="Delete",
                                   command=self.delete_selected_book)
    self.delete_button.pack()

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
      self.result = None

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

  def search_book(self, event=None):
    title_search = self.search_entry.get()
    if title_search:
      openlibrary = "https://openlibrary.org/search.json?title=" + title_search
      response = requests.get(openlibrary)
      info = response.json()
      if info['docs']:
        self.results_listbox.delete(0, tk.END)  # Clear previous results
        for i in range(min(5, len(info['docs']))):  # Show up to 5 results
          author = info['docs'][i]['author_name'][0] if 'author_name' in info[
              'docs'][i] else "N/A"
          publish_year = info['docs'][i][
              'first_publish_year'] if 'first_publish_year' in info['docs'][
                  i] else "N/A"
          self.results_listbox.insert(
              tk.END,
              f"{info['docs'][i]['title']} by {author} ({publish_year})")
          if i == 0:
            self.result = {
                'title': info['docs'][i]['title'],
                'author': author,
                'publish_year': publish_year
            }
      else:
        self.results_listbox.delete(0, tk.END)  # Clear previous results
        self.results_listbox.insert(tk.END,
                                    f"Nothing found for {title_search}")


if __name__ == "__main__":
  LibApp()