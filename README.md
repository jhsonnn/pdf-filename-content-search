# PDF Filename & Content Search GUI Tool (Windows Only)
# PDF 파일명 및 내용 검색 GUI Tool (윈도우 전용)

This tool allows you to search PDF files by **filename** and **internal content** within specified folders.  
It combines the fast search capability of **Everything** with multithreaded PDF text extraction using `pdfplumber`.

이 도구는 지정된 폴더 내의 PDF 파일을 **파일명**과 **내부 내용** 기준으로 검색할 수 있는 Windows GUI 프로그램입니다.  
**Everything**의 빠른 파일 검색 기능과 `pdfplumber`의 멀티스레드 텍스트 추출을 결합했습니다.

---

## Installation / 설치 방법

To use this project, install the required packages and prepare the DLL.
이 프로젝트를 사용하려면 필요한 패키지를 설치하고 DLL 파일을 준비하세요.

### 1. Install Python Packages / 파이썬 패키지 설치

> `pdfplumber`, `psutil` 패키지를 설치합니다.  
> => pip install pdfplumber psutil

### 2. Prepare Everything64.dll / Everything64.dll 준비

Make sure the following file exists in the same directory as the script:
Everything64.dll
다음 파일이 `pdf-filename-content-search.py`와 동일한 폴더에 있어야 합니다:
Everything64.dll

> `Everything64.dll` 파일을 `pdf-filename-content-search.py` 파일과 같은 폴더에 위치시키세요.

