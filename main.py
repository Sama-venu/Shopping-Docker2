import sys
from dress_manager import DressManager
from shopping_cart import ShoppingCart
from config import COMPANY_LOGO, CATEGORIES, SIZES

def display_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("MAIN MENU")
    print("="*60)
    print("1. 👗 View All Dresses")
    print("2. 🔍 Search Dresses")
    print("3. 🛒 Shopping Cart")
    print("4. 📦 Manage Collection (Admin)")
    print("5. 💾 Backup & Export Data")
    print("6. ℹ️ About")
    print("7. 🚪 Exit")
    print("="*60)

def search_menu(manager):
    """Search and filter menu"""
    while True:
        print("\n" + "-"*40)
        print("🔍 SEARCH & FILTER OPTIONS")
        print("-"*40)
        print("1. Search by name/brand")
        print("2. Filter by category")
        print("3. Filter by size")
        print("4. Filter by price range")
        print("5. View low stock items")
        print("6. Back to main menu")
        print("-"*40)
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            keyword = input("Enter search keyword: ")
            results = manager.search_dresses(keyword)
            display_search_results(results, f"Search: '{keyword}'")
        
        elif choice == '2':
            print(f"Categories: {', '.join(CATEGORIES)}")
            category = input("Enter category: ")
            results = manager.filter_by_category(category)
            display_search_results(results, f"Category: {category}")
        
        elif choice == '3':
            print(f"Sizes: {', '.join(SIZES)}")
            size = input("Enter size: ")
            results = manager.filter_by_size(size)
            display_search_results(results, f"Size: {size}")
        
        elif choice == '4':
            try:
                min_price = float(input("Min price: $"))
                max_price = float(input("Max price: $"))
                results = manager.filter_by_price_range(min_price, max_price)
                display_search_results(results, f"Price: ${min_price} - ${max_price}")
            except ValueError:
                print("❌ Invalid price!")
        
        elif choice == '5':
            results = manager.get_low_stock_items()
            display_search_results(results, "LOW STOCK ITEMS")
        
        elif choice == '6':
            break
        
        else:
            print("❌ Invalid choice!")

def display_search_results(results, title):
    """Display search results"""
    if not results:
        print(f"\n❌ No results found for '{title}'")
        return
    
    print(f"\n📋 {title}")
    print("="*100)
    print(f"{'ID':<6} {'Name':<22} {'Category':<12} {'Price':<8} {'Size':<6} {'Stock':<6} {'Brand':<12}")
    print("="*100)
    for dress in results:
        print(f"{dress['id']:<6} {dress['name']:<22} {dress['category']:<12} "
              f"${dress['price']:<7.2f} {dress['size']:<6} {dress['quantity']:<6} "
              f"{dress.get('brand', 'N/A'):<12}")
    print("="*100)

def shopping_cart_menu(manager, cart):
    """Shopping cart operations menu"""
    while True:
        print("\n" + "-"*40)
        print("🛒 SHOPPING CART MENU")
        print("-"*40)
        print("1. Add dress to cart")
        print("2. View cart")
        print("3. Remove from cart")
        print("4. Update quantity")
        print("5. Checkout")
        print("6. Clear cart")
        print("7. Back to main menu")
        print("-"*40)
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            manager.view_all_dresses()
            dress_id = input("\nEnter dress ID to add: ")
            dress = manager.get_dress_by_id(dress_id)
            if dress:
                try:
                    quantity = int(input("Enter quantity: "))
                    cart.add_to_cart(dress, quantity)
                except ValueError:
                    print("❌ Invalid quantity!")
            else:
                print("❌ Dress not found!")
        
        elif choice == '2':
            cart.view_cart()
        
        elif choice == '3':
            cart.view_cart()
            dress_id = input("\nEnter dress ID to remove: ")
            cart.remove_from_cart(dress_id)
        
        elif choice == '4':
            cart.view_cart()
            dress_id = input("\nEnter dress ID to update: ")
            try:
                quantity = int(input("Enter new quantity: "))
                cart.update_quantity(dress_id, quantity)
            except ValueError:
                print("❌ Invalid quantity!")
        
        elif choice == '5':
            if cart.cart_items:
                name = input("Enter your name: ")
                email = input("Enter your email (optional): ")
                cart.checkout(name, email)
                # Update stock after purchase
                for item in cart.cart_items:
                    dress = manager.get_dress_by_id(item['id'])
                    if dress:
                        new_stock = dress['quantity'] - item['quantity']
                        manager.update_stock(item['id'], new_stock)
            else:
                print("❌ Cart is empty!")
        
        elif choice == '6':
            confirm = input("Clear entire cart? (y/n): ")
            if confirm.lower() == 'y':
                cart.clear_cart()
        
        elif choice == '7':
            break
        
        else:
            print("❌ Invalid choice!")

