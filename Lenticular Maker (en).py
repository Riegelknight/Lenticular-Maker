import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import math, os

class LenticularMaker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lenticular Maker")
        self.geometry("340x470")
        self.minsize(200, 200)
        self.image_list = []  # List of images: {path, width, height}
        self.calc = {}
        # Parameter variables
        self.stripe_dir = tk.StringVar(value="vertical")
        self.lpi_var = tk.StringVar(value="100")
        self.ppi_var = tk.StringVar(value="600")
        self.width_cm = tk.StringVar()        # Default: empty
        self.width_inch = tk.StringVar(value="1")  # Required for vertical
        self.height_cm = tk.StringVar()       # Default: empty
        self.height_inch = tk.StringVar()     # Required for horizontal
        # Constant text for "optional"
        self.optional_text = "optional"
        self.create_widgets()
        self.bind("<Configure>", self.on_resize)

    def validate_numeric(self, P):
        # Allow empty input; otherwise only digits and at most one dot or comma.
        if P == "":
            return True
        for char in P:
            if char not in "0123456789.,":
                return False
        if P.count('.') + P.count(',') > 1:
            return False
        return True

    def create_widgets(self):
        vcmd = (self.register(self.validate_numeric), '%P')
        # --- 1. Image Management ---
        self.frm_images = tk.Frame(self)
        self.frm_images.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Top: Buttons
        self.frm_img_buttons = tk.Frame(self.frm_images)
        self.frm_img_buttons.grid(row=0, column=0, sticky="w")
        btn_add = tk.Button(self.frm_img_buttons, text="Add Images", command=self.add_images)
        btn_add.pack(side="left")
        btn_rem = tk.Button(self.frm_img_buttons, text="Remove Image", command=self.remove_image)
        btn_rem.pack(side="left", padx=(10, 0))
        # Below: Scrollable filename list (Treeview)
        self.frm_tree = tk.Frame(self.frm_images)
        self.frm_tree.grid(row=1, column=0, sticky="nsew", pady=(5,0))
        self.frm_images.rowconfigure(1, weight=1)
        self.frm_images.columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(self.frm_tree, columns=("dim"), show="tree", height=5)
        self.tree.heading("#0", text="Filename")
        self.tree.heading("dim", text="Dimensions")
        # Column ratio: 75% for filename, 25% for dimensions
        self.tree.column("#0", anchor="w")
        self.tree.column("dim", anchor="e")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.frm_tree.rowconfigure(0, weight=1)
        self.frm_tree.columnconfigure(0, weight=1)
        scr = ttk.Scrollbar(self.frm_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scr.set)
        scr.grid(row=0, column=1, sticky="ns")

        # --- 2. Parameter Settings ---
        self.frm_params = tk.Frame(self)
        self.frm_params.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        # Stripe direction
        tk.Label(self.frm_params, text="Stripe Direction:").grid(row=0, column=0, sticky="w")
        tk.Radiobutton(self.frm_params, text="Vertical", variable=self.stripe_dir, value="vertical",
                       command=self.param_changed).grid(row=0, column=1, sticky="w")
        tk.Radiobutton(self.frm_params, text="Horizontal", variable=self.stripe_dir, value="horizontal",
                       command=self.param_changed).grid(row=0, column=2, sticky="w")
        # LPI input
        tk.Label(self.frm_params, text="LPI:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.frm_params, textvariable=self.lpi_var, width=7, validate="key", validatecommand=vcmd)\
            .grid(row=1, column=1, columnspan=2, sticky="w")
        # Image width (cm & inch)
        self.lbl_width = tk.Label(self.frm_params, text="Image width (cm/inch):")
        self.lbl_width.grid(row=2, column=0, sticky="w")
        tk.Entry(self.frm_params, textvariable=self.width_cm, width=7, validate="key", validatecommand=vcmd)\
            .grid(row=2, column=1, sticky="w")
        et_width_inch = tk.Entry(self.frm_params, textvariable=self.width_inch, width=7, validate="key", validatecommand=vcmd)
        et_width_inch.grid(row=2, column=2, sticky="w")
        et_width_inch.bind("<KeyRelease>", self.on_width_inch)
        # Image height (cm & inch)
        self.lbl_height = tk.Label(self.frm_params, text=f"{self.optional_text}: Image height (cm/inch):")
        self.lbl_height.grid(row=3, column=0, sticky="w")
        tk.Entry(self.frm_params, textvariable=self.height_cm, width=7, validate="key", validatecommand=vcmd)\
            .grid(row=3, column=1, sticky="w")
        et_height_inch = tk.Entry(self.frm_params, textvariable=self.height_inch, width=7, validate="key", validatecommand=vcmd)
        et_height_inch.grid(row=3, column=2, sticky="w")
        et_height_inch.bind("<KeyRelease>", self.on_height_inch)
        # PPI input
        tk.Label(self.frm_params, text="PPI:").grid(row=4, column=0, sticky="w")
        tk.Entry(self.frm_params, textvariable=self.ppi_var, width=7, validate="key", validatecommand=vcmd)\
            .grid(row=4, column=1, columnspan=2, sticky="w")
        # Trigger recalculation for fields (except for inch fields; those are handled via binding)
        for var in (self.lpi_var, self.ppi_var, self.width_cm, self.height_cm):
            var.trace_add("write", lambda *args: self.param_changed())

        # --- 3. Info Area ---
        self.txt_info = tk.Text(self, height=9)
        self.txt_info.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.txt_info.tag_config("error", foreground="red")

        # --- 4. Generate Image Button ---
        btn_generate = tk.Button(self, text="Generate Image", command=self.generate_image)
        btn_generate.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        # Only the filename list and info area resize dynamically
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_width_inch(self, event):
        # When typing in the inch field for width, clear the cm field
        self.width_cm.set("")
        self.param_changed()

    def on_height_inch(self, event):
        # When typing in the inch field for height, clear the cm field
        self.height_cm.set("")
        self.param_changed()

    def add_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
        for f in files:
            if not any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".bmp"]):
                continue
            try:
                with Image.open(f) as im:
                    w, h = im.size
            except Exception:
                continue
            self.image_list.append({"path": f, "width": w, "height": h})
            fname = os.path.basename(f)
            self.tree.insert("", "end", text=fname, values=(f"{w}x{h}",))
        self.clear_error()
        self.param_changed()

    def remove_image(self):
        for item in self.tree.selection():
            idx = self.tree.index(item)
            self.tree.delete(item)
            if idx < len(self.image_list):
                del self.image_list[idx]
        self.clear_error()
        self.param_changed()

    def clear_error(self):
        self.txt_info.delete("1.0", tk.END)

    def param_changed(self):
        self.clear_error()
        # Optional hint: For vertical, image width (inch) is required; for horizontal, image height (inch) is required.
        if self.stripe_dir.get() == "vertical":
            self.lbl_width.config(text="Image width (cm/inch):")
            self.lbl_height.config(text=f"{self.optional_text}: Image height (cm/inch):")
        else:
            self.lbl_width.config(text=f"{self.optional_text}: Image width (cm/inch):")
            self.lbl_height.config(text="Image height (cm/inch):")
        # Conversion: if cm is entered, update inch field accordingly.
        if self.width_cm.get():
            try:
                cm_val = float(self.width_cm.get().replace(",", "."))
                if cm_val > 0:
                    self.width_inch.set(str(round(cm_val / 2.54, 3)))
            except:
                pass
        if self.height_cm.get():
            try:
                cm_val = float(self.height_cm.get().replace(",", "."))
                if cm_val > 0:
                    self.height_inch.set(str(round(cm_val / 2.54, 3)))
            except:
                pass
        self.recalc()

    def recalc(self):
        self.txt_info.delete("1.0", tk.END)
        if len(self.image_list) < 2:
            return
        try:
            LPI = float(self.lpi_var.get().replace(",", "."))
            PPI = float(self.ppi_var.get().replace(",", "."))
            if LPI <= 0 or PPI <= 0:
                raise ValueError
        except:
            self.txt_info.insert(tk.END, "LPI and PPI must be > 0", "error")
            return
        num_images = len(self.image_list)
        dirc = self.stripe_dir.get()
        stretching = False

        if dirc == "vertical":
            # Required: Image width (inch) must be > 0
            try:
                width_in = float(self.width_inch.get().replace(",", "."))
                if width_in <= 0:
                    raise ValueError
            except:
                self.txt_info.insert(tk.END, "Image width (inch) must not be empty", "error")
                return
            final_width = round(PPI * width_in)
            if self.height_inch.get().strip() != "":
                try:
                    h_in = float(self.height_inch.get().replace(",", "."))
                    if h_in <= 0:
                        raise ValueError
                    final_height = round(final_width * (h_in / width_in))
                    stretching = True
                except:
                    self.txt_info.insert(tk.END, "Invalid value for image height (inch)", "error")
                    return
            else:
                first = self.image_list[0]
                final_height = round(final_width * (first["height"] / first["width"]))
            Q = math.ceil(final_width / num_images)
            true_width = final_width / PPI
            true_height = final_height / PPI
        else:  # horizontal
            # Required: Image height (inch) must be > 0
            try:
                h_in = float(self.height_inch.get().replace(",", "."))
                if h_in <= 0:
                    raise ValueError
            except:
                self.txt_info.insert(tk.END, "Image height (inch) must not be empty", "error")
                return
            final_height = round(PPI * h_in)
            if self.width_inch.get().strip() != "":
                try:
                    width_in = float(self.width_inch.get().replace(",", "."))
                    if width_in <= 0:
                        raise ValueError
                    final_width = round(final_height * (width_in / h_in))
                    stretching = True
                except:
                    self.txt_info.insert(tk.END, "Invalid value for image width (inch)", "error")
                    return
            else:
                first = self.image_list[0]
                final_width = round(final_height * (first["width"] / first["height"]))
            Q = math.ceil(final_height / num_images)
            true_height = final_height / PPI
            true_width = final_width / PPI

        stripe_width = max(round(PPI / (num_images * LPI)), 1)
        true_lpi = PPI / (num_images * stripe_width)

        info = (f"Number of images: {num_images}\n"
                f"Final image width (px): {final_width}\n"
                f"Final image height (px): {final_height}\n"
                f"True image width (inch): {true_width:.4f}\n"
                f"True image height (inch): {true_height:.4f}\n"
                f"Stretching: {'active' if stretching else 'inactive'}\n"
                f"Stripe width (px): {stripe_width}\n"
                f"True LPI: {true_lpi:.2f}\n")
        self.calc = {"dir": dirc, "Bildendbreite": final_width, "Bildendhöhe": final_height,
                     "Q": Q, "stripe_width": stripe_width}
        self.txt_info.insert(tk.END, info)

    def on_resize(self, event):
        # Dynamically adjust only the Treeview (filename list)
        if self.tree:
            new_width = self.frm_tree.winfo_width()
            if new_width > 0:
                self.tree.column("#0", width=int(new_width * 0.75))
                self.tree.column("dim", width=int(new_width * 0.25))
            new_height = max(3, int(self.frm_tree.winfo_height() / 20))
            self.tree.config(height=new_height)

    def generate_image(self):
        if not self.calc:
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG", "*.png")])
        if not save_path:
            return
        dirc = self.calc["dir"]
        final_width = self.calc["Bildendbreite"]
        final_height = self.calc["Bildendhöhe"]
        Q = self.calc["Q"]
        stripe_width = self.calc["stripe_width"]
        num_images = len(self.image_list)
        imgs = []
        for item in self.image_list:
            try:
                im = Image.open(item["path"])
                # For vertical, no rotation; horizontal images are not rotated either (directly sliced)
                if dirc == "horizontal":
                    pass
                # Scale images: For vertical, size becomes (Q, final_height); for horizontal, (final_width, Q)
                if dirc == "vertical":
                    im = im.resize((Q, final_height))
                else:
                    im = im.resize((final_width, Q))
                imgs.append(im)
            except:
                continue
        if not imgs:
            return
        if dirc == "vertical":
            final = Image.new("RGB", (final_width, final_height))
            pointers = [0] * num_images
            x = 0
            while x < final_width:
                for i in range(num_images):
                    if x >= final_width:
                        break
                    if pointers[i] < Q:
                        sw = min(stripe_width, Q - pointers[i], final_width - x)
                        stripe = imgs[i].crop((pointers[i], 0, pointers[i] + sw, final_height))
                        final.paste(stripe, (x, 0))
                        pointers[i] += sw
                        x += sw
        else:  # horizontal
            final = Image.new("RGB", (final_width, final_height))
            pointers = [0] * num_images
            y = 0
            while y < final_height:
                for i in range(num_images):
                    if y >= final_height:
                        break
                    if pointers[i] < Q:
                        sh = min(stripe_width, Q - pointers[i], final_height - y)
                        stripe = imgs[i].crop((0, pointers[i], final_width, pointers[i] + sh))
                        final.paste(stripe, (0, y))
                        pointers[i] += sh
                        y += sh
        try:
            final.save(save_path)
        except Exception as e:
            self.txt_info.insert(tk.END, f"Save error: {e}", "error")

if __name__ == "__main__":
    app = LenticularMaker()
    app.mainloop()
