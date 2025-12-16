# MerryMatch - Donation & Wish List Tracker

A festive desktop application for managing charitable donations and matching them with wish lists. Built with Python and Tkinter, MerryMatch helps connect donors with recipients to spread joy and support SDG 1: No Poverty.

## Features

- **Donation Management**: Add, edit, and delete donation entries with detailed tracking
- **Wish List Management**: Track recipient wishes and needs
- **Smart Matching**: Automatically match available donations with pending wishes based on category and item name
- **Persistent Storage**: SQLite database ensures all data is saved between sessions
- **Real-time Statistics**: View available donations and pending wishes at a glance
- **User-friendly Interface**: Clean, colorful GUI with intuitive navigation

## Getting Started

### Prerequisites

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)
- sqlite3 (included in Python standard library)

### Installation

1. Clone or download this repository
2. Ensure all required files are in the same directory:
   - `Merrymatch.py` (main application)
   - `donation.py` (Donation class)
   - `wish.py` (Wish class)
   - `data_manager.py` (database operations)

3. Run the application:
```bash
python Merrymatch.py
```

## How to Use

### Adding Donations

1. Navigate to the **Donations** tab
2. Click **ADD DONATION**
3. Fill in the donor name, item, quantity, and category
4. Click **Save Donation**

### Adding Wishes

1. Navigate to the **Wish List** tab
2. Click **ADD WISH**
3. Fill in the recipient name, item needed, quantity, and category
4. Click **Save Wish**

### Editing Entries

1. Select an entry from the table
2. Click **EDIT SELECTED**
3. Modify the fields as needed
4. Click **Save Changes**

### Deleting Entries

1. Select an entry from the table
2. Click **DELETE SELECTED**
3. Confirm the deletion

### Matching Donations with Wishes

1. Navigate to the **Wishy Matchy** tab
2. Click **AUTO MATCH GIFTS**
3. The system will automatically match donations with wishes based on:
   - Same category
   - Same item name (case-insensitive)
   - Available quantity
4. View the matching results in the text area
5. Click **Clear Matches** to clear the results display

## Project Structure

```
MerryMatch/
│
├── Merrymatch.py          # Main application with GUI
├── donation.py            # Donation class definition
├── wish.py               # Wish class definition
├── data_manager.py       # Database operations
└── merry_match.db        # SQLite database (auto-created)
```

## Data Storage

- All data is stored in `merry_match.db` SQLite database
- Database is automatically created on first run
- Data is saved when you close the application
- Corrupted databases are automatically recreated

## Categories

The application supports the following categories:
- Toys
- Clothes
- Food
- Books
- Electronics
- Other

## Status Values

**Donations:**
- `Available` - Ready to be matched
- `Matched` - Fully allocated to wishes

**Wishes:**
- `Pending` - Awaiting fulfillment
- `Fulfilled` - All items received

## Technical Details

- **GUI Framework**: Tkinter
- **Database**: SQLite3
- **Python Version**: 3.6+
- **Architecture**: Object-Oriented Programming (OOP)

## Contributing

This is an educational project supporting SDG 1: No Poverty. Feel free to fork and adapt it for your own charitable initiatives!

## License

This project is open source and available for educational and charitable purposes.

## SDG Alignment

This application supports **SDG 1: No Poverty** by facilitating the efficient matching of charitable donations with those in need, helping to reduce poverty and provide essential resources to underserved communities.

---
