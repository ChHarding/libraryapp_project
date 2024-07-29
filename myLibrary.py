import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

import requests

con=sqlite3.connect('myLibrary.db')
cur=con.cursor()

class Main(object):
  def __init__(self, master):
    self.master = master

    def displayStats(evt):
      count_books=cur.execute("SELECT count(book_id) FROM books").fetchall()
      count_paper=cur.execute("SELECT COUNT(book_id) FROM books WHERE book_type='Paper'").fetchall()
      count_audio=cur.execute("SELECT COUNT(book_id) FROM books WHERE book_type='Audio'").fetchall()
      count_digital=cur.execute("SELECT COUNT(book_id) FROM books WHERE book_type='Digital'").fetchall()
      self.lbl_book_count.config(text="Total Books: "+str(count_books[0][0])+" books in library")
      self.paper_count.config(text="Paper Books: "+str(count_paper[0][0])+" books in library")
      self.audio_count.config(text="Audio Books: "+str(count_audio[0][0])+" books in library")
      self.digital_count.config(text="Digital Books: "+str(count_digital[0][0])+" books in library")
      displayBooks(self)

    
    def displayBooks(self):
      books=cur.execute("SELECT * FROM books").fetchall()
      count = 0 # CH: this should be initialized here, not outside the function
      
      self.list_books.delete(0, END)
      for book in books:
        print(book)
        self.list_books.insert(count,str(book[0])+" - "+book[1])
        count +=1

      def displayBookInfo(evt):
        value=str(self.list_books.get(self.list_books.curselection()))
        id=value.split(" - ")[0]
        book =cur.execute("SELECT * FROM books WHERE book_id=?",(id,))
        book_info=book.fetchall()
        print(book_info)

        self.list_details.delete(0,END)
        self.list_details.insert(0,"Book Name :"+book_info[0][1])
        self.list_details.insert(1,"Book Author :"+book_info[0][2]) 
        self.list_details.insert(2,"Book Type :"+book_info[0][3]) 
        self.list_details.insert(3,"Book Notes :"+book_info[0][4]) 
        
      
      self.list_books.bind('<<ListboxSelect>>', displayBookInfo)
      self.tabs.bind('<<NotebookTabChanged>>', displayStats)
      
    
    
    #frames
    mainframe=Frame(self.master)
    mainframe.pack()


    #topframe
    topframe=Frame(mainframe,width=1350,height=70,bg='#f8f8f8',padx=20,relief=SUNKEN,
                  borderwidth=2)
    topframe.pack(side=TOP,fill=X)


    #centerframe
    centerframe=Frame(mainframe,width=1350,height=680,relief=RIDGE,bg='#e0f0f0')
    centerframe.pack(side=TOP)


    #center left frame
    centerleftframe=Frame(centerframe,width=900,height=680,bg='#e0f0f0',relief=SUNKEN,
                         borderwidth=2)
    centerleftframe.pack(side=LEFT)


    #center right frame
    centerrightframe=Frame(centerframe,width=450,height=680,bg='#e0f0f0',relief=SUNKEN,
                          borderwidth=2)
    centerrightframe.pack(side=TOP)

    #searchbar
    search_bar=LabelFrame(centerrightframe,width=440,height=75,text='Enter Text',
                          bg='#9bc9ff')
    search_bar.pack(fill=BOTH)
    self.lbl_search=Label(search_bar,text='Search',bg='#9bc9ff',fg='white',
                          font='Vardana 10 bold')
    self.lbl_search.grid(row=0,column=0,padx=10,pady=10)
    self.ent_search=Entry(search_bar,width=30,font='Vardana 10',bd=5)
    self.ent_search.grid(row=0,column=1,padx=5,pady=10,columnspan=3)
    self.btn_search=Button(search_bar,text='Search',font='verdana 10',
                           bg='#fcc324',fg='white', command=self.searchmyLibrary)
    self.btn_search.grid(row=0,column=4,padx=10,pady=10)


    #listbar
    list_bar=LabelFrame(centerrightframe,width=440,height=175,text='List Box',
                        bg='#fcc324')
    list_bar.pack(fill=BOTH)
    lbl_list=Label(list_bar,text='Sort by',font='verdana 10',
                   bg='#fcc324',fg='#2488ff')
    lbl_list.grid(row=0,column=2,padx=20,pady=10)
    self.listChoice = IntVar() # Instantiate the IntVar
    rb1=Radiobutton(list_bar,text='All Books',variable=self.listChoice,value=1,bg='#fcc324')
    rb1.grid(row=1,column=0,padx=5,pady=10)
    rb2=Radiobutton(list_bar,text='Paper',variable=self.listChoice,value=2,bg='#fcc324')
    rb2.grid(row=1,column=1,padx=5,pady=10)
    rb3=Radiobutton(list_bar,text='Audio',variable=self.listChoice,value=3,bg='#fcc324')
    rb3.grid(row=1,column=2,padx=5,pady=10)    
    rb4=Radiobutton(list_bar,text='Digital',variable=self.listChoice,value=4,bg='#fcc324')
    rb4.grid(row=1,column=3,padx=5,pady=10)
    btn_list=Button(list_bar,text='List Books',bg='#2488ff',fg='white',font='verdana 10',command=self.listBooks)
    btn_list.grid(row=1,column=4,padx=10,pady=10)


    #title and image
    image_bar=Frame(centerrightframe,width=440,height=350)
    image_bar.pack(fill=BOTH)
    self.title_right=Label(image_bar,text='Welcome to your Library',font='vedana 10 bold')
    self.title_right.grid(row=0)


    ###################TABS####################
    self.tabs=ttk.Notebook(centerleftframe,width=900,height=660)
    self.tabs.pack()

    #tab1
    tab1=ttk.Frame(self.tabs,width=900,height=660)
    self.tabs.add(tab1,text='Books',compound=LEFT)

    #list books
    self.list_books=Listbox(tab1,width=40,height=30,bd=5,font='verdana 10')
    self.sbar_books=Scrollbar(tab1,orient=VERTICAL)
    self.list_books.grid(row=0,column=0,padx=(5,0),pady=5,sticky=N)
    self.sbar_books.config(command=self.list_books.yview)
    self.list_books.config(yscrollcommand=self.sbar_books.set)
    self.sbar_books.grid(row=0,column=0,sticky=N+S+E)
    #list details
    self.list_details=Listbox(tab1,width=80,height=30,bd=5,font='verdana 10')
    self.list_details.grid(row=0,column=1,padx=(5,0),pady=5,sticky=N)

    #tab2
    tab2=ttk.Frame(self.tabs,width=900,height=660)
    self.tabs.add(tab2,text='Details',compound=LEFT)

    #statistic
    self.lbl_book_count= Label(tab2,text='',pady=5,font='verdana 14 bold')
    self.lbl_book_count.grid(row=0)
    self.audio_count= Label(tab2,text='',pady=5,font='verdana 14 bold')
    self.audio_count.grid(row=1,sticky=W)
    self.digital_count= Label(tab2,text='',pady=5,font='verdana 14 bold')
    self.digital_count.grid(row=2,sticky=W)
    self.paper_count= Label(tab2,text='',pady=5,font='verdana 14 bold')
    self.paper_count.grid(row=3,sticky=W)

    #functions
    displayBooks(self)
    displayStats(self)

    ###################Tool Bar####################


    #add Book
    self.btnbook= Button(topframe,text='Add Book',width=20,height=2,bg='#9bc9ff',compound=LEFT,
                        font=('verdana',10,'bold'),command=self.addBook)
    self.btnbook.pack(side=LEFT,padx=10)


    #search Book
    self.btnsearch= Button(topframe,text='Edit Selection',width=20,height=2,bg='#9bc9ff',compound=LEFT,
                           font=('vardana',10,'bold'), 
                           command=self.editBook)
    self.btnsearch.pack(side=LEFT)


  def editBook(self):
    value=str(self.list_books.get(self.list_books.curselection()))
    id=value.split(" - ")[0]
    book =cur.execute("SELECT * FROM books WHERE book_id=?",(id,))
    book_info=book.fetchall()
    edit=EditBook(book_info)
  
  def addBook(self):
    add=AddBook()


  def searchmyLibrary(self):
    value=self.ent_search.get()
    search=cur.execute("SELECT * FROM books WHERE book_name LIKE ?",
                       ('%'+value+'%',)).fetchall()
    print(search)
    self.list_books.delete(0,END)
    count=0
    for book in search:
      self.list_books.insert(count,str(book[0])+" - "+book[1])
      count +=1

  def listBooks(self):
    value=self.listChoice.get()
    if value==1:
      allbooks=cur.execute("SELECT * FROM books").fetchall()
      self.list_books.delete(0,END)

      count=0
      for book in allbooks:
        self.list_books.insert(count,str(book[0])+" - "+book[1])
        count +=1

    elif value==2:
      books_in_library=cur.execute("SELECT * FROM books WHERE book_type='Paper'").fetchall()
      self.list_books.delete(0,END)
      count=0
      for book in books_in_library:
        self.list_books.insert(count,str(book[0])+" - "+book[1])
        count +=1

    elif value==3:
      books_in_library=cur.execute("SELECT * FROM books WHERE book_type='Audio'").fetchall()
      self.list_books.delete(0,END)
      count=0
      for book in books_in_library:
        self.list_books.insert(count,str(book[0])+" - "+book[1])
        count +=1

    elif value==4:
      books_in_library=cur.execute("SELECT * FROM books WHERE book_type='Digital'").fetchall()
      self.list_books.delete(0,END)
      count=0
      for book in books_in_library:
        self.list_books.insert(count,str(book[0])+" - "+book[1])
        count +=1

