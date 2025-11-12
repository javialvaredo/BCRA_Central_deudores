import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import warnings
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import SSLError, RequestException

# Omitir advertencias por verify=False (solo para este uso controlado)
warnings.simplefilter('ignore', InsecureRequestWarning)


class CentralDeDeudoresApp:
    BASE_URL = "https://api.bcra.gob.ar/centraldedeudores/v1.0"

    def __init__(self, root):
        self.root = root
        self.root.title("Consulta Central de Deudores - BCRA")
        self.root.geometry("700x520")

        ttk.Label(root, text="Ingrese CUIT / CUIL / CDI:", font=("Arial", 11)).pack(pady=10)

        self.entry_id = ttk.Entry(root, width=35)
        self.entry_id.pack(pady=5)

        frame_botones = ttk.Frame(root)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Deudas actuales", command=self.consultar_deudas).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botones, text="Deudas históricas", command=self.consultar_historicas).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botones, text="Cheques rechazados", command=self.consultar_cheques).grid(row=0, column=2, padx=5)

        self.result = tk.Text(root, width=90, height=22, wrap="word", font=("Consolas", 9))
        self.result.pack(padx=10, pady=10)

        # sesión estándar (maneja reintentos automáticos)
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3)
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def consultar_deudas(self):
        self._consultar("Deudas")

    def consultar_historicas(self):
        self._consultar("Deudas/Historicas")

    def consultar_cheques(self):
        self._consultar("Deudas/ChequesRechazados")

    def _consultar(self, endpoint):
        identificacion = self.entry_id.get().strip()
        if not identificacion.isdigit() or len(identificacion) != 11:
            messagebox.showwarning("Error", "Ingrese un CUIT/CUIL válido de 11 dígitos.")
            return

        url = f"{self.BASE_URL}/{endpoint}/{identificacion}"
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, f"Consultando {url}...\n\n")

        try:
            # Intento normal (verificación SSL)
            r = self.session.get(url, timeout=10)
            if r.status_code == 404:
                self.result.insert(tk.END, "⚠️ No se encontraron datos para este CUIT.")
                return
            r.raise_for_status()
            data = r.json()
            self._mostrar_datos(data)
            return

        except SSLError:
            # Reintenta sin verificación SSL (la pagina BCRA da error)
            r = self.session.get(url, timeout=10, verify=False)
            if r.status_code == 404:
                self.result.insert(tk.END, "⚠️ No se encontraron datos para este CUIT.")
                return
            r.raise_for_status()
            data = r.json()
            self._mostrar_datos(data)
            return

        except RequestException as e:
            self.result.insert(tk.END, f"❌ Error al consultar la API:\n{e}")

    def _mostrar_datos(self, data):
        """Muestra los datos de forma legible (sin formato JSON) y omite valores booleanos."""
        texto = ""

        def formatear(item, nivel=0):
            indent = "  " * nivel
            if isinstance(item, dict):
                for k, v in item.items():
                    # 🔹 Ignorar valores booleanos
                    if isinstance(v, bool):
                        continue
                    if isinstance(v, (dict, list)):
                        texto_local.append(f"{indent}{k}:")
                        formatear(v, nivel + 1)
                    else:
                        texto_local.append(f"{indent}{k}: {v}")
            elif isinstance(item, list):
                for i, v in enumerate(item, start=1):
                    texto_local.append(f"{indent}- Elemento {i}:")
                    formatear(v, nivel + 1)
            else:
                # 🔹 Ignorar valores booleanos sueltos también
                if isinstance(item, bool):
                    return
                texto_local.append(f"{indent}{item}")

        texto_local = []
        formatear(data)
        texto = "\n".join(texto_local)

        if not texto.strip():
            texto = "⚠️ No se encontraron datos para mostrar."

        self.result.insert(tk.END, texto.strip())




if __name__ == "__main__":
    root = tk.Tk()
    app = CentralDeDeudoresApp(root)
    root.mainloop()
