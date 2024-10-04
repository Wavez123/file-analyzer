import tkinter as tk
from tkinter import ttk
import random
import string

class MWEapp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # these containers are perhaps a bit too much for this example
        # but in the full code, this class is inheriting from a larger design
        self.wndcnt = ttk.Frame(self)
        self.wndcnt.pack(fill=None, expand=False, side="top", padx=20, pady=20)

        # add container to table
        tblcnt = ttk.Frame(self)
        tblcnt.pack(anchor="center")

        # add scrollbar
        scrollbary = ttk.Scrollbar(tblcnt, orient="vertical")
        scrollbary.grid(row=0, column=1, sticky="ns")
        scrollbarx = ttk.Scrollbar(tblcnt, orient="horizontal")
        scrollbarx.grid(row=1, column=0, sticky="ew")

        # use treeview to create table
        self.dynamictable = ttk.Treeview(
            tblcnt,
            column=("#1", "#2", "#3", "#4", "#5"),
            show="headings",
            height=30,
            xscrollcommand=scrollbarx.set,
            yscrollcommand=scrollbary.set
        )
        # bind mouse click to scroll callbacks
        self.dynamictable.bind("<Button-1>", self._scroll_init)
        self.dynamictable.bind("<B1-Motion>", self._scroll)
        self.last_y = 0
        self.dynamictable.grid(row=0, column=0, sticky="nsew")
        scrollbarx["command"] = self.dynamictable.xview
        scrollbary["command"] = self.dynamictable.yview

        # add headers
        self.dynamictable.heading("#1", anchor="w", text="Header 1")
        self.dynamictable.heading("#2", anchor="w", text="Header 2")
        self.dynamictable.heading("#3", anchor="w", text="Header 3")
        self.dynamictable.heading("#4", anchor="w", text="Header 4")
        self.dynamictable.heading("#5", anchor="w", text="Header 5")
        # add columns
        self.dynamictable.column("#1", anchor="w", width=100, stretch=False)
        self.dynamictable.column("#2", anchor="w", width=200, stretch=False)
        self.dynamictable.column("#3", anchor="w", width=200, stretch=False)
        self.dynamictable.column("#4", anchor="w", width=150, stretch=False)
        self.dynamictable.column("#5", anchor="w", width=500, stretch=False)
        # fill table at constant rate
        self._fill_tbl()

    def _rstr(self, N):
        #generate pseudo string with N characters.
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

    def _dummy_data(self):
        # dummy data
        longstring = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

        # dummy data is a list of 5-tuples containing strings
        database_data = []
        for i in range(50):
            if i == 10:
                database_data.append((str(i),self._rstr(10),self._rstr(15),self._rstr(6),longstring))
            else:
                database_data.append((str(i),self._rstr(10),self._rstr(15),self._rstr(6),self._rstr(30)))

        return database_data

    def _fill_tbl(self):

        database_data = self._dummy_data()

        # clear previous table
        self.dynamictable.delete(*self.dynamictable.get_children())

        # add dummy data
        for row in database_data:
            self.dynamictable.insert("","end",values=(row[0],row[1],row[2],row[3],row[4],),)

        # keep refreshing data each second
        #self.after(1000, self._fill_tbl)

    # callbacks for touch scroll
    def _scroll_init(self, event):
        self.last_y = event.y
    def _scroll(self, event):
        delta = -1 if event.y > self.last_y else 1
        self.last_y = event.y
        self.dynamictable.yview_scroll(delta, "units")

if __name__ == "__main__":
    app = MWEapp()
    app.mainloop()
