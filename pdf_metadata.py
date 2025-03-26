# pdf_metadata.py
# Requires: PyPDF2 (install with `pip install PyPDF2`)

import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

class PDFMetadataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edit Simple PDF Metadata")
        self.root.geometry("500x650")
        self.root.configure(bg="#000000") 

        try:
            icon = tk.PhotoImage(file="icon.png")
            self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Warning: Could not load icon - {e}")

        
        self.input_path = tk.StringVar()
        self.metadata_entries = {}

      
        self.label_style = {"bg": "#000000", "fg": "#BB86FC", "font": ("Arial", 12, "bold")} 
        self.entry_style = {"bg": "#1A1A1A", "fg": "#FFFFFF", "insertbackground": "#BB86FC", "font": ("Arial", 10), "borderwidth": 1, "relief": "solid"}
        self.button_style = {"bg": "#BB86FC", "fg": "#000000", "font": ("Arial", 11, "bold"), "activebackground": "#9B59D0", "relief": "flat", "borderwidth": 0}


        header = tk.Label(root, text="Edit Simple PDF Metadata", font=("Arial", 18, "bold"), bg="#000000", fg="#BB86FC")
        header.pack(pady=20)
        header.config(highlightbackground="#BB86FC", highlightcolor="#BB86FC", highlightthickness=1) 

        tk.Label(root, text="PDF File:", **self.label_style).pack()
        entry_input = tk.Entry(root, textvariable=self.input_path, width=40, **self.entry_style)
        entry_input.pack(pady=5)
        btn_input = tk.Button(root, text="Browse", command=self.select_input_file, **self.button_style, width=10)
        btn_input.pack(pady=5)
        btn_input.bind("<Enter>", lambda e: btn_input.config(bg="#9B59D0"))
        btn_input.bind("<Leave>", lambda e: btn_input.config(bg="#BB86FC"))


        btn_frame = tk.Frame(root, bg="#000000")
        btn_frame.pack(pady=15)
        btn_read = tk.Button(btn_frame, text="Load Metadata", command=self.read_metadata, **self.button_style, width=15)
        btn_read.grid(row=0, column=0, padx=10)
        btn_read.bind("<Enter>", lambda e: btn_read.config(bg="#9B59D0"))
        btn_read.bind("<Leave>", lambda e: btn_read.config(bg="#BB86FC"))

        btn_remove = tk.Button(btn_frame, text="Remove Metadata", command=self.remove_metadata, **self.button_style, width=15)
        btn_remove.grid(row=0, column=1, padx=10)
        btn_remove.bind("<Enter>", lambda e: btn_remove.config(bg="#9B59D0"))
        btn_remove.bind("<Leave>", lambda e: btn_remove.config(bg="#BB86FC"))

        self.metadata_frame = tk.Frame(root, bg="#000000")
        self.metadata_frame.pack(pady=10, fill="both", expand=True)


        self.save_btn = tk.Button(root, text="Save Changes", command=self.save_metadata, **self.button_style, width=15)
        self.save_btn.pack(pady=10)
        self.save_btn.bind("<Enter>", lambda e: self.save_btn.config(bg="#9B59D0"))
        self.save_btn.bind("<Leave>", lambda e: self.save_btn.config(bg="#BB86FC"))
        self.save_btn.pack_forget() 

    def select_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.input_path.set(file_path)

    def read_metadata(self):
        input_file = self.input_path.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid PDF file", parent=self.root)
            return

        try:
            pdf = PdfReader(input_file)
            metadata = pdf.metadata if pdf.metadata is not None else {}

            for widget in self.metadata_frame.winfo_children():
                widget.destroy()
            self.metadata_entries.clear()

            fields = [
                ('/Title', 'Title'),
                ('/Author', 'Author'),
                ('/Subject', 'Subject'),
                ('/Keywords', 'Keywords'),
                ('/Creator', 'Creator'),
                ('/Producer', 'Producer'),
                ('/CreationDate', 'Creation Date'),
                ('/ModDate', 'Modification Date'),
                ('/Trapped', 'Trapped'),
            ]

            for i, (key, display_name) in enumerate(fields):
                tk.Label(self.metadata_frame, text=f"{display_name}:", **self.label_style).grid(row=i, column=0, sticky="e", padx=5, pady=3)
                entry = tk.Entry(self.metadata_frame, width=40, **self.entry_style)
                entry.insert(0, metadata.get(key, ''))
                entry.grid(row=i, column=1, padx=5, pady=3)
                self.metadata_entries[key] = entry

            page_count = len(pdf.pages)
            tk.Label(self.metadata_frame, text="Page Count:", **self.label_style).grid(row=len(fields), column=0, sticky="e", padx=5, pady=3)
            tk.Label(self.metadata_frame, text=str(page_count), bg="#1A1A1A", fg="#FFFFFF", font=("Arial", 10), borderwidth=1, relief="solid").grid(row=len(fields), column=1, sticky="w", padx=5, pady=3)

            self.save_btn.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read metadata: {str(e)}", parent=self.root)

    def remove_metadata(self):
        input_file = self.input_path.get()

        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid PDF file", parent=self.root)
            return

        try:
            temp_file = input_file + ".tmp"
            pdf_reader = PdfReader(input_file)
            pdf_writer = PdfWriter()

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            pdf_writer.add_metadata({})

            with open(temp_file, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            os.replace(temp_file, input_file)

            messagebox.showinfo("Success", "Metadata removed from the file", parent=self.root)
            self.read_metadata_from_file(input_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove metadata: {str(e)}", parent=self.root)

    def save_metadata(self):
        input_file = self.input_path.get()

        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid PDF file", parent=self.root)
            return

        try:
            temp_file = input_file + ".tmp"
            pdf_reader = PdfReader(input_file)
            pdf_writer = PdfWriter()

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            new_metadata = {}
            for key, entry in self.metadata_entries.items():
                value = entry.get().strip()
                if value:
                    new_metadata[key] = value
            pdf_writer.add_metadata(new_metadata)

            with open(temp_file, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            os.replace(temp_file, input_file)

            messagebox.showinfo("Success", "Metadata changes saved to the file", parent=self.root)
            self.read_metadata_from_file(input_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save metadata: {str(e)}", parent=self.root)

    def read_metadata_from_file(self, file_path):
        try:
            pdf = PdfReader(file_path)
            metadata = pdf.metadata if pdf.metadata is not None else {}

            for widget in self.metadata_frame.winfo_children():
                widget.destroy()
            self.metadata_entries.clear()

            fields = [
                ('/Title', 'Title'),
                ('/Author', 'Author'),
                ('/Subject', 'Subject'),
                ('/Keywords', 'Keywords'),
                ('/Creator', 'Creator'),
                ('/Producer', 'Producer'),
                ('/CreationDate', 'Creation Date'),
                ('/ModDate', 'Modification Date'),
                ('/Trapped', 'Trapped'),
            ]

            for i, (key, display_name) in enumerate(fields):
                tk.Label(self.metadata_frame, text=f"{display_name}:", **self.label_style).grid(row=i, column=0, sticky="e", padx=5, pady=3)
                entry = tk.Entry(self.metadata_frame, width=40, **self.entry_style)
                entry.insert(0, metadata.get(key, ''))
                entry.grid(row=i, column=1, padx=5, pady=3)
                self.metadata_entries[key] = entry

            page_count = len(pdf.pages)
            tk.Label(self.metadata_frame, text="Page Count:", **self.label_style).grid(row=len(fields), column=0, sticky="e", padx=5, pady=3)
            tk.Label(self.metadata_frame, text=str(page_count), bg="#1A1A1A", fg="#FFFFFF", font=("Arial", 10), borderwidth=1, relief="solid").grid(row=len(fields), column=1, sticky="w", padx=5, pady=3)

            self.save_btn.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to verify metadata: {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMetadataApp(root)
    root.mainloop()