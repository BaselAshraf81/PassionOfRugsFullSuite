#!/usr/bin/env python3
"""
TrestleIQ Bulk Processor GUI - MODE 1
Process Excel datasets with progress tracking and caching
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from lead_processor_v2 import LeadProcessor
import os


class BulkProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TrestleIQ Bulk Processor")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Data
        self.input_file = None
        self.output_file = None
        self.api_key = None
        self.max_rows = None
        self.processing = False
        
        # Colors
        self.colors = {
            'bg': '#F5F7FA',
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'light': '#ECF0F1',
            'white': '#FFFFFF'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Setup UI
        self.create_ui()
    
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title = tk.Label(
            main,
            text="TrestleIQ Bulk Processor",
            font=('Arial', 22, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        )
        title.pack(pady=(0, 20))
        
        # Configuration frame
        config_frame = tk.LabelFrame(
            main,
            text="Configuration",
            font=('Arial', 12, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            relief=tk.RAISED,
            bd=2
        )
        config_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        # Grid configuration
        config_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # API Key
        tk.Label(config_frame, text="TrestleIQ API Key:", font=('Arial', 11, 'bold'), 
                bg=self.colors['white']).grid(row=row, column=0, sticky='e', padx=20, pady=15)
        self.api_key_entry = tk.Entry(config_frame, font=('Arial', 10), width=50)
        self.api_key_entry.grid(row=row, column=1, sticky='ew', padx=20, pady=15)
        row += 1
        
        # Input file
        tk.Label(config_frame, text="Input Excel File:", font=('Arial', 11, 'bold'), 
                bg=self.colors['white']).grid(row=row, column=0, sticky='e', padx=20, pady=15)
        
        input_frame = tk.Frame(config_frame, bg=self.colors['white'])
        input_frame.grid(row=row, column=1, sticky='ew', padx=20, pady=15)
        
        self.input_label = tk.Label(input_frame, text="No file selected", font=('Arial', 10), 
                                    bg=self.colors['white'], fg='gray')
        self.input_label.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            input_frame,
            text="Browse...",
            command=self.browse_input,
            font=('Arial', 10),
            bg=self.colors['light'],
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        row += 1
        
        # Output file name
        tk.Label(config_frame, text="Output File Name:", font=('Arial', 11, 'bold'), 
                bg=self.colors['white']).grid(row=row, column=0, sticky='e', padx=20, pady=15)
        self.output_entry = tk.Entry(config_frame, font=('Arial', 10), width=50)
        self.output_entry.insert(0, "processed_leads.xlsx")
        self.output_entry.grid(row=row, column=1, sticky='ew', padx=20, pady=15)
        row += 1
        
        # Max rows
        tk.Label(config_frame, text="Max Rows to Process:", font=('Arial', 11, 'bold'), 
                bg=self.colors['white']).grid(row=row, column=0, sticky='e', padx=20, pady=15)
        
        max_frame = tk.Frame(config_frame, bg=self.colors['white'])
        max_frame.grid(row=row, column=1, sticky='w', padx=20, pady=15)
        
        self.max_rows_entry = tk.Entry(max_frame, font=('Arial', 10), width=15)
        self.max_rows_entry.pack(side=tk.LEFT)
        
        tk.Label(max_frame, text="(leave empty for all rows)", font=('Arial', 9), 
                bg=self.colors['white'], fg='gray').pack(side=tk.LEFT, padx=10)
        
        # Try to load API key from config
        try:
            from config import API_KEY
            self.api_key_entry.insert(0, API_KEY)
        except:
            pass
        
        # Progress frame
        progress_frame = tk.LabelFrame(
            main,
            text="Processing Progress",
            font=('Arial', 12, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            relief=tk.RAISED,
            bd=2
        )
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to process",
            font=('Arial', 11),
            bg=self.colors['white'],
            fg=self.colors['primary'],
            anchor='w'
        )
        self.status_label.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)
        
        # Progress text
        self.progress_label = tk.Label(
            progress_frame,
            text="",
            font=('Arial', 10),
            bg=self.colors['white'],
            fg=self.colors['secondary']
        )
        self.progress_label.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        # Results text area
        result_frame = tk.Frame(progress_frame, bg=self.colors['white'])
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(
            result_frame,
            height=10,
            font=('Courier', 9),
            bg='#F8F9FA',
            fg=self.colors['primary'],
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        # Buttons frame
        button_frame = tk.Frame(main, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start Processing",
            command=self.start_processing,
            font=('Arial', 13, 'bold'),
            bg=self.colors['success'],
            fg='white',
            padx=40,
            pady=12,
            cursor='hand2'
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_processing,
            font=('Arial', 13, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            padx=40,
            pady=12,
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
    
    def browse_input(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select Input Excel File",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.input_file = filename
            self.input_label.config(text=os.path.basename(filename), fg='black')
    
    def log(self, message):
        """Add message to result text"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def update_progress(self, current, total):
        """Update progress bar"""
        percentage = (current / total) * 100
        self.progress_bar['value'] = percentage
        self.progress_label.config(text=f"Processing row {current} of {total} ({percentage:.1f}%)")
        self.root.update()
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update()
    
    def start_processing(self):
        """Start processing in background thread"""
        # Validate inputs
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter TrestleIQ API Key")
            return
        
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input Excel file")
            return
        
        output_name = self.output_entry.get().strip()
        if not output_name:
            messagebox.showerror("Error", "Please enter an output file name")
            return
        
        # Create output path
        input_dir = os.path.dirname(self.input_file)
        self.output_file = os.path.join(input_dir, output_name)
        if not self.output_file.endswith('.xlsx'):
            self.output_file += '.xlsx'
        
        # Get max rows
        max_rows_str = self.max_rows_entry.get().strip()
        self.max_rows = None
        if max_rows_str:
            try:
                self.max_rows = int(max_rows_str)
            except ValueError:
                messagebox.showerror("Error", "Max rows must be a number")
                return
        
        # Disable start button, enable stop
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.processing = True
        
        # Clear results
        self.result_text.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        self.progress_label.config(text="")
        
        # Start processing in thread
        self.api_key = api_key
        thread = threading.Thread(target=self.process_worker, daemon=True)
        thread.start()
    
    def process_worker(self):
        """Worker thread for processing"""
        try:
            self.log("=" * 60)
            self.log("TrestleIQ Bulk Processor")
            self.log("=" * 60)
            self.log(f"Input file: {os.path.basename(self.input_file)}")
            self.log(f"Output file: {os.path.basename(self.output_file)}")
            if self.max_rows:
                self.log(f"Max rows: {self.max_rows}")
            else:
                self.log("Processing: All rows")
            self.log("")
            
            # Check if output file exists (caching)
            if os.path.exists(self.output_file):
                self.log("✓ Output file exists - will use caching for existing records")
                self.log("")
            
            # Create processor
            processor = LeadProcessor(self.api_key)
            
            # Process with callbacks
            total_results, cached_count, api_count = processor.process_excel_file_bulk(
                self.input_file,
                self.output_file,
                self.max_rows,
                progress_callback=self.update_progress,
                status_callback=self.update_status
            )
            
            # Success
            self.root.after(0, lambda: self.log(""))
            self.root.after(0, lambda: self.log("=" * 60))
            self.root.after(0, lambda: self.log("✓ Processing Complete!"))
            self.root.after(0, lambda: self.log("=" * 60))
            self.root.after(0, lambda: self.log(f"Total results: {total_results}"))
            self.root.after(0, lambda: self.log(f"Cached records: {cached_count}"))
            self.root.after(0, lambda: self.log(f"API calls made: {api_count}"))
            self.root.after(0, lambda: self.log(f"Output saved to: {os.path.basename(self.output_file)}"))
            self.root.after(0, lambda: self.log(""))
            self.root.after(0, lambda: self.log("Features:"))
            self.root.after(0, lambda: self.log("  • RED rows: Address lookup failed"))
            self.root.after(0, lambda: self.log("  • GREEN rows: Last name matches"))
            self.root.after(0, lambda: self.log("  • Dropdown lists for phones and addresses"))
            self.root.after(0, lambda: self.log("  • Status dropdown in last column"))
            
            self.root.after(0, lambda: self.update_status("Processing complete!"))
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                f"Processing complete!\n\nTotal results: {total_results}\nCached: {cached_count}\nAPI calls: {api_count}\n\nOutput saved to:\n{self.output_file}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"\n✗ Error: {str(e)}"))
            self.root.after(0, lambda: self.update_status("Error occurred"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed:\n{str(e)}"))
        
        finally:
            self.processing = False
            self.root.after(0, lambda: self.start_btn.config(state='normal'))
            self.root.after(0, lambda: self.stop_btn.config(state='disabled'))
    
    def stop_processing(self):
        """Stop processing"""
        self.processing = False
        self.log("\n⚠ Stopping... (current row will complete)")
        self.update_status("Stopping...")


def main():
    root = tk.Tk()
    app = BulkProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
