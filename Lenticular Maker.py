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
        self.image_list = []  # Liste der Bilder: {path, width, height}
        self.calc = {}
        # Parameter-Variablen
        self.stripe_dir = tk.StringVar(value="vertikal")
        self.lpi_var = tk.StringVar(value="100")
        self.ppi_var = tk.StringVar(value="600")
        self.width_cm = tk.StringVar()
        self.width_inch = tk.StringVar(value="1")  # Pflicht bei vertikal
        self.height_cm = tk.StringVar()
        self.height_inch = tk.StringVar()          # Pflicht bei horizontal
        self.create_widgets()
        self.bind("<Configure>", self.on_resize)

    def validate_numeric(self, P):
        # Erlaubt leere Eingabe; ansonsten nur Ziffern, maximal ein Punkt oder Komma.
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
        # --- 1. Bildverwaltung ---
        self.frm_images = tk.Frame(self)
        self.frm_images.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # Oben: Buttons (fix angeordnet)
        self.frm_img_buttons = tk.Frame(self.frm_images)
        self.frm_img_buttons.grid(row=0, column=0, sticky="w")
        btn_add = tk.Button(self.frm_img_buttons, text="Bilder hinzufügen", command=self.add_images)
        btn_add.pack(side="left")
        btn_rem = tk.Button(self.frm_img_buttons, text="Bild entfernen", command=self.remove_image)
        btn_rem.pack(side="left", padx=(10, 0))
        # Darunter: Scrollbare Bildnamenliste (Treeview)
        self.frm_tree = tk.Frame(self.frm_images)
        self.frm_tree.grid(row=1, column=0, sticky="nsew", pady=(5,0))
        self.frm_images.rowconfigure(1, weight=1)
        self.frm_images.columnconfigure(0, weight=1)
        self.tree = ttk.Treeview(self.frm_tree, columns=("dim"), show="tree", height=5)
        self.tree.heading("#0", text="Dateiname")
        self.tree.heading("dim", text="Abmessungen")
        self.tree.column("dim", anchor="e")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.frm_tree.rowconfigure(0, weight=1)
        self.frm_tree.columnconfigure(0, weight=1)
        scr = ttk.Scrollbar(self.frm_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scr.set)
        scr.grid(row=0, column=1, sticky="ns")
        
        # --- 2. Parameter-Einstellungen ---
        self.frm_params = tk.Frame(self)
        self.frm_params.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        tk.Label(self.frm_params, text="Streifenrichtung:").grid(row=0, column=0, sticky="w")
        tk.Radiobutton(self.frm_params, text="vertikal", variable=self.stripe_dir, value="vertikal",
                       command=self.param_changed).grid(row=0, column=1, sticky="w")
        tk.Radiobutton(self.frm_params, text="horizontal", variable=self.stripe_dir, value="horizontal",
                       command=self.param_changed).grid(row=0, column=2, sticky="w")
        tk.Label(self.frm_params, text="LPI:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.frm_params, textvariable=self.lpi_var, width=7,
                 validate="key", validatecommand=vcmd)\
            .grid(row=1, column=1, columnspan=2, sticky="w")
        self.lbl_width = tk.Label(self.frm_params, text="Bildbreite (cm/inch):")
        self.lbl_width.grid(row=2, column=0, sticky="w")
        tk.Entry(self.frm_params, textvariable=self.width_cm, width=7,
                 validate="key", validatecommand=vcmd)\
            .grid(row=2, column=1, sticky="w")
        et_width_inch = tk.Entry(self.frm_params, textvariable=self.width_inch, width=7,
                                 validate="key", validatecommand=vcmd)
        et_width_inch.grid(row=2, column=2, sticky="w")
        et_width_inch.bind("<KeyRelease>", self.on_width_inch)
        self.lbl_height = tk.Label(self.frm_params, text="optional: Bildhöhe (cm/inch):")
        self.lbl_height.grid(row=3, column=0, sticky="w")
        tk.Entry(self.frm_params, textvariable=self.height_cm, width=7,
                 validate="key", validatecommand=vcmd)\
            .grid(row=3, column=1, sticky="w")
        et_height_inch = tk.Entry(self.frm_params, textvariable=self.height_inch, width=7,
                                  validate="key", validatecommand=vcmd)
        et_height_inch.grid(row=3, column=2, sticky="w")
        et_height_inch.bind("<KeyRelease>", self.on_height_inch)
        tk.Label(self.frm_params, text="PPI:").grid(row=4, column=0, sticky="w")
        tk.Entry(self.frm_params, textvariable=self.ppi_var, width=7,
                 validate="key", validatecommand=vcmd)\
            .grid(row=4, column=1, columnspan=2, sticky="w")
        for var in (self.lpi_var, self.ppi_var, self.width_cm, self.height_cm):
            var.trace_add("write", lambda *args: self.param_changed())
        
        # --- 3. Infobereich ---
        self.txt_info = tk.Text(self, height=9)
        self.txt_info.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.txt_info.tag_config("error", foreground="red")
        
        # --- 4. Bild generieren ---
        btn_generate = tk.Button(self, text="Bild generieren", command=self.generate_image)
        btn_generate.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_width_inch(self, event):
        self.width_cm.set("")
        self.param_changed()

    def on_height_inch(self, event):
        self.height_cm.set("")
        self.param_changed()

    def add_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Bilder", "*.png;*.jpg;*.jpeg;*.bmp")])
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
        if self.stripe_dir.get() == "vertikal":
            self.lbl_width.config(text="Bildbreite (cm/inch):")
            self.lbl_height.config(text="optional: Bildhöhe (cm/inch):")
        else:
            self.lbl_height.config(text="Bildhöhe (cm/inch):")
            self.lbl_width.config(text="optional: Bildbreite (cm/inch):")
        if self.width_cm.get():
            try:
                cm = float(self.width_cm.get().replace(",", "."))
                self.width_inch.set(str(round(cm / 2.54, 3)))
            except:
                pass
        if self.height_cm.get():
            try:
                cm = float(self.height_cm.get().replace(",", "."))
                self.height_inch.set(str(round(cm / 2.54, 3)))
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
            self.txt_info.insert(tk.END, "LPI und PPI müssen > 0 sein", "error")
            return
        num_images = len(self.image_list)
        dirc = self.stripe_dir.get()
        stretching = False
        if dirc == "vertikal":
            try:
                width_in = float(self.width_inch.get().replace(",", "."))
                if width_in <= 0:
                    raise ValueError
            except:
                self.txt_info.insert(tk.END, "Bildbreite (inch) darf nicht leer sein", "error")
                return
            Bildendbreite = round(PPI * width_in)
            if self.height_inch.get().strip() != "":
                try:
                    h_in = float(self.height_inch.get().replace(",", "."))
                    if h_in <= 0:
                        raise ValueError
                    Bildendhöhe = round(Bildendbreite * (h_in / width_in))
                    stretching = True
                except:
                    self.txt_info.insert(tk.END, "Ungültiger Wert für Bildhöhe (inch)", "error")
                    return
            else:
                first = self.image_list[0]
                Bildendhöhe = round(Bildendbreite * (first["height"] / first["width"]))
            Q = math.ceil(Bildendbreite / num_images)
            K = Bildendhöhe
            true_width = Bildendbreite / PPI
            true_height = Bildendhöhe / PPI
        else:
            try:
                h_in = float(self.height_inch.get().replace(",", "."))
                if h_in <= 0:
                    raise ValueError
            except:
                self.txt_info.insert(tk.END, "Bildhöhe (inch) darf nicht leer sein", "error")
                return
            Bildendhöhe = round(PPI * h_in)
            if self.width_inch.get().strip() != "":
                try:
                    width_in = float(self.width_inch.get().replace(",", "."))
                    if width_in <= 0:
                        raise ValueError
                    Bildendbreite = round(Bildendhöhe * (width_in / h_in))
                    stretching = True
                except:
                    self.txt_info.insert(tk.END, "Ungültiger Wert für Bildbreite (inch)", "error")
                    return
            else:
                first = self.image_list[0]
                Bildendbreite = round(Bildendhöhe * (first["width"] / first["height"]))
            Q = math.ceil(Bildendhöhe / num_images)
            K = Bildendbreite
            true_height = Bildendhöhe / PPI
            true_width = Bildendbreite / PPI
        Streifenbreite = max(round(PPI / (num_images * LPI)), 1)
        wahrerLPI = PPI / (num_images * Streifenbreite)
        info = (f"Anzahl der Bilder: {num_images}\n"
                f"Bildendbreite (px): {Bildendbreite}\n"
                f"Bildendhöhe (px): {Bildendhöhe}\n"
                f"wahre Bildbreite (inch): {true_width:.4f}\n"
                f"wahre Bildhöhe (inch): {true_height:.4f}\n"
                f"Streckung: {'aktiv' if stretching else 'ausgeblendet'}\n"
                f"Streifenbreite (px): {Streifenbreite}\n"
                f"wahrer LPI-Wert: {wahrerLPI:.2f}\n")
        self.calc = {"dir": dirc, "Bildendbreite": Bildendbreite, "Bildendhöhe": Bildendhöhe,
                     "Q": Q, "K": K, "Streifenbreite": Streifenbreite}
        self.txt_info.insert(tk.END, info)

    def on_resize(self, event):
        if self.tree:
            new_width = self.frm_tree.winfo_width()
            if new_width > 0:
                # Abmessungen Bildnamenlisteaufteilung
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
        BB = self.calc["Bildendbreite"]
        BH = self.calc["Bildendhöhe"]
        Q = self.calc["Q"]
        K = self.calc["K"]
        Streifenbreite = self.calc["Streifenbreite"]
        num_images = len(self.image_list)
        imgs = []
        for item in self.image_list:
            try:
                im = Image.open(item["path"])
                if dirc == "horizontal":
                    im = im.rotate(90, expand=True)
                im = im.resize((Q, K))
                imgs.append(im)
            except:
                continue
        if not imgs:
            return
        if dirc == "vertikal":
            final = Image.new("RGB", (BB, BH))
            pointers = [0] * num_images
            x = 0
            while x < BB:
                for i in range(num_images):
                    if x >= BB:
                        break
                    if pointers[i] < Q:
                        sw = min(Streifenbreite, Q - pointers[i], BB - x)
                        stripe = imgs[i].crop((pointers[i], 0, pointers[i] + sw, K))
                        final.paste(stripe, (x, 0))
                        pointers[i] += sw
                        x += sw
        else:
            final = Image.new("RGB", (BB, BH))
            pointers = [0] * num_images
            y = 0
            while y < BH:
                for i in range(num_images):
                    if y >= BH:
                        break
                    if pointers[i] < Q:
                        sh = min(Streifenbreite, Q - pointers[i], BH - y)
                        stripe = imgs[i].crop((0, pointers[i], K, pointers[i] + sh))
                        final.paste(stripe, (0, y))
                        pointers[i] += sh
                        y += sh
            final = final.rotate(-90, expand=True)
        try:
            final.save(save_path)
        except Exception as e:
            self.txt_info.insert(tk.END, f"Speicherfehler: {e}", "error")

if __name__ == "__main__":
    app = LenticularMaker()
    app.mainloop()
