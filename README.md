# 📍 JET GeoTagger

JET GeoTagger is a simple and lightweight Python GUI application that allows you to add GPS (Geo Tag), keywords, and descriptions to JPEG images by embedding EXIF metadata.

---

## 🚀 Features

- 📌 Add Latitude & Longitude to images
- 🏷️ Add Keywords (comma-separated)
- 📝 Add Image Description
- 🖼️ Supports JPEG images (.jpg / .jpeg)
- 📂 **Bulk Image Processing (Process multiple images at once)**
- 🖱️ **Drag & Drop Support (Easily drop files directly into the app)**
- ⚡ Fast and easy-to-use GUI
- 💻 Built with Python (Tkinter & TkinterDnD)

---

## 🖥️ Preview

Simple GUI with:

- Multiple Image selection & Drag-and-Drop capability
- Output folder selection
- Latitude & Longitude input
- Metadata fields (keywords & description)

---

## 📦 Requirements

Make sure you have Python installed (3.x recommended)

Install dependencies:
```bash
pip install pillow piexif tkinterdnd2
```

## 🏃 How To Run

```bash
python main.py
```

## 📌 Usage

1. Select input images (Select multiple files or **Drag & Drop** them directly)
2. Choose an **Output Folder**
3. Enter:
   - Latitude (e.g., 21.1702)
   - Longitude (e.g., 72.8311)
4. Add optional:
   - Keywords (comma-separated)
   - Description
5. Click "🚀 Add Geo Tag (Bulk)"
6. Done ✅ (All processed images will be saved in the output folder with a `geotagged_` prefix).

## 🛠️ Tech Stack

- Python
- Tkinter (GUI)
- TkinterDnD (Drag & Drop handling)
- Pillow (Image handling)
- piexif (EXIF metadata)

## 📈 Future Improvements

- Map-based coordinate picker
- Dark mode UI
- Progress bar for bulk processing tracking

## 👨‍💻 Author

- [JETRock](https://github.com/jeturgavli)
