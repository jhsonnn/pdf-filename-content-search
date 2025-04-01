import os
import pdfplumber
import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import ctypes.wintypes
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import psutil
import subprocess

SEARCH_FOLDER = r"C:\Users\YourUserName\Desktop"  # Root folder path
TARGET_FOLDERS = ['1', '2'] # Subfolders to search
EVERYTHING_PATH = r"C:\Program Files\Everything\Everything.exe" # The file path to Everything.exe exists
NUM_WORKERS = 8

EVERYTHING_OK = 0
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
MAX_RESULTS = 10000

everything = ctypes.WinDLL("./Everything64.dll")
everything.Everything_SetSearchW.argtypes = [ctypes.c_wchar_p]
everything.Everything_QueryW.argtypes = [ctypes.c_int]
everything.Everything_GetNumResults.restype = ctypes.c_int
everything.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
everything.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p
everything.Everything_GetResultPathW.argtypes = [ctypes.c_int]
everything.Everything_GetResultPathW.restype = ctypes.c_wchar_p

def ensure_everything_running():
    # Check currently running processes
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'everything.exe' in proc.info['name'].lower():
            print("Everything already running.")
            return  # Exit if already running

    # Launch in the background if not running
    try:
        print("Launching Everything in the background...")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # Hide window
        subprocess.Popen(
            [EVERYTHING_PATH, "-startup"],
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
            startupinfo=startupinfo,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Everything launched successfully.")
    except FileNotFoundError:
        print(f"Error: Could not find Everything.exe at {EVERYTHING_PATH}. Please check the path.")
    except Exception as e:
        print(f"Failed to launch Everything: {e}")

# PDF content search
def check_pdf_file(filepath, content_keywords):
    try:
        with pdfplumber.open(filepath) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    content = (text + os.path.basename(filepath)).lower()
                    if any(kw in content for kw in content_keywords):
                        excerpt = get_excerpt(text, content_keywords)
                        return os.path.basename(filepath), filepath, page_num, excerpt
    except Exception as e:
        print(f"Failed to open PDF: {filepath} → {e}")
    return None

def get_excerpt(text, keywords):
    lower_text = text.lower()
    for kw in keywords:
        if kw in lower_text:
            idx = lower_text.find(kw)
            return text[max(0, idx - 20):idx + 50].replace("\n", " ")
    return "..."

def run_pdf_search(content_keywords):
    update_status("Searching PDF content...")
    all_pdf_files = []
    for folder in TARGET_FOLDERS:
        full_path = os.path.join(SEARCH_FOLDER, folder)
        if os.path.exists(full_path):
            for root_dir, _, files in os.walk(full_path):
                for file in files:
                    if file.lower().endswith(".pdf"):
                        all_pdf_files.append(os.path.join(root_dir, file))

    results = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(check_pdf_file, f, content_keywords) for f in all_pdf_files]
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    def update_ui():
        pdf_table.delete(*pdf_table.get_children())
        for filename, filepath, page_num, excerpt in results:
            pdf_table.insert("", "end", values=(filename, filepath, page_num, excerpt))
        pdf_count_label.config(text=f"({len(results)} results)")
        update_status("PDF content search completed.")

    root.after(0, update_ui)

def everything_search(keyword):
    ensure_everything_running()

    # Generate search query

    search_query = f'path:"{os.path.join(SEARCH_FOLDER, "1")}" | path:"{os.path.join(SEARCH_FOLDER, "2")}" {keyword}'
    print(f"Executing search query: {search_query}")
    everything.Everything_SetSearchW(search_query)
    everything.Everything_QueryW(1)

    # Retrieve the number of search results
    num_results = everything.Everything_GetNumResults()
    print(f"Number of results: {num_results}")

    # Process search results
    results = [
        (
            everything.Everything_GetResultFileNameW(i), 
            os.path.join(everything.Everything_GetResultPathW(i), everything.Everything_GetResultFileNameW(i))
        )
        for i in range(min(num_results, MAX_RESULTS))
    ]

    # Remove duplicates
    unique_results = list(set(results))
    print(f"Unique Results: {unique_results}")
    return unique_results

