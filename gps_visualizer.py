import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseEvent

def load_and_plot():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path)

        if 'Longitude' not in df.columns or 'Latitude' not in df.columns:
            messagebox.showerror("Missing Columns", "CSV must contain 'Longitude' and 'Latitude'.")
            return

        # Clear previous content
        for widget in frame.winfo_children():
            widget.destroy()
        info_label.config(text="")

        # Plotting
        fig, ax = plt.subplots(figsize=(6, 4))
        sc = ax.scatter(df['Longitude'], df['Latitude'], c='blue', label="GPS Path")
        ax.set_title("GPS Trajectory")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True)

        # Interaction callback to show index
        def on_click(event: MouseEvent):
            if event.inaxes == ax:
                x, y = event.xdata, event.ydata
                distances = ((df['Longitude'] - x)**2 + (df['Latitude'] - y)**2)
                nearest_index = distances.idxmin()
                info_label.config(text=f"Closest Index: {nearest_index} | Longitude: {df.loc[nearest_index, 'Longitude']:.6f}, Latitude: {df.loc[nearest_index, 'Latitude']:.6f}")

        fig.canvas.mpl_connect('button_press_event', on_click)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("GPS Data Plotter with Index Viewer")
root.geometry("800x650")

btn = tk.Button(root, text="Load GPS CSV and Plot", command=load_and_plot, font=('Arial', 12))
btn.pack(pady=10)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

info_label = tk.Label(root, text="", font=('Arial', 11), fg="darkgreen")
info_label.pack(pady=5)

root.mainloop()
