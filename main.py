import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import piexif


def to_deg(value, loc):
    if value < 0:
        loc_value = loc[0]
    else:
        loc_value = loc[1]

    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    min = int(t1)
    sec = round((t1 - min) * 60, 5)

    return (deg, min, sec), loc_value


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

        # GPS
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = lat_deg[1]
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = [
            change_to_rational(x) for x in lat_deg[0]
        ]
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = lon_deg[1]
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = [
            change_to_rational(x) for x in lon_deg[0]
        ]

        # Description
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode("utf-8")

        # Keywords
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le")

        exif_bytes = piexif.dump(exif_dict)

        img = Image.open(img_path)
        img.save(out_path, "jpeg", exif=exif_bytes)

        messagebox.showinfo("Success", "✅ Metadata added successfully!")

    except ValueError:
        messagebox.showerror("Error", "Invalid latitude or longitude!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
root = Tk()
root.title("Jetur Gavli Program Image Geo Tagger")
root.geometry("450x400")

image_path = StringVar()
output_path = StringVar()

Label(root, text="Select Image").pack()
Entry(root, textvariable=image_path, width=45).pack()
Button(root, text="Browse", command=select_image).pack()

Label(root, text="Save As").pack()
Entry(root, textvariable=output_path, width=45).pack()
Button(root, text="Browse", command=select_output).pack()

Label(root, text="Latitude").pack()
lat_entry = Entry(root)
lat_entry.pack()

Label(root, text="Longitude").pack()
lon_entry = Entry(root)
lon_entry.pack()

Label(root, text="Keywords (comma separated)").pack()
keywords_entry = Entry(root, width=40)
keywords_entry.pack()

Label(root, text="Description").pack()
desc_entry = Entry(root, width=40)
desc_entry.pack()

Button(root, text="Add Geo Tag", command=add_metadata, bg="green", fg="white").pack(pady=15)

root.mainloop()