def main():
  root = Tk()
  app = Main(root)
  root.title("Library Management System")
  root.geometry("1350x750+350+200")
  root.mainloop()

class EditBook(Toplevel):
  def __init__(self, book_id):
    Toplevel.__init__(self)
    self.geometry('650x550')
    self.title("Edit Book")
    self.resizable(False,False)

    self.book_id = book_id

    ##################Frames###################

    #TopFrame
    self.topframe=Frame(self,height=150,bg='white')
    self.topframe.pack(fill=X)

    #BottomFrame
    self.bottomframe=Frame(self,height=400,bg='#fcc324')
    self.bottomframe.pack(fill=X)

    ##################Header###################
    self.heading=Label(self.topframe,text='Edit Book',
                       font='verdana 20 bold',fg="#003f8a",bg='white')
    self.heading.place(x=250,y=60)

    ##################Form###################
    #Title
    self.lbl_name=Label(self.bottomframe,text='Book Title:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_name.place(x=40,y=40)
    self.ent_name=Entry(self.bottomframe,width=30,bd=4)
    self.ent_name.place(x=150,y=45)
    #Author
    self.lbl_author=Label(self.bottomframe,text='Author:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_author.place(x=40,y=80)
    self.ent_author=Entry(self.bottomframe,width=30,bd=4)
    self.ent_author.place(x=150,y=85)
    #Type
    self.lbl_type=Label(self.bottomframe,text='Type:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_type.place(x=40,y=120)
    self.ent_type=StringVar(self)
    self.ent_type.set("Paper")  # Default value
    self.ent_type_options=['Paper','Audio','Digital']
    self.ent_type_dropdown=ttk.Combobox(self.bottomframe,textvariable=
                                        self.ent_type,
                                        values=self.ent_type_options)
    self.ent_type_dropdown.place(x=150,y=125)
    #Notes
    self.lbl_notes=Label(self.bottomframe,text='Notes:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_notes.place(x=40,y=160)
    self.ent_notes=Text(self.bottomframe,width=35,height=10,bd=4)
    self.ent_notes.place(x=150,y=165)
    #Button
    button=Button(self.bottomframe,text='Save Changes',command=self.saveChanges,
                  font='verdana 10 bold',bg='#2488ff',fg='white')
    button.place(x=300,y=350)

    # Populate the form with the book's data
    self.populateForm()

  def populateForm(self):
    book = cur.execute("SELECT * FROM books WHERE book_id=?", (self.book_id,)).fetchone()
    if book:
      self.ent_name.insert(0, book[1])
      self.ent_author.insert(0, book[2])
      self.ent_type.set(book[3])
      self.ent_notes.insert(END, book[4])

  def saveChanges(self):
    name=self.ent_name.get()
    author=self.ent_author.get()
    type=self.ent_type.get()
    notes=self.ent_notes.get("1.0",END)

    if name and author and type !="":
      try:
        query="UPDATE books SET book_name=?, book_author=?, book_type=?, book_notes=? WHERE book_id=?"
        cur.execute(query,(name,author,type,notes, self.book_id))
        con.commit()
        messagebox.showinfo("Success","Book Updated Successfully")
        self.destroy()
      except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}") 

class AddBook(Toplevel):
  def __init__(self):
    Toplevel.__init__(self)
    self.geometry('650x550')
    self.title("Add Book")
    self.resizable(False,False)

    ##################Frames###################

    #TopFrame
    self.topframe=Frame(self,height=150,bg='white')
    self.topframe.pack(fill=X)

    #BottomFrame
    self.bottomframe=Frame(self,height=400,bg='#fcc324')
    self.bottomframe.pack(fill=X)

    ##################Header###################
    self.heading=Label(self.topframe,text='Add Book',
                       font='verdana 20 bold',fg="#003f8a",bg='white')
    self.heading.place(x=250,y=60)

    ##################Form###################
    #Title
    self.lbl_name=Label(self.bottomframe,text='Book Title:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_name.place(x=40,y=40)
    self.ent_name=Entry(self.bottomframe,width=30,bd=4)
    self.ent_name.insert(0,"")
    self.ent_name.place(x=150,y=45)
    #Author
    self.lbl_author=Label(self.bottomframe,text='Author:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_author.place(x=40,y=80)
    self.ent_author=Entry(self.bottomframe,width=30,bd=4)
    self.ent_author.insert(0,"")
    self.ent_author.place(x=150,y=85)
    #Type
    self.lbl_type=Label(self.bottomframe,text='Type:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_type.place(x=40,y=120)
    self.ent_type=StringVar(self)
    self.ent_type.set("Paper")  # Default value
    self.ent_type_options=['Paper','Audio','Digital']
    self.ent_type_dropdown=ttk.Combobox(self.bottomframe,textvariable=
                                        self.ent_type,
                                        values=self.ent_type_options)
    self.ent_type_dropdown.place(x=150,y=125)
    #Notes
    self.lbl_notes=Label(self.bottomframe,text='Notes:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_notes.place(x=40,y=160)
    self.ent_notes=Text(self.bottomframe,width=35,height=10,bd=4)
    self.ent_notes.insert(END,"Enter Notes")
    self.ent_notes.place(x=150,y=165)
    #Button
    button=Button(self.bottomframe,text='Add Book',command=self.addBook2,
                  font='verdana 10 bold',bg='#2488ff',fg='white')
    button.place(x=300,y=350)
    #button 2
    button=Button(self.bottomframe,text='Search the Web',command=self.__init__2,
                  font='verdana 10 bold',bg='#2488ff',fg='white')
    button.place(x=150,y=10)

  def searchBook(self):
    title_search = self.ent_name2.get()
    if title_search:
      openlibrary = "https://openlibrary.org/search.json?title=" + title_search
      response = requests.get(openlibrary)
      info = response.json()
      if info['docs']:
        self.results_listbox.delete(0,0)  # Clear previous results
        for i in range(min(5, len(info['docs']))):  # Show up to 5 results

          # CH if you use a long expression multiple times, it's better to store it in a variable
          curr = info['docs'][i]
          author = curr.get('author_name', ["N/A"])[0] # CH: if author_name is not present, return ["N/A"] and take the first element
          publish_year = curr.get('first_publish_year', "N/A") # CH: if first_publish_year is not present, return "N/A"

          self.results_listbox.insert(0,
              f"{info['docs'][i]['title']} by {author} ({publish_year})")


      else:
        self.results_listbox.delete(0,0)  # Clear previous results
        self.results_listbox.insert(0, f"Nothing found for {title_search}")

  def __init__2(self):
    Toplevel.__init__(self)
    self.geometry('650x550')
    self.title("Search for a Book")
    self.resizable(False,False)

    ##################Frames###################

    #TopFrame
    self.topframe=Frame(self,height=150,bg='white')
    self.topframe.pack(fill=X)

    #BottomFrame
    self.bottomframe=Frame(self,height=400,bg='#fcc324')
    self.bottomframe.pack(fill=X)

    ##################Header###################
    self.heading=Label(self.topframe,text='Search for a Book',
                       font='verdana 20 bold',fg="#003f8a",bg='white')
    self.heading.place(x=250,y=60)

    ##################Form###################
    #Title
    self.lbl_name=Label(self.bottomframe,text='Book Title:',
                        font='verdana 10 bold',fg='white',bg='#fcc324')
    self.lbl_name.place(x=40,y=40)
    self.ent_name2=Entry(self.bottomframe,width=30,bd=4)
    self.ent_name2.insert(0,"")
    self.ent_name2.place(x=150,y=45)
    #Results
    self.lbl_results=Label(self.bottomframe,text='Results:',
                          font=('verdana 10 bold'),fg='white',bg='#fcc324')
    self.lbl_results.place(x=40,y=120)
    self.results_listbox = Listbox(self.bottomframe, height=10, width=30)
    self.results_listbox.place(x=150,y=125)
    #Button
    button=Button(self.bottomframe,text='Add Selection',command=self.put_result_in_add_book_form,
                   font='verdana 10 bold',bg='#2488ff',fg='white')
    button.place(x=150,y=300)
    #button 2
    button=Button(self.bottomframe,text='Search',command=self.searchBook,
                  font='verdana 10 bold',bg='#2488ff',fg='white')
    button.place(x=150,y=85)
    

  def put_result_in_add_book_form(self):
    if self.results_listbox:  # Check if self.result is not None
      selected_index = self.results_listbox.curselection()
      if selected_index:
        selected_item = self.results_listbox.get(selected_index[0])
        # Assuming the listbox items are in the format "Title by Author (Year)"
        title, author = selected_item.split(" by ", 1)
        author = author.split(" (")[0]  # Remove the year

        self.ent_name.delete(0,0)  # Clear any existing text in the entry
        self.ent_name.insert(0, title)
        self.ent_author.delete(0,0)
        self.ent_author.insert(0, author)
        self.destroy()
    

  def addBook2(self):
    name=self.ent_name.get()
    author=self.ent_author.get()
    type=self.ent_type.get()
    notes=self.ent_notes.get("1.0",END)

    if name and author and type !="":
      try:
        query="INSERT INTO 'books' (book_name,book_author,book_type,book_notes) VALUES (?,?,?,?)"
        cur.execute(query,(name,author,type,notes))
        con.commit()
        messagebox.showinfo("Success","Book Added Successfully")
        self.destroy()

      except:
        messagebox.showerror("Error","Cant add to your library.")
    else:
      messagebox.showerror("Error","Fields cannot be empty.")

if __name__ == '__main__':
  main()