from config import TAX_RATE, DISCOUNT_THRESHOLD, DISCOUNT_RATE
from receipt_generator import ReceiptGenerator

class ShoppingCart:
    """Manages shopping cart operations"""
    
    def __init__(self):
        self.cart_items = []
        self.receipt_gen = ReceiptGenerator()
    
    def add_to_cart(self, dress, quantity):
        """Add dress to shopping cart"""
        if quantity > dress['quantity']:
            print(f"❌ Only {dress['quantity']} items available!")
            return False
        
        # Check if item already in cart
        for item in self.cart_items:
            if item['id'] == dress['id']:
                item['quantity'] += quantity
                print(f"✅ Updated quantity for {dress['name']}: {item['quantity']}")
                return True
        
        # Add new item
        cart_item = {
            'id': dress['id'],
            'name': dress['name'],
            'price': dress['price'],
            'quantity': quantity,
            'subtotal': dress['price'] * quantity
        }
        self.cart_items.append(cart_item)
        print(f"✅ Added {quantity} x {dress['name']} to cart")
        return True
    
    def remove_from_cart(self, dress_id):
        """Remove item from cart"""
        for i, item in enumerate(self.cart_items):
            if item['id'] == dress_id:
                removed = self.cart_items.pop(i)
                print(f"✅ Removed {removed['name']} from cart")
                return True
        print(f"❌ Dress with ID {dress_id} not in cart!")
        return False
    
    def update_quantity(self, dress_id, new_quantity):
        """Update item quantity in cart"""
        for item in self.cart_items:
            if item['id'] == dress_id:
                if new_quantity <= 0:
                    return self.remove_from_cart(dress_id)
                item['quantity'] = new_quantity
                item['subtotal'] = item['price'] * new_quantity
                print(f"✅ Updated {item['name']} quantity to {new_quantity}")
                return True
        print(f"❌ Dress with ID {dress_id} not in cart!")
        return False
    
    def view_cart(self):
        """Display cart contents"""
        if not self.cart_items:
            print("\n🛒 Your cart is empty!")
            return
        
        print("\n" + "="*70)
        print("🛒 YOUR SHOPPING CART")
        print("="*70)
        print(f"{'ID':<6} {'Name':<22} {'Price':<8} {'Qty':<6} {'Subtotal':<10}")
        print("-"*70)
        
        total = 0
        for item in self.cart_items:
            print(f"{item['id']:<6} {item['name']:<22} ${item['price']:<7.2f} "
                  f"{item['quantity']:<6} ${item['subtotal']:<9.2f}")
            total += item['subtotal']
        
        print("-"*70)
        print(f"{'Subtotal:':>55} ${total:.2f}")
        
        # Calculate discount
        discount = 0
        if total >= DISCOUNT_THRESHOLD:
            discount = total * DISCOUNT_RATE
            print(f"{'Discount (10%):':>55} -${discount:.2f}")
        
        tax = (total - discount) * TAX_RATE
        print(f"{f'Tax ({TAX_RATE*100:.0f}%):':>55} ${tax:.2f}")
        
        final_total = total - discount + tax
        print("="*70)
        print(f"{'FINAL TOTAL:':>55} ${final_total:.2f}")
        print("="*70)
        
        return final_total
    
    def checkout(self, customer_name, customer_email=""):
        """Process checkout and generate receipt"""
        if not self.cart_items:
            print("❌ Cannot checkout: Cart is empty!")
            return False
        
        # Calculate totals
        subtotal = sum(item['subtotal'] for item in self.cart_items)
        discount = subtotal * DISCOUNT_RATE if subtotal >= DISCOUNT_THRESHOLD else 0
        tax = (subtotal - discount) * TAX_RATE
        total = subtotal - discount + tax
        
        # Generate receipt
        receipt_data = {
            'customer_name': customer_name,
            'customer_email': customer_email,
            'items': self.cart_items,
            'subtotal': subtotal,
            'discount': discount,
            'tax': tax,
            'total': total
        }
        
        receipt_file = self.receipt_gen.generate_receipt(receipt_data)
        
        # Clear cart after successful checkout
        self.cart_items = []
        print(f"\n✅ Checkout successful!")
        print(f"🧾 Receipt saved as: {receipt_file}")
        return True
    
    def clear_cart(self):
        """Clear all items from cart"""
        if self.cart_items:
            self.cart_items = []
            print("🛒 Cart cleared!")
        else:
            print("Cart is already empty!")
