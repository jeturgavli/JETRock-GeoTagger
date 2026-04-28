import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import piexif


# ------------------ LOGIC SAME ------------------ #
def to_deg(value, loc):
    if value < 0:
        loc_value = loc[0]
    else:
        loc_value = loc[1]

    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    minute = int(t1)
    sec = round((t1 - minute) * 60, 5)

    return (deg, minute, sec), loc_value


def change_to_rational(number):
    return (int(number * 1000000), 1000000)


def select_image():
    file = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")])
    image_path.set(file)


def select_output():
    file = filedialog.asksaveasfilename(defaultextension=".jpg",
                                        filetypes=[("JPEG files", "*.jpg")])
    output_path.set(file)


def add_metadata():
    try:
        img_path = image_path.get()
        out_path = output_path.get()

        if not img_path or not out_path:
            messagebox.showerror("Error", "Select image and output path!")
            return

        lat = float(lat_entry.get())
        lon = float(lon_entry.get())
        keywords = keywords_entry.get()
        description = desc_entry.get()

        lat_deg = to_deg(lat, ["S", "N"])
        lon_deg = to_deg(lon, ["W", "E"])

        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = lat_deg[1]
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = [
            change_to_rational(x) for x in lat_deg[0]
        ]
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = lon_deg[1]
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = [
            change_to_rational(x) for x in lon_deg[0]
        ]

        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode("utf-8")
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le")

        exif_bytes = piexif.dump(exif_dict)

        img = Image.open(img_path)
        img.save(out_path, "jpeg", exif=exif_bytes)

        messagebox.showinfo("Success", "✅ Metadata added successfully!")

    except ValueError:
        messagebox.showerror("Error", "Invalid latitude or longitude!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# ------------------ UI DESIGN ------------------ #
root = Tk()
root.title("📍 Image Geo Tagger - JET Rock")
root.geometry("520x420")
root.configure(bg="#f5f5f5")

image_path = StringVar()
output_path = StringVar()

# Title
Label(root, text="Image Geo Tagger", font=("Arial", 16, "bold"),
      bg="#f5f5f5").pack(pady=10)

frame = Frame(root, bg="#ffffff", bd=2, relief=RIDGE)
frame.pack(padx=15, pady=10, fill="both", expand=True)

# ---------- Image Selection ----------
Label(frame, text="Select Image", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
Entry(frame, textvariable=image_path, width=40).grid(row=0, column=1, padx=5)
Button(frame, text="Browse", command=select_image).grid(row=0, column=2, padx=5)

# ---------- Output ----------
Label(frame, text="Save As", bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
Entry(frame, textvariable=output_path, width=40).grid(row=1, column=1, padx=5)
Button(frame, text="Browse", command=select_output).grid(row=1, column=2, padx=5)

# ---------- Coordinates ----------
Label(frame, text="Latitude", bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
lat_entry = Entry(frame)
lat_entry.grid(row=2, column=1, padx=5)

Label(frame, text="Longitude", bg="white").grid(row=3, column=0, sticky="w", padx=10, pady=5)
lon_entry = Entry(frame)
lon_entry.grid(row=3, column=1, padx=5)

# ---------- Metadata ----------
Label(frame, text="Keywords", bg="white").grid(row=4, column=0, sticky="w", padx=10, pady=5)
keywords_entry = Entry(frame, width=40)
keywords_entry.grid(row=4, column=1, columnspan=2, padx=5)

Label(frame, text="Description", bg="white").grid(row=5, column=0, sticky="w", padx=10, pady=5)
desc_entry = Entry(frame, width=40)
desc_entry.grid(row=5, column=1, columnspan=2, padx=5)

# ---------- Button ----------
Button(root, text="🚀 Add Geo Tag",
       command=add_metadata,
       bg="#28a745", fg="white",
       font=("Arial", 11, "bold"),
       padx=10, pady=5).pack(pady=15)

root.mainloop()