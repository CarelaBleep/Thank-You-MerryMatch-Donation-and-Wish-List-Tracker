import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from donation import Donation
from wish import Wish

from data_manager import (
    load_donations,
    load_wishes,
    save_donations,
    save_wishes,
    add_donation as db_add_donation,
    add_wish as db_add_wish,
    update_donation as db_update_donation,
    update_wish as db_update_wish,
    delete_donation as db_delete_donation,
    delete_wish as db_delete_wish,
)

#MAIN APPLICATION 

class Merrymatch:
    def __init__(self, root):
        self.root = root
        #Set main window properties 
        self.root.title("THANK YOU MERRY MATCH! DONATION & WISH LIST TRACKER")
        self.root.geometry("1000x700") 
        self.root.configure(bg="white") 

        #Load data from the database upon startup
        self.donations = load_donations() # list for Donation objects
        self.wishes = load_wishes()    # list for Wish objects
        
        #Hook the save function to the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()
        self.refresh_all()

    def on_closing(self):
        try:
            #Save the current state of donations and wishes lists
            save_donations(self.donations)
            save_wishes(self.wishes)
            messagebox.showinfo("Data Saved", "All changes have been successfully saved to the database. BYE BYE!")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving data: {e}")
        finally:
            self.root.destroy()

    def setup_ui(self):
        #Header Frame (Red background)
        header_frame = tk.Frame(self.root, bg="#FF5555")
        header_frame.pack(fill="x")
        
        #Main Title Label
        title = tk.Label(header_frame, text="THANK YOU MERRY MATCH! DONATION AND WISH LIST TRACKER", 
                        font=("Small Fonts", 16, "bold"), fg="#FFFFFF", bg="#FF5555")
        title.pack(pady=(10, 0))

        #SDG Banner Label
        sdg = tk.Label(header_frame, text="SDG 1: NO POVERTY", 
                      font=("small fonts", 10, "bold"), fg="white", bg="#A3D78A")
        sdg.pack(pady=(0, 10))

        #Style  Notebook/Tabs
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=('fixedsys', 10, 'bold'), padding=[15, 10], fg='#B45253')
        style.map('TNotebook.Tab',
                  background=[('selected', '#FFFACD'), ('!selected', '#F0F0F0')])

        style.configure('Treeview', font=('fixedsys', 10))
        style.configure('Treeview.Heading', font=('fixedsys', 11, 'bold'))

        #Main Navigation Notebook/Tabs 
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, fill="both", expand=True, padx=10)

        #tab frames
        self.donations_frame = tk.Frame(self.notebook)
        self.notebook.add(self.donations_frame, text="Donations")
        self.setup_donations_tab()

        self.wishes_frame = tk.Frame(self.notebook)
        self.notebook.add(self.wishes_frame, text="Wish List")
        self.setup_wishes_tab()

        self.matching_frame = tk.Frame(self.notebook)
        self.notebook.add(self.matching_frame, text="Wishy Matchy")
        self.setup_matching_tab()

    def setup_donations_tab(self):
        #Donations tab interface, with buttons and Treeview.

        btn_frame = tk.Frame(self.donations_frame)
        btn_frame.pack(fill="x", pady=(10, 5), padx=5)

        btn_frame.columnconfigure(0, weight=1) 

        #Buttons with commands  
        tk.Button(btn_frame, text="ADD DONATION", command=self.add_donation,
                bg="#A3D78A", font=("fixedsys", 10)).grid(row=0, column=1, padx=5, pady=7, sticky="e")
        tk.Button(btn_frame, text="EDIT SELECTED", command=self.edit_donation,
                bg="#FFE797", font=("fixedsys", 10)).grid(row=0, column=2, padx=5, pady=7, sticky="e")
        tk.Button(btn_frame, text="DELETE SELECTED", command=self.delete_donation,
                bg="#FF5555", font=("fixedsys", 10)).grid(row=0, column=3, padx=5, pady=7, sticky="e")

        #Treeview/Table for displaying data
        columns = ("donor", "item", "quantity", "category", "status", "date")
        self.donation_tree = ttk.Treeview(self.donations_frame, columns=columns, 
                                         show="headings", height=15)
        #Column headings
        self.donation_tree.heading("donor", text="Donor Name")
        self.donation_tree.heading("item", text="Item")
        self.donation_tree.heading("quantity", text="Quantity") 
        self.donation_tree.heading("category", text="Category")
        self.donation_tree.heading("status", text="Status")
        self.donation_tree.heading("date", text="Date")
        
        #Configure column widths and alignment
        self.donation_tree.column("quantity", width=80, anchor="center")
        self.donation_tree.column("status", width=100, anchor="center")
        self.donation_tree.pack(pady=10, fill="both", expand=True, padx=5)

        #Stats Label
        self.donation_stats = tk.Label(self.donations_frame, text="", 
                                      font=("fixedsys", 14, "bold"), fg="#B45253")
        self.donation_stats.pack(pady=5)

    def setup_wishes_tab(self):
        #Wish List tab interface
        btn_frame = tk.Frame(self.wishes_frame)
        btn_frame.pack(fill="x", pady=(10, 5), padx=5)

        btn_frame.columnconfigure(0, weight=1) 

        #Buttons with commands (ADD, EDIT, DELETE)
        tk.Button(btn_frame, text="ADD WISH", command=self.add_wish, 
                 bg="#A3D78A", font=("fixedsys", 10)).grid(row=0, column=1, padx=5, pady=7, sticky="e")
        tk.Button(btn_frame, text="EDIT SELECTED", command=self.edit_wish, 
                 bg="#FFE797", font=("fixedsys", 10)).grid(row=0, column=2, padx=5, pady=7, sticky="e")
        tk.Button(btn_frame, text="DELETE SELECTED", command=self.delete_wish, 
                 bg="#FF5555", font=("fixedsys", 10)).grid(row=0, column=3, padx=5, pady=7, sticky="e")

        #Treeview/Table for displaying data
        columns = ("recipient", "item", "quantity", "category", "status", "date")
        self.wish_tree = ttk.Treeview(self.wishes_frame, columns=columns, 
                                     show="headings", height=15)
        self.wish_tree.heading("recipient", text="Recipient Name")
        self.wish_tree.heading("item", text="Item Needed")
        self.wish_tree.heading("quantity", text="Quantity")
        self.wish_tree.heading("category", text="Category")
        self.wish_tree.heading("status", text="Status")
        self.wish_tree.heading("date", text="Date")

        #Configure helpful column widths and alignment
        self.wish_tree.column("quantity", width=80, anchor="center")
        self.wish_tree.column("status", width=100, anchor="center")

        self.wish_tree.pack(pady=10, fill="both", expand=True, padx=5)

        #Stats Label
        self.wish_stats = tk.Label(self.wishes_frame, text="", 
                                   font=("fixedsys", 14, "bold"), 
                                   fg="#B45253")
        self.wish_stats.pack(pady=5)

    def setup_matching_tab(self):
        #Auto Matching tab interface
        tk.Label(self.matching_frame, text="MATCH AVAILABLE DONATION WITH WISH LIST", 
                font=("fixedsys", 14, "bold"), fg="purple").pack(pady=7)

        #Button for matching logic
        tk.Button(self.matching_frame, text="AUTO MATCH GIFTS", 
                 command=self.auto_match, bg="#DDA0DD", 
                 font=("fixedsys", 12, "bold"), height=3, width=20).pack(pady=10)
        
        #Text area to display matching results
        self.match_text = tk.Text(self.matching_frame, height=15, width=80, 
                                 font=("fixedsys", 10), relief=tk.SUNKEN, bd=2)
        self.match_text.pack(pady=10, fill="both", expand=True, padx=5)

        #Button to clear the results text area
        tk.Button(self.matching_frame, text="Clear Matches", 
                 command=self.clear_matches, bg="#FF5555", font=("fixedsys", 10)).pack(pady=5)

    #Utility Functions for Object Retrieval
    def find_donation_by_keys(self, donor, item, date):
        #Finds a Donation object in the list using its key attributes

        for d in self.donations:
            if d.donor == donor and d.item == item and d.date == date:
                return d
        return None

    def find_wish_by_keys(self, recipient, item, date):
        #Finds a Wish object in the list using its key attributes

        for w in self.wishes:
            if w.recipient == recipient and w.item == item and w.date == date:
                return w
        return None

    def _show_dialog(self, title, initial_data=None, is_donation=True, item_to_edit=None, original_keys=None):
        #Dialog for adding and editing items

        #Create a new top-level window for the dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("350x300")
        dialog.transient(self.root)
        dialog.grab_set()

        #Input field setup
        name_label = "Donor Name:" if is_donation else "Recipient Name:"
        item_label = "Item:" if is_donation else "Item Needed:"
        
        #Name Entry
        tk.Label(dialog, text=name_label, font=("fixedsys", 10)).pack(pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack()
        name_entry.insert(0, initial_data.get('name', '') if initial_data else '')

        #Item Entry
        tk.Label(dialog, text=item_label, font=("fixedsys", 10)).pack(pady=5)
        item_entry = tk.Entry(dialog, width=30)
        item_entry.pack()
        item_entry.insert(0, initial_data.get('item', '') if initial_data else '')

        #Quantity Entry
        tk.Label(dialog, text="Quantity:", font=("fixedsys", 10)).pack(pady=5)
        qty_entry = tk.Entry(dialog, width=30)
        qty_entry.pack()
        qty_entry.insert(0, str(initial_data.get('quantity', 1)) if initial_data else '1')

        #Category Dropdown
        tk.Label(dialog, text="Category:", font=("fixedsys", 10)).pack(pady=5)
        cat_var = tk.StringVar(value=initial_data.get('category', 'Toys') if initial_data else 'Toys')
        categories = ["Toys", "Clothes", "Food", "Books", "Electronics", "Other"]
        style = ttk.Style()
        style.configure('TCombobox', font=('fixedsys', 10), fieldbackground='white')
        combo = ttk.Combobox(dialog, textvariable=cat_var, values=categories, state="readonly", style='TCombobox', font=('fixedsys', 10))
        combo.pack()

        def save():
            #Handles input validation and object creation/update
            name = name_entry.get().strip()
            item = item_entry.get().strip()
            qty_str = qty_entry.get().strip()
            
            #Input Validation
            if not name or not item or not qty_str:
                messagebox.showerror("Error", "All fields required!")
                return
            try:
                qty = int(qty_str)
                if qty < 0:
                    messagebox.showerror("Error", "Quantity must be a non-negative integer!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a positive integer!")
                return

            category = cat_var.get()
            date = datetime.now().strftime("%Y-%m-%d")

            if item_to_edit:
                #EDIT Logic: Update attributes of the existing object
                old_keys = original_keys or (
                    (item_to_edit.donor, item_to_edit.item, item_to_edit.date)
                )

                if is_donation:
                    item_to_edit.donor = name
                else:
                    item_to_edit.recipient = name
                
                item_to_edit.item = item
                item_to_edit.category = category
                item_to_edit.quantity = qty
                
                #Reset status if quantity becomes > 0 after editing a matched/fulfilled item
                if qty > 0:
                    if item_to_edit.status == "Matched" and is_donation:
                        item_to_edit.status = "Available"
                    if item_to_edit.status == "Fulfilled" and not is_donation:
                        item_to_edit.status = "Pending"
                else:
                    #If quantity is set to 0, mark as complete
                    item_to_edit.status = "Matched" if is_donation else "Fulfilled" 

                #Persist change immediately with UPDATE to keep DB in sync
                updated = (
                    db_update_donation(*old_keys, item_to_edit)
                    if is_donation else db_update_wish(*old_keys, item_to_edit)
                )
                if updated:
                    messagebox.showinfo("Success", f"{'Donation' if is_donation else 'Wish'} updated!")
                else:
                    messagebox.showwarning("Database", "Update did not save to the database.")

            else:
                #ADD Logic: Create a new object and append it to the list
                status = "Available" if is_donation and qty > 0 else ("Pending" if not is_donation and qty > 0 else "Matched/Fulfilled")

                if is_donation:
                    new_item = Donation(name, item, qty, category, status, date)
                    self.donations.append(new_item)
                    db_add_donation(new_item)
                    messagebox.showinfo("Success", "Donation added! Thank you! 🎁")
                else:
                    new_item = Wish(name, item, qty, category, status, date)
                    self.wishes.append(new_item)
                    db_add_wish(new_item)
                    messagebox.showinfo("Success", "Wish added! ⭐")
            
            self.refresh_all() #Update the visible list/table
            dialog.destroy()

        #Save Button
        save_button_text = "Save Changes" if item_to_edit else ("Save Donation" if is_donation else "Save Wish")
        save_button_color = "#ADD8E6" if item_to_edit else ("#90EE90" if is_donation else "#FFE4B5")
        
        tk.Button(dialog, text=save_button_text, command=save, 
                 bg=save_button_color, font=("fixedsys", 10, "bold")).pack(pady=15)


    #CRUD Functions
    def add_donation(self):
        #Handler for ADD DONATION button
        self._show_dialog("Add Donation", is_donation=True)

    def add_wish(self):
        #Handler for ADD WISH button
        self._show_dialog("Add Wish", is_donation=False)

    def edit_donation(self):
        #Handler for EDIT SELECTED button on Donations tab
        selected = self.donation_tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a donation to edit.")
            return

        #Get the tag to find the index
        tags = self.donation_tree.item(selected[0])["tags"]
        if not tags:
            messagebox.showerror("Error", "Could not identify donation.")
            return
        
        donation_idx = int(tags[0].split("_")[1])
        donation_to_edit = self.donations[donation_idx]

        initial_data = {
            'name': donation_to_edit.donor,
            'item': donation_to_edit.item,
            'quantity': donation_to_edit.quantity,
            'category': donation_to_edit.category
        }
        self._show_dialog(
            "Edit Donation",
            initial_data=initial_data,
            is_donation=True,
            item_to_edit=donation_to_edit,
            original_keys=(donation_to_edit.donor, donation_to_edit.item, donation_to_edit.date),
        )

    def edit_wish(self):
        #Handler for EDIT SELECTED button on Wish List tab
        selected = self.wish_tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a wish to edit.")
            return

        tags = self.wish_tree.item(selected[0])["tags"]
        if not tags:
            messagebox.showerror("Error", "Could not identify wish.")
            return
        
        wish_idx = int(tags[0].split("_")[1])
        wish_to_edit = self.wishes[wish_idx]

        initial_data = {
            'name': wish_to_edit.recipient,
            'item': wish_to_edit.item,
            'quantity': wish_to_edit.quantity,
            'category': wish_to_edit.category
        }
        self._show_dialog(
            "Edit Wish",
            initial_data=initial_data,
            is_donation=False,
            item_to_edit=wish_to_edit,
            original_keys=(wish_to_edit.recipient, wish_to_edit.item, wish_to_edit.date),
        )


    def delete_donation(self):
        #Handler for DELETE SELECTED button on Donations tab.
        selected = self.donation_tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a donation.")
            return
            
        if messagebox.askyesno("Confirm", "Delete this donation?"):
            tags = self.donation_tree.item(selected[0])["tags"]
            if tags:
                donation_idx = int(tags[0].split("_")[1])
                removed = self.donations.pop(donation_idx)
                db_delete_donation(removed.donor, removed.item, removed.date)

            self.refresh_all()
            messagebox.showinfo("Success", "Donation deleted.")


    def delete_wish(self):
        #Handler for DELETE SELECTED button on Wish List tab
        selected = self.wish_tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a wish.")
            return
            
        if messagebox.askyesno("Confirm", "Delete this wish?"):
            tags = self.wish_tree.item(selected[0])["tags"]
            if tags:
                wish_idx = int(tags[0].split("_")[1])
                removed = self.wishes.pop(wish_idx)
                db_delete_wish(removed.recipient, removed.item, removed.date)

            self.refresh_all()
            messagebox.showinfo("Success", "Wish deleted.")

    #Core Logic 
    def auto_match(self):
        #Logic to match available donations with pending wishes

        matches = []
        
        #Filter for items that can be matched (quantity > 0 and correct status)
        donations_for_match = [d for d in self.donations if d.status == "Available" and d.quantity > 0]
        wishes_for_match = [w for w in self.wishes if w.status == "Pending" and w.quantity > 0]

        #Iteration and Matching
        for wish in wishes_for_match:
            for donation in donations_for_match:
                #Match if same Category AND same Item Name (case-insensitive)
                if (donation.category == wish.category and 
                    donation.item.lower() == wish.item.lower()):
                    
                    old_donation_key = (donation.donor, donation.item, donation.date)
                    old_wish_key = (wish.recipient, wish.item, wish.date)

                    #Determine the quantity to match (the lesser of available or needed)
                    qty_matched = min(donation.quantity, wish.quantity)
                    
                    if qty_matched > 0:
                        matches.append(f"✓ Matched: {donation.item} ({qty_matched}) from {donation.donor} → {wish.recipient}")
                        
                        #Update Donation object
                        donation.quantity -= qty_matched
                        if donation.quantity == 0:
                            donation.status = "Matched"
                        
                        #Update Wish object
                        wish.quantity -= qty_matched
                        if wish.quantity == 0:
                            wish.status = "Fulfilled"

                        #Keep database updated as matches occur
                        db_update_donation(*old_donation_key, donation)
                        db_update_wish(*old_wish_key, wish)

                        #Break the inner loop if the wish is now fully fulfilled
                        if wish.quantity == 0:
                            break

        #Display results
        self.match_text.delete(1.0, tk.END)
        if matches:
            self.match_text.insert(tk.END, " MATCHING RESULTS \n\n")
            self.match_text.insert(tk.END, "\n".join(matches))
            self.match_text.insert(tk.END, f"\n\n Total Matches: {len(matches)}")
            self.refresh_all()
            messagebox.showinfo("Success", f"Matched {len(matches)} items!")
        else:
            self.match_text.insert(tk.END, "No matches found.\nTry adding more donations or wishes!")

    def clear_matches(self):
        #Clears the output text area in the Matching tab
        self.match_text.delete(1.0, tk.END)

    def refresh_all(self):
        #Updates the Treeviews and stats labels to reflect current in-memory data
        
        #Refresh Donations Tab 
        for item in self.donation_tree.get_children():
            self.donation_tree.delete(item)
        
        total_donations = 0
        available_qty = 0
        for idx, d in enumerate(self.donations):
            #Insert object data into the Treeview row with index tag
            item_id = self.donation_tree.insert("", "end", values=(d.donor, d.item, d.quantity, 
                                                        d.category, d.status, d.date), tags=(f"donation_{idx}",))
            total_donations += 1
            if d.status == "Available" and d.quantity > 0:
                available_qty += d.quantity 

        #Update stats label
        self.donation_stats.config(text=f"TOTAL DONATIONS: {total_donations} | AVAILABLE: {available_qty}")

        #Refresh Wishes Tab
        for item in self.wish_tree.get_children():
            self.wish_tree.delete(item)
        
        total_wishes = 0
        pending_qty = 0
        for idx, w in enumerate(self.wishes):
            #Insert object data into the Treeview row with index tag
            item_id = self.wish_tree.insert("", "end", values=(w.recipient, w.item, w.quantity, 
                                                    w.category, w.status, w.date), tags=(f"wish_{idx}",))
            total_wishes += 1
            if w.status == "Pending" and w.quantity > 0:
                pending_qty += w.quantity 
        
        #Update stats label
        self.wish_stats.config(text=f"TOTAL WISH LIST: {total_wishes} | PENDING: {pending_qty}")


#RUN BLOCK

if __name__ == "__main__":
    root = tk.Tk()
    app = Merrymatch(root)
    root.mainloop()