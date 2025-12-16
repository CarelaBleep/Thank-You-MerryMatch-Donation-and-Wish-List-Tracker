# data_manager.py for SQL
import sqlite3
import os
from donation import Donation
from wish import Wish

DATABASE_FILE = "merry_match.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  #Access columns by name
    return conn

def init_database():
    #If database exists but is corrupted, delete it
    if os.path.exists(DATABASE_FILE):
        try:
            # Test if database is readable
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            conn.close()
        except sqlite3.DatabaseError as e:
            print(f"Database corrupted, recreating: {e}")
            conn.close()
            os.remove(DATABASE_FILE)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    #Create donations table (only if it doesn't exist)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor TEXT NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available',
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    #Create wishes table (only if it doesn't exist)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    #Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_donations_status ON donations(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_donations_category ON donations(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_wishes_status ON wishes(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_wishes_category ON wishes(category)")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def load_donations():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT donor, item, quantity, category, status, date 
            FROM donations 
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [Donation(
            row['donor'],
            row['item'],
            row['quantity'],
            row['category'],
            row['status'],
            row['date']
        ) for row in rows]
    except Exception as e:
        print(f"Error loading donations: {e}")
        return []

def save_donations(donations):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        #Clear existing donations
        cursor.execute("DELETE FROM donations")
        
        #Insert all donations
        for d in donations:
            cursor.execute("""
                INSERT INTO donations (donor, item, quantity, category, status, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (d.donor, d.item, d.quantity, d.category, d.status, d.date))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving donations: {e}")

def add_donation(donation):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO donations (donor, item, quantity, category, status, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (donation.donor, donation.item, donation.quantity, 
              donation.category, donation.status, donation.date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding donation: {e}")
        return False

def delete_donation(donor, item, date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM donations 
            WHERE donor = ? AND item = ? AND date = ?
        """, (donor, item, date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting donation: {e}")
        return False

def update_donation(original_donor, original_item, original_date, donation):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE donations
            SET donor = ?, item = ?, quantity = ?, category = ?, status = ?, date = ?
            WHERE donor = ? AND item = ? AND date = ?
        """, (
            donation.donor,
            donation.item,
            donation.quantity,
            donation.category,
            donation.status,
            donation.date,
            original_donor,
            original_item,
            original_date
        ))
        conn.commit()
        updated = cursor.rowcount
        conn.close()
        return updated > 0
    except Exception as e:
        print(f"Error updating donation: {e}")
        return False

def load_wishes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT recipient, item, quantity, category, status, date 
            FROM wishes 
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [Wish(
            row['recipient'],
            row['item'],
            row['quantity'],
            row['category'],
            row['status'],
            row['date']
        ) for row in rows]
    except Exception as e:
        print(f"Error loading wishes: {e}")
        return []

def save_wishes(wishes):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Clear existing wishes
        cursor.execute("DELETE FROM wishes")
        
        # Insert all wishes
        for w in wishes:
            cursor.execute("""
                INSERT INTO wishes (recipient, item, quantity, category, status, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (w.recipient, w.item, w.quantity, w.category, w.status, w.date))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving wishes: {e}")

def add_wish(wish):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO wishes (recipient, item, quantity, category, status, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (wish.recipient, wish.item, wish.quantity, 
              wish.category, wish.status, wish.date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding wish: {e}")
        return False

def delete_wish(recipient, item, date):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM wishes 
            WHERE recipient = ? AND item = ? AND date = ?
        """, (recipient, item, date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting wish: {e}")
        return False

def update_wish(original_recipient, original_item, original_date, wish):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE wishes
            SET recipient = ?, item = ?, quantity = ?, category = ?, status = ?, date = ?
            WHERE recipient = ? AND item = ? AND date = ?
        """, (
            wish.recipient,
            wish.item,
            wish.quantity,
            wish.category,
            wish.status,
            wish.date,
            original_recipient,
            original_item,
            original_date
        ))
        conn.commit()
        updated = cursor.rowcount
        conn.close()
        return updated > 0
    except Exception as e:
        print(f"Error updating wish: {e}")
        return False

#Initialize database on module import

init_database()