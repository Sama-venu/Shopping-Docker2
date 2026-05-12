from datetime import datetime
from file_handler import FileHandler
from config import CATEGORIES, SIZES

class DressManager:
    """Manages dress collection operations"""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.dresses = self.file_handler.load_dresses()
    
    def add_dress(self, dress_id, name, category, price, size, quantity, brand="", material=""):
        """Add a new dress to the collection"""
        # Validation
        if category not in CATEGORIES:
            print(f"❌ Invalid category. Choose from: {', '.join(CATEGORIES)}")
            return False
        
        if size not in SIZES:
            print(f"❌ Invalid size. Choose from: {', '.join(SIZES)}")
            return False
        
        dress = {
            "id": dress_id,
            "name": name,
            "category": category,
            "price": float(price),
            "size": size,
            "quantity": int(quantity),
            "brand": brand,
            "material": material,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rating": 0,
            "reviews": []
        }
        
        self.dresses.append(dress)
        self.file_handler.save_dresses(self.dresses)
        print(f"\n✅ {name} added successfully to collection!")
        return True
    
    def view_all_dresses(self):
        """Display all dresses in the collection"""
        if not self.dresses:
            print("\n📭 No dresses in the collection.")
            return
        
        print("\n" + "="*100)
        print(f"{'ID':<6} {'Name':<22} {'Category':<12} {'Price':<8} {'Size':<6} {'Qty':<6} {'Brand':<12}")
        print("="*100)
        for dress in self.dresses:
            print(f"{dress['id']:<6} {dress['name']:<22} {dress['category']:<12} "
                  f"${dress['price']:<7.2f} {dress['size']:<6} {dress['quantity']:<6} "
                  f"{dress.get('brand', 'N/A'):<12}")
        print("="*100)
        print(f"Total Dresses: {len(self.dresses)}")
    
    def search_dresses(self, keyword=""):
        """Search dresses by name or brand"""
        if not keyword:
            return self.dresses
        
        results = [d for d in self.dresses if 
                  keyword.lower() in d['name'].lower() or 
                  keyword.lower() in d.get('brand', '').lower()]
        return results
    
    def filter_by_category(self, category):
        """Filter dresses by category"""
        return [d for d in self.dresses if d['category'].lower() == category.lower()]
    
    def filter_by_size(self, size):
        """Filter dresses by size"""
        return [d for d in self.dresses if d['size'].upper() == size.upper()]
    
    def filter_by_price_range(self, min_price, max_price):
        """Filter dresses within price range"""
        return [d for d in self.dresses if min_price <= d['price'] <= max_price]
    
    def get_dress_by_id(self, dress_id):
        """Get a specific dress by ID"""
        for dress in self.dresses:
            if dress['id'] == dress_id:
                return dress
        return None
    
    def update_stock(self, dress_id, new_quantity):
        """Update stock quantity"""
        dress = self.get_dress_by_id(dress_id)
        if dress:
            old_qty = dress['quantity']
            dress['quantity'] = new_quantity
            self.file_handler.save_dresses(self.dresses)
            print(f"✅ Stock updated: {dress['name']} ({old_qty} → {new_quantity})")
            return True
        return False
    
    def update_price(self, dress_id, new_price):
        """Update dress price"""
        dress = self.get_dress_by_id(dress_id)
        if dress:
            old_price = dress['price']
            dress['price'] = new_price
            self.file_handler.save_dresses(self.dresses)
            print(f"✅ Price updated: {dress['name']} (${old_price:.2f} → ${new_price:.2f})")
            return True
        return False
    
    def remove_dress(self, dress_id):
        """Remove a dress from collection"""
        dress = self.get_dress_by_id(dress_id)
        if dress:
            self.dresses.remove(dress)
            self.file_handler.save_dresses(self.dresses)
            print(f"✅ {dress['name']} removed from collection!")
            return True
        print(f"❌ Dress with ID {dress_id} not found!")
        return False
    
    def get_low_stock_items(self, threshold=5):
        """Get items with low stock"""
        return [d for d in self.dresses if d['quantity'] <= threshold]
    
    def backup_current_data(self):
        """Create backup of current data"""
        return self.file_handler.backup_data(self.dresses)
    
    def restore_from_backup(self):
        """Restore data from backup"""
        restored = self.file_handler.restore_backup()
        if restored:
            self.dresses = restored
        return restored
