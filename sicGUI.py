import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox

# Import our assembler modules
# Assuming the modules are in the src directory and can be imported directly
from src.instructions import instruction_size
from src.assembler_pass1 import pass1, symbol_table
from src.assembler_pass2 import pass2

class SICXEAssemblerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SIC/XE Assembler")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create a data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Set up the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.input_tab = ttk.Frame(self.notebook)
        self.symbol_tab = ttk.Frame(self.notebook)
        self.listing_tab = ttk.Frame(self.notebook)
        self.htme_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.input_tab, text="Assembly Code")
        self.notebook.add(self.symbol_tab, text="Symbol Table")
        self.notebook.add(self.listing_tab, text="Listing")
        self.notebook.add(self.htme_tab, text="HTME Records")
        
        # Setup the input tab
        self.setup_input_tab()
        
        # Setup the symbol table tab
        self.setup_symbol_tab()
        
        # Setup the listing tab
        self.setup_listing_tab()
        
        # Setup the HTME records tab
        self.setup_htme_tab()
        
        # Bottom frame for buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add buttons for operations
        self.create_buttons()
    
    def setup_input_tab(self):
        # Create a frame for the input area
        input_frame = ttk.Frame(self.input_tab)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label for the input
        ttk.Label(input_frame, text="SIC/XE Assembly Code:").pack(anchor=tk.W)
        
        # Create a text widget for entering assembly code
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=80, height=25)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Load existing data/in.txt if it exists
        try:
            with open('data/in.txt', 'r') as file:
                content = file.read()
                self.input_text.insert(tk.END, content)
        except FileNotFoundError:
            pass  # If file doesn't exist, do nothing

    
    def setup_symbol_tab(self):
        # Create a frame for the symbol table
        symbol_frame = ttk.Frame(self.symbol_tab)
        symbol_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label for the symbol table
        ttk.Label(symbol_frame, text="Symbol Table:").pack(anchor=tk.W)
        
        # Create a text widget for displaying the symbol table
        self.symbol_text = scrolledtext.ScrolledText(symbol_frame, wrap=tk.WORD, width=40, height=20)
        self.symbol_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.symbol_text.config(state=tk.DISABLED)
    
    def setup_listing_tab(self):
        # Create a frame for the listing
        listing_frame = ttk.Frame(self.listing_tab)
        listing_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label for the listing
        ttk.Label(listing_frame, text="Assembly Listing:").pack(anchor=tk.W)
        
        # Create a text widget for displaying the listing
        self.listing_text = scrolledtext.ScrolledText(listing_frame, wrap=tk.WORD, width=80, height=25)
        self.listing_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listing_text.config(state=tk.DISABLED)
    
    def setup_htme_tab(self):
        # Create a frame for the HTME records
        htme_frame = ttk.Frame(self.htme_tab)
        htme_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Label for the HTME records
        ttk.Label(htme_frame, text="HTME Records:").pack(anchor=tk.W)
        
        # Create a text widget for displaying the HTME records
        self.htme_text = scrolledtext.ScrolledText(htme_frame, wrap=tk.WORD, width=80, height=20)
        self.htme_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.htme_text.config(state=tk.DISABLED)
    
    def create_buttons(self):
        # Load button
        self.load_btn = ttk.Button(self.button_frame, text="Load File", command=self.load_file)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_btn = ttk.Button(self.button_frame, text="Save File", command=self.save_file)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Assemble button
        self.assemble_btn = ttk.Button(self.button_frame, text="Assemble", command=self.assemble)
        self.assemble_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_btn = ttk.Button(self.button_frame, text="Clear All", command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        self.exit_btn = ttk.Button(self.button_frame, text="Exit", command=self.root.quit)
        self.exit_btn.pack(side=tk.RIGHT, padx=5)
    
    def load_file(self):
        # Open file dialog
        file_path = filedialog.askopenfilename(
            filetypes=[("Assembly Files", "*.asm"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        # Check if file was selected
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
                messagebox.showinfo("Success", f"File loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def save_file(self):
        # Open file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".asm",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        # Check if file was selected
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    content = self.input_text.get(1.0, tk.END)
                    file.write(content)
                messagebox.showinfo("Success", f"File saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def assemble(self):
    # Get the current assembly code from the input text widget
        assembly_code = self.input_text.get(1.0, tk.END)

        try:
            # Save the current input to data/in.txt temporarily for the assembler to use
            with open('data/in.txt', 'w') as f:
                f.write(assembly_code)

            # Run pass 1 of the assembler
            pass1('data/in.txt')

            # Run pass 2 of the assembler
            pass2('data/intermediate.txt', 'data/out_pass1.txt', 'data/symbTable.txt')

            # Show success message
            messagebox.showinfo("Success", "Assembly completed successfully!")

            # Update the tabs with the results
            self.update_symbol_table()
            self.update_listing()
            self.update_htme_records()

            # Switch to the listing tab
            self.notebook.select(2)  # Index 2 is the listing tab

        except Exception as e:
            messagebox.showerror("Error", f"Assembly failed: {str(e)}")

    
    def update_symbol_table(self):
        # Read the symbol table file and update the symbol table tab
        try:
            with open('data/symbTable.txt', 'r') as f:
                content = f.read()
                
                # Enable text widget for editing
                self.symbol_text.config(state=tk.NORMAL)
                
                # Clear previous content
                self.symbol_text.delete(1.0, tk.END)
                
                # Insert new content
                self.symbol_text.insert(tk.END, "Symbol\tAddress\n")
                self.symbol_text.insert(tk.END, "-" * 20 + "\n")
                self.symbol_text.insert(tk.END, content)
                
                # Disable text widget for editing
                self.symbol_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load symbol table: {str(e)}")
    
    def update_listing(self):
        # Read the listing file and update the listing tab
        try:
            with open('data/listing.txt', 'r') as f:
                content = f.read()
                
                # Enable text widget for editing
                self.listing_text.config(state=tk.NORMAL)
                
                # Clear previous content
                self.listing_text.delete(1.0, tk.END)
                
                # Insert new content
                self.listing_text.insert(tk.END, content)
                
                # Disable text widget for editing
                self.listing_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load listing: {str(e)}")
    
    def update_htme_records(self):
        # Read the HTME file and update the HTME tab
        try:
            with open('data/HTME.txt', 'r') as f:
                content = f.read()
                
                # Enable text widget for editing
                self.htme_text.config(state=tk.NORMAL)
                
                # Clear previous content
                self.htme_text.delete(1.0, tk.END)
                
                # Insert new content
                self.htme_text.insert(tk.END, content)
                
                # Disable text widget for editing
                self.htme_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load HTME records: {str(e)}")
    
    def clear_all(self):
        # Clear all text widgets
        self.input_text.delete(1.0, tk.END)
        
        # Enable text widgets for editing
        self.symbol_text.config(state=tk.NORMAL)
        self.listing_text.config(state=tk.NORMAL)
        self.htme_text.config(state=tk.NORMAL)
        
        # Clear content
        self.symbol_text.delete(1.0, tk.END)
        self.listing_text.delete(1.0, tk.END)
        self.htme_text.delete(1.0, tk.END)
        
        # Disable text widgets for editing
        self.symbol_text.config(state=tk.DISABLED)
        self.listing_text.config(state=tk.DISABLED)
        self.htme_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = SICXEAssemblerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()