def run_filename_search(filename_keywords):
    update_status("Searching filenames...")
    results = []

    # Perform search for each keyword
    for keyword in filename_keywords:
        results.extend(everything_search(keyword))

    # Remove duplicates
    unique_results = list(set(results))

    def update_ui():
        filename_table.delete(*filename_table.get_children())
        for file, path in unique_results:
            filename_table.insert("", "end", values=(file, path))
        filename_count_label.config(text=f"({len(unique_results)} results)")
        update_status("Filename search completed.")

    root.after(0, update_ui)

def search_pdf_content():
    content_input = entry_content.get().strip()
    content_keywords = [kw.strip().lower() for kw in content_input.split(',') if kw.strip()]
    if content_keywords:
        threading.Thread(target=run_pdf_search, args=(content_keywords,), daemon=True).start()
    else:
        messagebox.showwarning("Input required", "Please enter PDF content keywords.")

def search_filename():
    filename_input = entry_filename.get().strip()
    filename_keywords = [kw.strip().lower() for kw in filename_input.split(',') if kw.strip()]
    if filename_keywords:
        threading.Thread(target=run_filename_search, args=(filename_keywords,), daemon=True).start()
    else:
        messagebox.showwarning("Input required", "Please enter filename keywords.")

def clear_content_field():
    entry_content.delete(0, tk.END)

def clear_filename_field():
    entry_filename.delete(0, tk.END)

def update_status(message):
    status_label.config(text=message)


# Main entry point
if __name__ == "__main__":
    # Ensure Everything.exe is running before starting the GUI
    ensure_everything_running()

# GUI setup
root = tk.Tk()
root.title("PDF Text and Filename Search Tool")
root.geometry("1000x800")

search_frame = tk.Frame(root)
search_frame.pack(padx=10, pady=10, anchor="w")

# Filename search
tk.Label(search_frame, text="📁 Filename Keywords").grid(row=0, column=0, sticky="w")
entry_filename = tk.Entry(search_frame, width=70)
entry_filename.grid(row=0, column=1, padx=(5, 5))
tk.Button(search_frame, text="Search", width=8, command=search_filename).grid(row=0, column=2)
tk.Button(search_frame, text="Clear", width=8, command=clear_filename_field).grid(row=0, column=3)

# PDF content search
tk.Label(search_frame, text="📄 PDF Content Keywords").grid(row=1, column=0, sticky="w")
entry_content = tk.Entry(search_frame, width=70)
entry_content.grid(row=1, column=1, padx=(5, 5))
tk.Button(search_frame, text="Search", width=8, command=search_pdf_content).grid(row=1, column=2)
tk.Button(search_frame, text="Clear", width=8, command=clear_content_field).grid(row=1, column=3)

# Filename search results
file_frame = tk.Frame(root)
tk.Label(root, text="📁 Filename Search Results", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
filename_count_label = tk.Label(root, text="(0 results)", anchor="e")
filename_count_label.pack(fill="x", padx=10)
file_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
filename_table = ttk.Treeview(file_frame, columns=("Filename", "Path"), show="headings")
filename_table.heading("Filename", text="Filename")
filename_table.heading("Path", text="Path")
filename_table.column("Filename", width=200)
filename_table.column("Path", width=750)
scroll2 = ttk.Scrollbar(file_frame, orient="vertical", command=filename_table.yview)
filename_table.configure(yscrollcommand=scroll2.set)
filename_table.pack(side="left", fill="both", expand=True)
scroll2.pack(side="right", fill="y")

# PDF content search results
pdf_frame = tk.Frame(root)
tk.Label(root, text="📄 PDF Content Search Results", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
pdf_count_label = tk.Label(root, text="(0 results)", anchor="e")
pdf_count_label.pack(fill="x", padx=10)
pdf_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
pdf_table = ttk.Treeview(pdf_frame, columns=("Filename", "Path", "Page", "Excerpt"), show="headings")
for col in ("Filename", "Path", "Page","Excerpt"):
    pdf_table.heading(col, text=col)
    if col == "Path":
        pdf_table.column(col, width=450)
    elif col == "Excerpt":
        pdf_table.column(col, width=300)
    else:
        pdf_table.column(col, width=100)
scroll1 = ttk.Scrollbar(pdf_frame, orient="vertical", command=pdf_table.yview)
pdf_table.configure(yscrollcommand=scroll1.set)
pdf_table.pack(side="left", fill="both", expand=True)
scroll1.pack(side="right", fill="y")

status_label = tk.Label(root, text="", fg="blue", anchor="w")
status_label.pack(fill="x", padx=10, pady=(0, 5))

root.mainloop()
