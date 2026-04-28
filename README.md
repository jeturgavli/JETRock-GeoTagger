# 📍 JET GeoTagger

JET GeoTagger is a simple and lightweight Python GUI application that allows you to add GPS (Geo Tag), keywords, and descriptions to JPEG images by embedding EXIF metadata.

---

## 🚀 Features

- 📌 Add Latitude & Longitude to images
- 🏷️ Add Keywords (comma-separated)
- 📝 Add Image Description
- 🖼️ Supports JPEG images (.jpg / .jpeg)
- ⚡ Fast and easy-to-use GUI
- 💻 Built with Python (Tkinter)

---

## 🖥️ Preview

Simple GUI with:

- Image selection
- Output file selection
- Latitude & Longitude input
- Metadata fields (keywords & description)

---

## 📦 Requirements

Make sure you have Python installed (3.x recommended)

Install dependencies:

```bash
pip install pillow piexif
```

## How To Run

```bash
python main.py
```

## 📌 Usage

1. Select an input image (JPEG)
2. Choose output file location
3. Enter:
   - Latitude (e.g., 21.1702)
   - Longitude (e.g., 72.8311)
4. Add optional:
   - Keywords (comma-separated)
   - Description
5. Click "Add Geo Tag"
6. Done ✅

## 🛠️ Tech Stack

- Python
- Tkinter (GUI)
- Pillow (Image handling)
- piexif (EXIF metadata)

## 📈 Future Improvements

- Bulk image processing
- Drag & drop support
- Map-based coordinate picker
- Dark mode UI

## 👨‍💻 Author

- [JETRock](https://github.com/jeturgavli)
