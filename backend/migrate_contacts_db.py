#!/usr/bin/env python3
"""
Migration script to add Department and Sector columns to contacts.db
Run this script to update existing contacts database with new columns
"""

import sqlite3
import os
import sys

def migrate_contacts_db(db_path):
    """Add Departament, Sektor, and Email columns to contacts table if they don't exist"""
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get current table schema
        cursor.execute("PRAGMA table_info(contacts)")
        columns = {row[1] for row in cursor.fetchall()}  # Get column names
        
        print(f"Current columns in contacts table: {', '.join(sorted(columns))}")
        
        # Add missing columns
        columns_to_add = {
            'Departament': 'TEXT',
            'Sektor': 'TEXT',
            'Email': 'TEXT'
        }
        
        # Also handle Mail -> Email migration
        if 'Mail' in columns and 'Email' not in columns:
            print("Migrating Mail column to Email...")
            cursor.execute("ALTER TABLE contacts RENAME COLUMN Mail TO Email")
            columns.add('Email')
            columns.discard('Mail')
            conn.commit()
        
        for col_name, col_type in columns_to_add.items():
            if col_name not in columns:
                print(f"Adding column: {col_name} ({col_type})")
                cursor.execute(f"ALTER TABLE contacts ADD COLUMN {col_name} {col_type}")
                columns.add(col_name)
                conn.commit()
        
        print("\n✅ Migration completed successfully!")
        print(f"Updated columns: {', '.join(sorted(columns))}")
        
        # Display sample data
        cursor.execute("SELECT COUNT(*) FROM contacts")
        count = cursor.fetchone()[0]
        print(f"\nTotal contacts in database: {count}")
        
        if count > 0:
            cursor.execute("SELECT Ad, Soyad, Vəzifə, Departament, Sektor, Email FROM contacts LIMIT 3")
            print("\nSample contacts:")
            for row in cursor.fetchall():
                print(f"  - {row[0]} {row[1]}: {row[2]}, Dept: {row[3] or 'N/A'}, Sector: {row[4] or 'N/A'}, Email: {row[5] or 'N/A'}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error during migration: {e}")
        return False

if __name__ == "__main__":
    # Try multiple possible database locations
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'contacts.db'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'contacts.db'),
        '/tmp/contacts.db'
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("Could not find contacts.db in these locations:")
        for p in possible_paths:
            print(f"  - {p}")
        sys.exit(1)
    
    print(f"Using database: {db_path}\n")
    success = migrate_contacts_db(db_path)
    sys.exit(0 if success else 1)
