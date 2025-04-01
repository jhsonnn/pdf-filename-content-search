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
    # 현재 실행 중인 프로세스 확인
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'everything.exe' in proc.info['name'].lower():
            print("Everything already running.")
            return  # 이미 실행 중이면 종료

    # 실행 중이 아니면 백그라운드에서 실행
    try:
        print("Launching Everything in the background...")
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # 창 숨기기
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
        print(f"PDF 열기 실패: {filepath} → {e}")
    return None

def get_excerpt(text, keywords):
    lower_text = text.lower()
    for kw in keywords:
        if kw in lower_text:
            idx = lower_text.find(kw)
            return text[max(0, idx - 20):idx + 50].replace("\n", " ")
    return "..."

def run_pdf_search(content_keywords):
    update_status("PDF 내용 검색 중...")
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
        pdf_count_label.config(text=f"({len(results)}건)")
        update_status("PDF 내용 검색 완료.")

    root.after(0, update_ui)

def everything_search(keyword):
    ensure_everything_running()

    # 검색 쿼리 생성
    search_query = f'path:"{os.path.join(SEARCH_FOLDER, "1")}" | path:"{os.path.join(SEARCH_FOLDER, "2")}" {keyword}'
    print(f"Executing search query: {search_query}")
    everything.Everything_SetSearchW(search_query)
    everything.Everything_QueryW(1)

    # 검색 결과 개수 가져오기
    num_results = everything.Everything_GetNumResults()
    print(f"Number of results: {num_results}")

    # 검색 결과 처리
    results = [
        (
            everything.Everything_GetResultFileNameW(i), 
            os.path.join(everything.Everything_GetResultPathW(i), everything.Everything_GetResultFileNameW(i))
        )
        for i in range(min(num_results, MAX_RESULTS))
    ]

    # 중복 제거
    unique_results = list(set(results))
    print(f"Unique Results: {unique_results}")
    return unique_results

def run_filename_search(filename_keywords):
    update_status("파일명 검색 중...")
    results = []

    # 키워드별로 검색 수행
    for keyword in filename_keywords:
        results.extend(everything_search(keyword))

    # 중복 제거
    unique_results = list(set(results))

    def update_ui():
        filename_table.delete(*filename_table.get_children())
        for file, path in unique_results:
            filename_table.insert("", "end", values=(file, path))
        filename_count_label.config(text=f"({len(unique_results)}건)")
        update_status("파일명 검색 완료.")

    root.after(0, update_ui)

def search_pdf_content():
    content_input = entry_content.get().strip()
    content_keywords = [kw.strip().lower() for kw in content_input.split(',') if kw.strip()]
    if content_keywords:
        threading.Thread(target=run_pdf_search, args=(content_keywords,), daemon=True).start()
    else:
        messagebox.showwarning("입력 필요", "PDF 내용 검색어를 입력하세요.")

def search_filename():
    filename_input = entry_filename.get().strip()
    filename_keywords = [kw.strip().lower() for kw in filename_input.split(',') if kw.strip()]
    if filename_keywords:
        threading.Thread(target=run_filename_search, args=(filename_keywords,), daemon=True).start()
    else:
        messagebox.showwarning("입력 필요", "파일명 검색어를 입력하세요.")

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
root.title("PDF 내부 텍스트 및 파일명 검색기")
root.geometry("1000x800")

search_frame = tk.Frame(root)
search_frame.pack(padx=10, pady=10, anchor="w")

# Filename search
tk.Label(search_frame, text="📁 파일명 검색어").grid(row=0, column=0, sticky="w")
entry_filename = tk.Entry(search_frame, width=70)
entry_filename.grid(row=0, column=1, padx=(5, 5))
tk.Button(search_frame, text="검색", width=8, command=search_filename).grid(row=0, column=2)
tk.Button(search_frame, text="초기화", width=8, command=clear_filename_field).grid(row=0, column=3)

# PDF content search
tk.Label(search_frame, text="📄 PDF 내용 검색어").grid(row=1, column=0, sticky="w")
entry_content = tk.Entry(search_frame, width=70)
entry_content.grid(row=1, column=1, padx=(5, 5))
tk.Button(search_frame, text="검색", width=8, command=search_pdf_content).grid(row=1, column=2)
tk.Button(search_frame, text="초기화", width=8, command=clear_content_field).grid(row=1, column=3)

# Filename search results
file_frame = tk.Frame(root)
tk.Label(root, text="📁 파일명 검색 결과", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
filename_count_label = tk.Label(root, text="(0건)", anchor="e")
filename_count_label.pack(fill="x", padx=10)
file_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
filename_table = ttk.Treeview(file_frame, columns=("파일명", "경로"), show="headings")
filename_table.heading("파일명", text="파일명")
filename_table.heading("경로", text="경로")
filename_table.column("파일명", width=200)
filename_table.column("경로", width=750)
scroll2 = ttk.Scrollbar(file_frame, orient="vertical", command=filename_table.yview)
filename_table.configure(yscrollcommand=scroll2.set)
filename_table.pack(side="left", fill="both", expand=True)
scroll2.pack(side="right", fill="y")

# PDF content search results
pdf_frame = tk.Frame(root)
tk.Label(root, text="📄 PDF 내용 검색 결과", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
pdf_count_label = tk.Label(root, text="(0건)", anchor="e")
pdf_count_label.pack(fill="x", padx=10)
pdf_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
pdf_table = ttk.Treeview(pdf_frame, columns=("파일명", "경로", "페이지", "문장 발췌"), show="headings")
for col in ("파일명", "경로", "페이지", "문장 발췌"):
    pdf_table.heading(col, text=col)
    if col == "경로":
        pdf_table.column(col, width=450)
    elif col == "문장 발췌":
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
