import json
import os
import shutil
from datetime import datetime
from config import DRESSES_FILE, BACKUP_FILE

class FileHandler:
    """Handles all file operations for the dress shopping system"""
    
    def __init__(self):
        self.create_data_directories()
    
    def create_data_directories(self):
        """Create necessary directories if they don't exist"""
        directories = ["data", "data/receipts"]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"📁 Created directory: {directory}")
    
    def save_dresses(self, dresses):
        """Save dresses data to JSON file"""
        try:
            with open(DRESSES_FILE, 'w') as file:
                json.dump(dresses, file, indent=4)
            return True
        except Exception as e:
            print(f"❌ Error saving dresses: {e}")
            return False
    
    def load_dresses(self):
        """Load dresses data from JSON file"""
        if os.path.exists(DRESSES_FILE):
            try:
                with open(DRESSES_FILE, 'r') as file:
                    dresses = json.load(file)
                return dresses
            except Exception as e:
                print(f"❌ Error loading dresses: {e}")
                return []
        else:
            print("📝 No existing data file found. Starting fresh.")
            return []
    
    def backup_data(self, dresses):
        """Create backup of current data"""
        try:
            with open(BACKUP_FILE, 'w') as file:
                json.dump(dresses, file, indent=4)
            print(f"✅ Backup saved to {BACKUP_FILE}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def restore_backup(self):
        """Restore data from backup file"""
        if os.path.exists(BACKUP_FILE):
            try:
                with open(BACKUP_FILE, 'r') as file:
                    dresses = json.load(file)
                self.save_dresses(dresses)
                print("✅ Data restored from backup!")
                return dresses
            except Exception as e:
                print(f"❌ Restore failed: {e}")
                return None
        else:
            print("❌ No backup file found!")
            return None
    
    def export_to_csv(self, dresses, filename="dress_export.csv"):
        """Export dress data to CSV file"""
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if dresses:
                    fieldnames = dresses[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(dresses)
            print(f"✅ Data exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
