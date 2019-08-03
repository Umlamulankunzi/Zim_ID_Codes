"""Main Script of Zim Code Application

Main module script imports relevant modules and launches the
application
"""


import os
import difflib

from tkinter import *
from tkinter import ttk, messagebox

import database_init

__author__ = "Umlamulankunzi Dev (Prince D Jele)"
__copyright__ = "Copyright 2019, Umlamulankunzi Dev"
__credits__ = ["Umlamulankunzi"]
__license__ = "Apache License-2.0"
__version__ = "1.04.25"
__maintainer__ = "Umlamulankunzi Dev"
__email__ = "umlamulankunzi@gmail.com"
__status__ = "Production"
__date__ = "20/02/2019"



def start_app():
    '''Starting point when module is the main routine.'''

    root = Tk()
    Application(root)
    root.mainloop()


class Application:
    '''This class configures and populates the main root window. master
    is the main container root window.'''

    def __init__(self, master=None):
        """Parameters
        -------------------------
        master : tkinter.Tk() instance
            The main root window
        """

        # database initialisation
        self.db = database_init.Data()

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        font10 = "-family {Tahoma} -size 10 -weight normal -slant" \
                 " roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor),
                                        ('active', _ana2color)])
        # self.style.configure("Treeview.Heading", background="#7aafff",
        #                      font=("calibri", 8, "bold"))
        self.style.configure("TButton", background=_bgcolor,
                             foreground="green",
                             font=("Tahoma", 10, "bold"))
        self.style.configure("bk.TButton", background=_bgcolor,
                             foreground="red",
                             font=("Tahoma", 10, "bold"))


        # Creating custom style for Treeview heading
        self.custom_style = ttk.Style()
        self.custom_style.element_create("Custom.Treeheading.border",
                                         "from", "default")

        self.custom_style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side': 'right', 'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        self.custom_style.configure("Custom.Treeview.Heading",
                                    background=_bgcolor, foreground="black",
                                    relief="flat", font=("calibri", 11, "bold"))
        self.custom_style.map("Custom.Treeview.Heading",
                              relief=[('active', 'groove'),
                                      ('pressed', 'sunken')])


        self.master = master
        self.master.geometry("600x334+451+152")
        self.master.title("Zim National ID Codes")
        self.master.resizable(0, 0)
        self.master.configure(background="#d9d9d9")
        self.master.configure(height="300")
        self.master.iconbitmap('main_icon_small.ico')
        self.master.bind('<Return>', lambda e: self.search())
        
        # creating menus on the menu bar
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Shortcuts
        self.kb_shortcut_menu = Menu(self.menu_bar, tearoff=0)
        
        self.kb_shortcut_menu.add_command(label='Clear entry field    -Backspace')
        self.kb_shortcut_menu.add_command(label='\nSearch                    -Enter')
        								  #'\n')
        self.menu_bar.add_cascade(label='Shortcuts', menu=self.kb_shortcut_menu)

        # Help menu
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label='How to use', command=
                                   lambda:self.help("how_to"))
        self.help_menu.add_command(label='Terms and Conditions', command=
                                   lambda:self.help("t&cs"))
        self.help_menu.add_separator()
        self.help_menu.add_command(label='About', command=
                                   lambda:self.help("about"))

        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        main_label = Label(master, bg="#d9d9d9", disabledforeground="#a3a3a3",
                           fg="green", text="Zim ID Codes Finder",
                           font=("Calibri", 20, "bold"), width=214)

        dev_label = Label(master, bg="#d9d9d9", disabledforeground="#a3a3a3",
                          fg="gray",
                          text="Developed by\nUMLAMULANKUNZI\n\u00a9 2019", )

        self.image_lb = Label(master, background="#d9d9d9",
                              disabledforeground="#a3a3a3", fg="#000000",
                              width=114)

        self.search_var = StringVar()
        self.search_entry = Entry(master, bg="white", font=font10, fg="#000000",
                                  disabledforeground="#a3a3a3",
                                  width=234, insertbackground="black",
                                  justify="center",
                                  textvariable=self.search_var)
        self.search_entry.focus()
        self.search_var.trace_add("write", self.validate_command)

        self.radio_var = StringVar()
        self.radio_var.set("0")
        self.radio_1 = ttk.Radiobutton(master, value="0", text="Province",
                                       variable=self.radio_var, takefocus='0',
                                       command=self.rad_select)

        self.radio_2 = ttk.Radiobutton(master, text="District", value="1",
                                       variable=self.radio_var, takefocus='0',
                                       command=self.rad_select)

        self.radio_3 = ttk.Radiobutton(master, text="ID Code", value="2",
                                       variable=self.radio_var, takefocus='0',
                                       command=self.rad_select, width=75)


        self.btn_txt = StringVar()
        self.sech_btn = ttk.Button(master, command=self.search, takefocus='0',
                                   width=137, textvariable=self.btn_txt)

        self.browse_frm = LabelFrame(master, relief=GROOVE, fg="black",
                                     text="Browse ID Codes", bg="#d9d9d9",
                                     width=270, font=("Tahoma", 10))

        self.browse_lstbx = ScrolledListBox(self.browse_frm, bg="white",
                                            disabledforeground="#a3a3a3",
                                            font=font10, fg="black",
                                            highlightbackground="#d9d9d9",
                                            highlightcolor="#d9d9d9",
                                            selectbackground="#42e5f4",
                                            selectforeground="black", width=10)
        self.update(self.browse_lstbx, action="update browse listbox")
        self.browse_lstbx.bind("<Double-Button-1>", self.browse_select)

        self.back_btn = ttk.Button(self.browse_frm, text=" Back ",
                                   takefocus='0', style="bk.TButton",
                                   command=lambda: self.update(self.browse_treevw,
                                                               action="back to listbox"),
                                   state=DISABLED)

        self.style.configure('Treeview.Heading', font="TkDefaultFont")
        self.browse_treevw = ScrolledTreeView(self.browse_frm,
                                              columns=["Dist", "Code"],
                                              show="headings",
                                              style="Custom.Treeview")
        self.browse_treevw.bind('<Button-1>', self.handle_click)

        self.browse_treevw.heading("Dist", text="District", anchor="w")
        self.browse_treevw.heading("Code", text="ID Code", anchor="center")
        self.browse_treevw.column("Dist", width="171", minwidth="20",
                                  stretch="1", anchor="w")
        self.browse_treevw.column("Code", width="60", minwidth="20",
                                  stretch="1", anchor="center")

        self.results_frm = LabelFrame(master, relief=GROOVE, fg="black",
                                      text="Search Results", bg="#d9d9d9",
                                      width=240, font=("Tahoma", 10))

        self.search_treevw = ScrolledTreeView(self.results_frm,
                                              columns=["Dist", "Code"],
                                              show="headings",
                                              style="Custom.Treeview")
        self.search_treevw.bind('<Button-1>', self.handle_click)

        self.search_treevw.heading("Dist", text="District", anchor="w")
        self.search_treevw.heading("Code", text="ID Code", anchor="center")

        self.search_treevw.column("Dist", width="146", minwidth="146",
                                  stretch="1", anchor="w")
        self.search_treevw.column("Code", width="55", minwidth="55",
                                  stretch="1", anchor="center")

        main_label.place(relx=0.32, rely=0.03, height=41, width=222)
        dev_label.place(relx=0.75, rely=0.03, height=41)
        self.image_lb.place(relx=0.03, rely=0.03, height=41, width=56)
        self.search_entry.place(relx=0.05, rely=0.3, height=30, relwidth=0.39)
        self.radio_1.place(relx=0.05, rely=0.21, relwidth=0.12, relheight=0.0,
                           height=21)
        self.radio_2.place(relx=0.18, rely=0.21, relwidth=0.1, relheight=0.0,
                           height=21)
        self.radio_3.place(relx=0.32, rely=0.21, relwidth=0.13,
                           relheight=0.0, height=21)
        self.sech_btn.place(relx=0.13, rely=0.41, height=26, width=140)
        self.browse_frm.place(relx=0.52, rely=0.18, relheight=0.76,
                              relwidth=0.45)
        self.browse_lstbx.place(relx=0.03, rely=0.03, relheight=0.8,
                                relwidth=0.95)
        self.back_btn.place(relx=0.68, rely=0.85, relwidth=0.3)
        self.results_frm.place(relx=0.05, rely=0.57, relheight=0.37,
                               relwidth=0.4)
        self.search_treevw.place(relx=0.02, rely=0.05, relheight=0.85
                                 , relwidth=0.94)

        self.rad_select()

        # Using os module to get list of images to be used by
        # change_img method
        self.counter = 0
        self.image_names = []

        # images contained in seperate resource folder the basepath
        # images named alphabetically for changing in correct order
        basepath = 'gif_resource/'

        with os.scandir(basepath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.image_names.append(entry.name)

        self.display_imgs = [PhotoImage(file=basepath + x) for x in self.image_names]
        master.after(100, self.change_img)

    @staticmethod
    def handle_click(event):
        _widget = event.widget
        if _widget.identify_region(event.x, event.y) == "separator":
            return "break"

    @staticmethod
    def help(action):
        """Show info about the application"""

        if action == 'about':
            title_txt = 'About Zim ID Codes'
            info_text = ' ZIM ID CODES'
            detail_txt = 'Ver ' + __version__ +'\nDeveloped by Umlamulankunzi' \
            			 + '\nPowered by Open Source\n\u00a9 2019'

        elif action == 'how_to':
            title_txt = 'Zim ID Codes Help'
            info_text = '\t\tZIM ID CODES HELP'
            detail_txt = '\n--------------------------------------------------------------------------\n' + \
            '1. Browse ID Codes:\n' + \
            '\t- Double Click on Province name\n' + \
            '\t- View District and codes of province\n' + \
            '\t- Click Back button to go back to province list\n' + \
            '\n--------------------------------------------------------------------------\n' + \
            '2. Search:\n' + \
            '\t- Search by Province, District or Code\n' + \
            '\t- By selecting appropriate type above search entry\n' + \
            '\t- Enter search term in search Entry box\n' + \
            '\t- View Search results in Search results box' +\
            '\n--------------------------------------------------------------------------'
        elif action == 't&cs':

            title_txt = "Zim ID Codes T & Cs"
            info_text ="Copyright 2019 Umlamulankunzi Dev (PD Jele)"
            detail_txt = """Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the
License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless  required  by  applicable  law or agreed to 
in writing, software distributed under the License
is  distributed  on  an  "AS  IS"  BASIS,  WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either
express  or  implied.  See  the  License  for  the 
specific  language  governing  permissions  and
limitations under the License."""
        
        messagebox.showinfo(title=title_txt, message=info_text, detail=detail_txt)


    def change_img(self):
        """Changes image of image label in main window

        Creates gif animation by changing the image of image label
        after 100ms.
        """

        self.image_lb.configure(image=self.display_imgs[self.counter])
        self.counter += 1
        if self.counter == len(self.image_names):
            self.counter = 0
        self.master.after(100, self.change_img)

    def validate_command(self, *_args):
        """Validates User input into search entry widget"""

        if self.radio_var.get() == '2':
            self.search_var.set(self.search_var.get().strip())
            try:
                int(self.search_var.get())
                if len(self.search_var.get()) == 3:
                    raise ValueError
            except ValueError:
                self.search_var.set(self.search_var.get()[:len(self.search_var.get()) - 1])

        self.search_var.set(self.search_var.get().title())
        if self.search_var.get().strip() == "":
            self.search_var.set("")
        elif self.search_var.get()[-2:] == "  ":
            self.search_var.set(self.search_var.get()[:len(self.search_var.get()) - 1])
        try:
            if len(self.search_var.get()) == 30:
                raise ValueError
        except ValueError:
            self.search_var.set(self.search_var.get()[:len(self.search_var.get()) - 1])

    def update(self, w, **kwargs):
        """Update information on Treeview widgets or listbox widget

        Parameters
        ----------
        w : tkinter.TreeView or tkinter.Listbox Widget
            The widget to be updated
        
        keyword Args:
            action: str
                defines action to be done by function valid options
                include:
                    - update browse listbox: updates listbox
                    - update search treeview: updates search treewview
                      widget
                    - back to listbox: deletes info on browse treeview
                      widget and places back the list box

            data: list
                defines data to be to be updated on widget w, 
                optional for listbox

            prov: str
                defines the province for selected data 
                optional for listbox
            """
        if kwargs["action"] == "update browse listbox":
            # data = self.db.query(col="all")
            provs = self.db.get("prov")

            for prov in provs:
                w.insert("end", " " + prov)

        elif kwargs["action"] == "update search treeview":
            self.results_frm.configure(text=kwargs["prov"], foreground="blue",
                                       font=("Tahoma", 12, "bold"))
            self.clear_treeview(w)

            for info in kwargs["data"]:
                w.insert("", "end", values=(info[1:]))

        elif kwargs["action"] == "back to listbox":
            self.clear_treeview(w)
            w.place_forget()
            self.browse_lstbx.place(relx=0.03, rely=0.03, relheight=0.8,
                                    relwidth=0.95)
            self.back_btn.configure(state=DISABLED)
            self.browse_frm.configure(text="Browse ID Codes", fg="black",
                                      font=("Tahoma", 10))

    @staticmethod
    def clear_treeview(treeview_widget):
        """Clear treeview widget

        Parameters
        ----------
        treeview_widget: tkinter.Treeview Widget instance
        """

        for row in treeview_widget.get_children():
            treeview_widget.delete(row)

    def browse_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        prov = widget.get(selection[0])

        # populating with selected province districts
        info = self.db.query(prov, "province", col1="district", col2="code")
        for dist in info:
            self.browse_treevw.insert('', 'end', values=dist)

        self.browse_lstbx.place_forget()
        self.browse_treevw.place(relx=0.03, rely=0.03, relheight=0.8,
                                 relwidth=0.95)

        self.back_btn.configure(state=NORMAL)
        self.browse_frm.configure(text=prov)
        self.browse_frm.configure(foreground="blue", font=("Tahoma", 12, "bold"))

    def rad_select(self):
        """Change search button text on radio button select"""

        if self.radio_var.get() == "0":
            self.btn_txt.set("Search by Province")
        elif self.radio_var.get() == "1":
            self.btn_txt.set("Search by District")
        elif self.radio_var.get() == "2":
            self.btn_txt.set("Search by ID Code")
        self.search_var.set("")
        self.results_frm.configure(text="Search Results", fg="black",
                                   bg="#d9d9d9", font=("Tahoma", 10))


    def close_match(self, word, search_type=None):
        """Find close matches

        Find possible match for incorrectly spelled user input

        Parameters
        ----------
        word: str
            User input, used to find possible match
        search_type: str
            Search type used to define possibilities list from which
            to find correct match
        """
        possibilities = []

        if search_type == "Province":
            possibilities = self.db.get("prov")
        elif search_type == "District":
            possibilities = self.db.get("dist")
        elif search_type == "Code":
            possibilities = self.db.get("code")

        match = difflib.get_close_matches(word, possibilities, n=1, cutoff=0.6)
        if match:
            return match[0]
        else:
            return None

    def search(self):
        """Manages search inquiries and call self.update method with
        result data.
        """
        res = None
        search_term = self.search_var.get()
        if search_term in database_init.short_hand:
            search_term = database_init.short_hand[search_term]

        if search_term.strip() == "":
            self.clear_treeview(self.search_treevw)
            messagebox.showinfo(title="Search Error",
                                message="Empty Search!\n"
                                        "Please enter search term\n"
                                        "to return results")
            return None


        elif self.btn_txt.get() == "Search by Province":
            # you need query value and column only
            res = self.db.query(search_term, "province")

        elif self.btn_txt.get() == "Search by District":
            res = self.db.query(search_term, "district")

        elif self.btn_txt.get() == "Search by ID Code":
            res = self.db.query(search_term, "code")

        if res:
            self.update(self.search_treevw, action="update search treeview",
                        data=res, prov=res[0][0])
        else:
            self.clear_treeview(self.search_treevw)
            search_type = {"0": "Province", "1": "District", "2": "ID Code"}
            search_term = self.search_var.get().title()

            posble_word = self.close_match(search_term,
                                           search_type=
                                           search_type[self.radio_var.get()]
                                           )
            if posble_word:
                display_msg = search_type[self.radio_var.get()] + " " + \
                              search_term + "\nNot Found! \nDid you mean\n" + posble_word

                confirm = messagebox.askyesnocancel(title='Search Result',
                                                    message=display_msg)
                if confirm:
                    self.search_entry.delete(0, END)
                    self.search_entry.insert(0, posble_word)
                    res = self.db.query(posble_word,
                                        search_type[self.radio_var.get()])
                    self.update(self.search_treevw, data=res, prov=res[0][0],
                                action="update search treeview")

            else:
                display_msg = search_type[self.radio_var.get()] + " " + \
                              search_term + "\nNot Found"
                messagebox.showinfo(title='Search Result',
                                    message=display_msg)
                return None


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        # self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass

        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)

        methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        # else:
        #     methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
        #               + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)

    return wrapped


class ScrolledListBox(AutoScroll, Listbox):
    """A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


class ScrolledTreeView(AutoScroll, ttk.Treeview):
    """A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed."""

    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


if __name__ == '__main__':
    start_app()