You can also get `Everything64.dll` by installing [Everything](https://www.voidtools.com/downloads/).
[Everything](https://www.voidtools.com/downloads/) 이 경로에서 다운 받을 수도 있습니다.
설치하셨다면면 Everything의 설치 폴더에서 `Everything64.dll` 파일을 찾아 복사하세요.

복사 위치:
pdf-filename-content-search.py 파일이 있는 동일한 폴더

---

## Folder Structure / 폴더 구조

By default, the script searches PDF files in the following two folders:
C:\Users\YourUsername\Desktop\1 and C:\Users\YourUsername\Desktop\2

기본적으로 스크립트는 다음 두 폴더 내의 PDF 파일을 검색합니다:
C:\Users\YourUsername\Desktop\1, C:\Users\YourUsername\Desktop\2

To change the root path or target folders, edit the following lines in pdf-filename-content-search.py:

```python
SEARCH_FOLDER = r"C:\Users\YourUsername\Desktop\pdf-filename-content-search"
TARGET_FOLDERS = ['1', '2']

The program assumes that the files you want to search are located in the folders named 1 and 2.
If you want to search in other folders, simply update the folder names in the configuration.
현재 이 프로그램은 검색하려는 파일들이 1, 2 폴더에 있다고 가정하고 동작합니다.
다른 폴더에서 검색하고 싶다면, 위 설정 부분에서 폴더 이름을 원하는 대로 수정하면 됩니다.


## How to Run / 실행 방법
Run the script using Python:
python pdf-filename-content-search.py
파이썬으로 위 명령어를 실행하면 GUI 창이 열립니다.


## How to Setup  Everything / Everything 세팅 방법
To enable fast filename searching using Everything, you need to set the indexing folders:

1. Open Everything

2. Go to Tools > Options > Indexes > Folders

3. Add the folders (e.g., C:\Users\YourUsername\Desktop\1, 2, etc.) you want to include in the search

This will make the specified folders indexed by Everything, allowing for fast searching.

Everything을 통한 빠른 파일명 검색을 위해 색인할 폴더를 설정해야 합니다:

1. Everything을 실행하세요

2. 도구 > 설정 > 색인 > 폴더 로 이동합니다

3. 검색을 원하는 경로(예: C:\Users\YourUsername\Desktop\1, 2 등)를 추가하세요

이렇게 설정하면 지정된 폴더 내 파일을 빠르게 검색할 수 있습니다.



## Features / 주요 기능
Fast filename search using Everything

PDF content search using pdfplumber

Multithreaded search with ThreadPoolExecutor

GUI built with tkinter

Everything을 이용한 초고속 파일명 검색

pdfplumber를 통한 PDF 내부 텍스트 검색

ThreadPoolExecutor를 사용한 멀티스레드 검색

tkinter 기반의 직관적인 GUI

🖼️ Screenshot / 스크린샷
Add a screenshot here if desired.
원한다면 여기에 GUI 스크린샷을 추가하세요.

🖥️ Compatibility / 호환성
Windows only (Everything DLL is Windows-specific)

Python 3.9+ recommended

Windows 전용 (Everything은 Windows에서만 작동)

Python 3.9 이상 권장

📄 License / 라이선스
This project is licensed under the MIT License.
본 프로젝트는 MIT 라이선스로 배포됩니다.
# PDF Filename & Content Search GUI Tool (Windows Only)
# PDF 파일명 및 내용 검색 GUI Tool (윈도우 전용)

This tool allows you to search PDF files by **filename** and **internal content** within specified folders.  
It combines the fast search capability of **Everything** with multithreaded PDF text extraction using `pdfplumber`.

이 도구는 지정된 폴더 내의 PDF 파일을 **파일명**과 **내부 내용** 기준으로 검색할 수 있는 Windows GUI 프로그램입니다.  
**Everything**의 빠른 파일 검색 기능과 `pdfplumber`의 멀티스레드 텍스트 추출을 결합했습니다.

---

## Installation / 설치 방법

To use this project, install the required packages and prepare the DLL.
이 프로젝트를 사용하려면 필요한 패키지를 설치하고 DLL 파일을 준비하세요.

### 1. Install Python Packages / 파이썬 패키지 설치

> `pdfplumber`, `psutil` 패키지를 설치합니다.  
> => pip install pdfplumber psutil

### 2. Prepare Everything64.dll / Everything64.dll 준비

Make sure the following file exists in the same directory as the script:
Everything64.dll
다음 파일이 `pdf-filename-content-search.py`와 동일한 폴더에 있어야 합니다:
Everything64.dll

> `Everything64.dll` 파일을 `pdf-filename-content-search.py` 파일과 같은 폴더에 위치시키세요.

You can also get `Everything64.dll` by installing [Everything](https://www.voidtools.com/downloads/).
[Everything](https://www.voidtools.com/downloads/) 이 경로에서 다운 받을 수도 있습니다.
설치하셨다면면 Everything의 설치 폴더에서 `Everything64.dll` 파일을 찾아 복사하세요.

복사 위치:
pdf-filename-content-search.py 파일이 있는 동일한 폴더

---

## Folder Structure / 폴더 구조

By default, the script searches PDF files in the following two folders:
C:\Users\YourUsername\Desktop\1 and C:\Users\YourUsername\Desktop\2

기본적으로 스크립트는 다음 두 폴더 내의 PDF 파일을 검색합니다:
C:\Users\YourUsername\Desktop\1, C:\Users\YourUsername\Desktop\2

To change the root path or target folders, edit the following lines in pdf-filename-content-search.py:

```python
SEARCH_FOLDER = r"C:\Users\YourUsername\Desktop\pdf-filename-content-search"
TARGET_FOLDERS = ['1', '2']

The program assumes that the files you want to search are located in the folders named 1 and 2.
If you want to search in other folders, simply update the folder names in the configuration.
현재 이 프로그램은 검색하려는 파일들이 1, 2 폴더에 있다고 가정하고 동작합니다.
다른 폴더에서 검색하고 싶다면, 위 설정 부분에서 폴더 이름을 원하는 대로 수정하면 됩니다.


## How to Run / 실행 방법
Run the script using Python:
python pdf-filename-content-search.py
파이썬으로 위 명령어를 실행하면 GUI 창이 열립니다.


## How to Setup  Everything / Everything 세팅 방법
To enable fast filename searching using Everything, you need to set the indexing folders:

1. Open Everything

2. Go to Tools > Options > Indexes > Folders

3. Add the folders (e.g., C:\Users\YourUsername\Desktop\1, 2, etc.) you want to include in the search

This will make the specified folders indexed by Everything, allowing for fast searching.

Everything을 통한 빠른 파일명 검색을 위해 색인할 폴더를 설정해야 합니다:

1. Everything을 실행하세요

2. 도구 > 설정 > 색인 > 폴더 로 이동합니다

3. 검색을 원하는 경로(예: C:\Users\YourUsername\Desktop\1, 2 등)를 추가하세요

이렇게 설정하면 지정된 폴더 내 파일을 빠르게 검색할 수 있습니다.



## Features / 주요 기능
Fast filename search using Everything

PDF content search using pdfplumber

Multithreaded search with ThreadPoolExecutor

GUI built with tkinter

Everything을 이용한 초고속 파일명 검색

pdfplumber를 통한 PDF 내부 텍스트 검색

ThreadPoolExecutor를 사용한 멀티스레드 검색

tkinter 기반의 직관적인 GUI

🖼️ Screenshot
Add a screenshot here if desired.
원한다면 여기에 GUI 스크린샷을 추가하세요.

🖥️ Compatibility / 호환성
Windows only (Everything DLL is Windows-specific)

Python 3.9+ recommended

Windows 전용 (Everything은 Windows에서만 작동)

Python 3.9 이상 권장

📄 License
This project is licensed under the MIT License.
본 프로젝트는 MIT 라이센스로 배포됩니다.
