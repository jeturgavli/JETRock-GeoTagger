import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import piexif

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    print("Please install tkinterdnd2 by running: pip install tkinterdnd2")
    exit()

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
    files = filedialog.askopenfilenames(filetypes=[("JPEG files", "*.jpg *.jpeg")])
    if files:
        image_path.set(" ".join(f"{{{f}}}" for f in files))
# ------------------------------------------------------

def select_output():
    folder = filedialog.askdirectory()
    if folder:
        output_path.set(folder)
# --------------------------------------------------------------------------

def add_metadata():
    try:
        img_paths_raw = image_path.get()
        out_folder = output_path.get()

        if not img_paths_raw or not out_folder:
            messagebox.showerror("Error", "Select images and output folder!")
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

        img_paths = root.tk.splitlist(img_paths_raw)
        success_count = 0

        for img_path in img_paths:
            if not os.path.isfile(img_path) or not img_path.lower().endswith(('.jpg', '.jpeg')):
                continue
            
            filename = os.path.basename(img_path)
            out_path = os.path.join(out_folder, "geotagged_" + filename)

            img = Image.open(img_path)
            img.save(out_path, "jpeg", exif=exif_bytes)
            success_count += 1

        if success_count > 0:
            messagebox.showinfo("Success", f"✅ Metadata added to {success_count} images!")
        else:
            messagebox.showwarning("Warning", "No valid JPEG images found to process.")

    except ValueError:
        messagebox.showerror("Error", "Invalid latitude or longitude!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = TkinterDnD.Tk()
root.title("Image Geo Tagger - JET Rock(Jetur Gavli)")
root.geometry("520x420")
root.configure(bg="#f5f5f5")

image_path = StringVar()
output_path = StringVar()

Label(root, text="Image Geo Tagger Jetur Gavli", font=("Arial", 16, "bold"),
      bg="#f5f5f5").pack(pady=10)

frame = Frame(root, bg="#ffffff", bd=2, relief=RIDGE)
frame.pack(padx=15, pady=10, fill="both", expand=True)

Label(frame, text="Select Images", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
Entry(frame, textvariable=image_path, width=40).grid(row=0, column=1, padx=5)
Button(frame, text="Browse", command=select_image).grid(row=0, column=2, padx=5)

Label(frame, text="Output Folder", bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
Entry(frame, textvariable=output_path, width=40).grid(row=1, column=1, padx=5)
Button(frame, text="Browse", command=select_output).grid(row=1, column=2, padx=5)

Label(frame, text="Latitude", bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
lat_entry = Entry(frame)
lat_entry.grid(row=2, column=1, padx=5)

Label(frame, text="Longitude", bg="white").grid(row=3, column=0, sticky="w", padx=10, pady=5)
lon_entry = Entry(frame)
lon_entry.grid(row=3, column=1, padx=5)

Label(frame, text="Keywords", bg="white").grid(row=4, column=0, sticky="w", padx=10, pady=5)
keywords_entry = Entry(frame, width=40)
keywords_entry.grid(row=4, column=1, columnspan=2, padx=5)

Label(frame, text="Description", bg="white").grid(row=5, column=0, sticky="w", padx=10, pady=5)
desc_entry = Entry(frame, width=40)
desc_entry.grid(row=5, column=1, columnspan=2, padx=5)

Button(root, text="🚀 Add Geo Tag (Bulk)",
       command=add_metadata,
       bg="#28a745", fg="white",
       font=("Arial", 11, "bold"),
       padx=10, pady=5).pack(pady=15)

def drop_inside(event):
    files = root.tk.splitlist(event.data)
    
    image_path.set(" ".join(f"{{{f}}}" for f in files))
    if files:
        first_file_dir = os.path.dirname(files[0])
        output_path.set(first_file_dir)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop_inside)

root.mainloop()