def admin_menu(manager):
    """Admin menu for managing collection"""
    password = input("Enter admin password: ")
    if password != "admin123":  # Simple password protection
        print("❌ Access denied!")
        return
    
    while True:
        print("\n" + "-"*40)
        print("📦 ADMIN MENU")
        print("-"*40)
        print("1. Add new dress")
        print("2. Update stock")
        print("3. Update price")
        print("4. Remove dress")
        print("5. View all dresses")
        print("6. Back to main menu")
        print("-"*40)
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            print("\n➕ ADD NEW DRESS")
            dress_id = input("Dress ID: ")
            name = input("Dress name: ")
            print(f"Categories: {', '.join(CATEGORIES)}")
            category = input("Category: ")
            try:
                price = float(input("Price: $"))
                print(f"Sizes: {', '.join(SIZES)}")
                size = input("Size: ")
                quantity = int(input("Quantity: "))
                brand = input("Brand (optional): ")
                material = input("Material (optional): ")
                manager.add_dress(dress_id, name, category, price, size, quantity, brand, material)
            except ValueError:
                print("❌ Invalid price or quantity!")
        
        elif choice == '2':
            manager.view_all_dresses()
            dress_id = input("\nDress ID to update: ")
            try:
                new_quantity = int(input("New quantity: "))
                manager.update_stock(dress_id, new_quantity)
            except ValueError:
                print("❌ Invalid quantity!")
        
        elif choice == '3':
            manager.view_all_dresses()
            dress_id = input("\nDress ID to update price: ")
            try:
                new_price = float(input("New price: $"))
                manager.update_price(dress_id, new_price)
            except ValueError:
                print("❌ Invalid price!")
        
        elif choice == '4':
            manager.view_all_dresses()
            dress_id = input("\nDress ID to remove: ")
            confirm = input(f"Remove dress {dress_id}? (y/n): ")
            if confirm.lower() == 'y':
                manager.remove_dress(dress_id)
        
        elif choice == '5':
            manager.view_all_dresses()
        
        elif choice == '6':
            break
        
        else:
            print("❌ Invalid choice!")

def backup_menu(manager):
    """Backup and export menu"""
    while True:
        print("\n" + "-"*40)
        print("💾 BACKUP & EXPORT MENU")
        print("-"*40)
        print("1. Backup current data")
        print("2. Restore from backup")
        print("3. Export to CSV")
        print("4. Back to main menu")
        print("-"*40)
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            manager.backup_current_data()
        
        elif choice == '2':
            confirm = input("Restore from backup? Current data will be lost! (y/n): ")
            if confirm.lower() == 'y':
                manager.restore_from_backup()
        
        elif choice == '3':
            filename = input("Export filename (default: dress_export.csv): ")
            if not filename:
                filename = "dress_export.csv"
            manager.file_handler.export_to_csv(manager.dresses, filename)
        
        elif choice == '4':
            break
        
        else:
            print("❌ Invalid choice!")

def main():
    print(COMPANY_LOGO)
    print("Welcome to FashionHub Dress Collection Shopping System!")
    print("Your one-stop destination for elegant dresses\n")
    
    manager = DressManager()
    cart = ShoppingCart()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            manager.view_all_dresses()
        
        elif choice == '2':
            search_menu(manager)
        
        elif choice == '3':
            shopping_cart_menu(manager, cart)
        
        elif choice == '4':
            admin_menu(manager)
        
        elif choice == '5':
            backup_menu(manager)
        
        elif choice == '6':
            print("\n" + "="*60)
            print("FASHIONHUB DRESS COLLECTION SHOPPING SYSTEM")
            print("Version 2.0")
            print("Created with ❤️ for dress lovers")
            print("="*60)
        
        elif choice == '7':
            print("\n👋 Thank you for shopping at FashionHub!")
            print("We hope to see you again soon!")
            print("Data saved successfully.\n")
            sys.exit(0)
        
        else:
            print("❌ Invalid choice! Please enter 1-7.")

if __name__ == "__main__":
    main()
