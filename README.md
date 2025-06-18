# Selenium Image & Text Crawler

## Overview
This project provides Python scripts to automatically crawl:
- **Images from Google Image Search**
- **Text content from Namuwiki**
using Selenium WebDriver.

---

## Features

### 1. Image Crawling (`image_crawling.py`)
- Downloads images in bulk from Google Images for a given keyword
- Supports JPG and PNG formats
- Automatically creates folders for each keyword
- Logs download success/failure

### 2. Namuwiki Text Crawling (`namu.py`)
- Crawls the main text content of a Namuwiki article for a given keyword
- Removes disclaimers and unnecessary text
- Saves the result as a `.txt` file

---

## Project Structure

```
.
├── image_crawling.py
├── namu.py
├── README.md
├── images/           # Downloaded images
├── texts/            # Downloaded text files
└── util/
    ├── image_utils.py
    ├── browser_utils.py
    └── ...
```

---

## Requirements
- Python **3.11**
- `selenium` Python package
- Google Chrome browser (latest version)

> **Note:** ChromeDriver is no longer required. Selenium 4.6+ supports automatic driver management.

Install dependencies:
```bash
pip install selenium
```

---

## How to Use

### Image Crawling
```bash
python image_crawling.py
```
- Enter the search keyword, number of images, and image format when prompted.
- Images will be saved in `images/<keyword>/`.

### Namuwiki Text Crawling
```bash
python namu.py
```
- Enter the search keyword when prompted.
- The article text will be saved in `texts/<keyword>.txt`.

---

## Example Output
- `images/Trickcal/Trickcal_1.jpg` (image files)
- `texts/Sunrin_Internet_High_School.txt` (text file)

---

## Notes
- If Google or Namuwiki changes their website structure, crawling may stop working.
- Excessive crawling may violate the terms of service of the target sites.

---
