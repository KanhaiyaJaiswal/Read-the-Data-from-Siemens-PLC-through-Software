import tkinter as tk
from tkinter import messagebox
from snap7.client import Client
from snap7.util import get_int, get_real
from snap7 import Area

def read_plc_data():
    try:
        ip = ip_entry.get()
        db_number = int(db_entry.get())
        start_byte = int(start_entry.get())
        size = int(size_entry.get())

        plc = Client()
        plc.connect(ip, 0, 1)

        if not plc.get_connected():
            messagebox.showerror("Connection Error", "Could not connect to PLC")
            return

        data = plc.read_area(Area.DB, db_number, start_byte, size)

        # Extract INT and REAL values
        int1 = get_int(data, 0)
        int2 = get_int(data, 2)
        real1 = get_real(data, 4)
        real2 = get_real(data, 8)

        int1_label.config(text=f"INT1: {int1}")
        int2_label.config(text=f"INT2: {int2}")
        real1_label.config(text=f"REAL1: {real1:.2f}")
        real2_label.config(text=f"REAL2: {real2:.2f}")

        plc.disconnect()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("PLC Data Reader (Snap7)")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="PLC IP:").pack()
ip_entry = tk.Entry(root)
ip_entry.insert(0, "192.168.1.20")
ip_entry.pack()

tk.Label(root, text="DB Number:").pack()
db_entry = tk.Entry(root)
db_entry.insert(0, "10")
db_entry.pack()

tk.Label(root, text="Start Byte:").pack()
start_entry = tk.Entry(root)
start_entry.insert(0, "0")
start_entry.pack()

tk.Label(root, text="Size (Bytes):").pack()
size_entry = tk.Entry(root)
size_entry.insert(0, "100")
size_entry.pack()

tk.Button(root, text="Read Data", command=read_plc_data, bg="green", fg="white").pack(pady=10)

int1_label = tk.Label(root, text="INT1: ")
int1_label.pack()
int2_label = tk.Label(root, text="INT2: ")
int2_label.pack()
real1_label = tk.Label(root, text="REAL1: ")
real1_label.pack()
real2_label = tk.Label(root, text="REAL2: ")
real2_label.pack()

root.mainloop()