import tkinter as tk
from tkinter import messagebox, ttk
from config import countries
from data_handler import load_from_json, save_to_json
from data_extraction import extract_stadium_info

def treeview_sort_column(tv, col, reverse):
    """Ordenar las columnas del Treeview."""
    data_type = str
    if col == 'Capacity':
        data_type = int
    l = [(data_type(tv.set(k, col).replace(',', '')), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

def start_interface():
    """Iniciar la interfaz gráfica."""
    def on_submit():
        source = source_var.get()
        country = combo_country.get()
        stadium_name = entry_stadium_name.get()

        if source == 'web':
            country_id = countries[country]
            stadium_data = extract_stadium_info(country_id, stadium_name)
            save_to_json(country, stadium_data)
        elif source == 'db':
            data = load_from_json()
            if data is None or country not in data:
                messagebox.showerror("Error", "No se encontró información en la base de datos local.")
                return
            stadium_data = data[country]

        for item in tree.get_children():
            tree.delete(item)
        for stadium in stadium_data:
            if not stadium_name or stadium_name.lower() in stadium['stadium'].lower():
                tree.insert("", "end", values=(stadium['stadium'], stadium['capacity'], stadium['city']))
    
    root = tk.Tk()
    root.title("Consulta de Estadios")

    tk.Label(root, text="Seleccionar País:").grid(row=0, column=0, padx=10, pady=10)
    combo_country = ttk.Combobox(root, values=list(countries.keys()))
    combo_country.grid(row=0, column=1, padx=10, pady=10)
    combo_country.set("Colombia")  # Establecer Colombia como selección predeterminada

    tk.Label(root, text="Nombre del Estadio (opcional):").grid(row=1, column=0, padx=10, pady=10)
    entry_stadium_name = tk.Entry(root)
    entry_stadium_name.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Fuente de Datos:").grid(row=2, column=0, padx=10, pady=10)
    source_var = tk.StringVar(value="web")
    tk.Radiobutton(root, text="Web", variable=source_var, value="web").grid(row=2, column=1, padx=10, pady=10, sticky='w')
    tk.Radiobutton(root, text="Base de Datos", variable=source_var, value="db").grid(row=2, column=1, padx=10, pady=10, sticky='e')

    tk.Button(root, text="Consultar", command=on_submit).grid(row=3, columnspan=2, pady=20)

    columns = ('Stadium', 'Capacity', 'City')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
    tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_interface()
