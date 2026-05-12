import os
from datetime import datetime
from config import RECEIPTS_DIR, COMPANY_NAME, COMPANY_LOGO

class ReceiptGenerator:
    """Handles receipt generation and printing"""
    
    def __init__(self):
        self.ensure_receipts_directory()
    
    def ensure_receipts_directory(self):
        """Ensure receipts directory exists"""
        if not os.path.exists(RECEIPTS_DIR):
            os.makedirs(RECEIPTS_DIR)
    
    def generate_receipt(self, receipt_data):
        """Generate a receipt file for the purchase"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        receipt_filename = f"{RECEIPTS_DIR}receipt_{timestamp}.txt"
        
        with open(receipt_filename, 'w', encoding='utf-8') as f:
            # Header
            f.write(COMPANY_LOGO)
            f.write(f"\n{COMPANY_NAME}\n")
            f.write("="*60 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Receipt No: {timestamp}\n")
            f.write(f"Customer: {receipt_data['customer_name']}\n")
            if receipt_data.get('customer_email'):
                f.write(f"Email: {receipt_data['customer_email']}\n")
            f.write("="*60 + "\n\n")
            
            # Items
            f.write("ITEMS PURCHASED:\n")
            f.write("-"*60 + "\n")
            f.write(f"{'Item':<30} {'Qty':<6} {'Price':<10} {'Total':<10}\n")
            f.write("-"*60 + "\n")
            
            for item in receipt_data['items']:
                f.write(f"{item['name']:<30} {item['quantity']:<6} "
                       f"${item['price']:<9.2f} ${item['subtotal']:<9.2f}\n")
            
            # Totals
            f.write("-"*60 + "\n")
            f.write(f"{'Subtotal:':>50} ${receipt_data['subtotal']:.2f}\n")
            
            if receipt_data['discount'] > 0:
                f.write(f"{'Discount:':>50} -${receipt_data['discount']:.2f}\n")
            
            f.write(f"{'Tax:':>50} ${receipt_data['tax']:.2f}\n")
            f.write("="*60 + "\n")
            f.write(f"{'FINAL TOTAL:':>50} ${receipt_data['total']:.2f}\n")
            f.write("="*60 + "\n\n")
            
            # Footer
            f.write("Thank you for shopping with us!\n")
            f.write("We hope you enjoy your new dresses!\n")
            f.write("="*60 + "\n")
            f.write("Returns accepted within 30 days with original receipt\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        return receipt_filename
    
    def generate_bulk_receipt(self, receipts_data, filename="bulk_sales_report.txt"):
        """Generate a bulk sales report"""
        report_filename = f"{RECEIPTS_DIR}{filename}"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("BULK SALES REPORT\n")
            f.write("="*70 + "\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            total_sales = 0
            for i, receipt in enumerate(receipts_data, 1):
                f.write(f"Sale #{i}\n")
                f.write(f"  Customer: {receipt['customer_name']}\n")
                f.write(f"  Total: ${receipt['total']:.2f}\n")
                f.write(f"  Items: {len(receipt['items'])}\n\n")
                total_sales += receipt['total']
            
            f.write("="*70 + "\n")
            f.write(f"TOTAL SALES: ${total_sales:.2f}\n")
            f.write(f"NUMBER OF TRANSACTIONS: {len(receipts_data)}\n")
            f.write("="*70 + "\n")
        
        return report_filename
