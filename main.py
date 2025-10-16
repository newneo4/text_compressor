import tkinter as tk
from tkinter import filedialog, messagebox
from huffman import huffman_compress, huffman_decompress

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

def compress_file():
    path = entry_file.get()
    if not path:
        messagebox.showwarning("Advertencia", "Selecciona un archivo de texto primero.")
        return

    output_path = path.replace(".txt", ".bin")
    orig_size, comp_size = huffman_compress(path, output_path)
    messagebox.showinfo("Compresión completada",
                        f"Archivo comprimido: {output_path}\n"
                        f"Tamaño original: {orig_size} bytes\n"
                        f"Tamaño comprimido: {comp_size} bytes\n")

def decompress_file():
    file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
    if not file_path:
        return
    output_path = file_path.replace(".bin", "_restored.txt")
    comp_size, decomp_size = huffman_decompress(file_path, output_path)
    messagebox.showinfo("Descompresión completada",
                        f"Archivo restaurado: {output_path}\n"
                        f"Tamaño comprimido: {comp_size} bytes\n"
                        f"Tamaño descomprimido: {decomp_size} bytes")

root = tk.Tk()
root.title("Compresor de archivos de texto")
root.geometry("420x200")

tk.Label(root, text="Archivo de texto:").pack(pady=5)
entry_file = tk.Entry(root, width=50)
entry_file.pack(pady=5)

tk.Button(root, text="Seleccionar archivo", command=select_file).pack(pady=5)
tk.Button(root, text="Comprimir", bg="#4CAF50", fg="white", command=compress_file).pack(pady=5)
tk.Button(root, text="Descomprimir", bg="#2196F3", fg="white", command=decompress_file).pack(pady=5)

root.mainloop()
