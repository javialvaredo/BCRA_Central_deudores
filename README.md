# 🏦 Central de Deudores - BCRA (Interfaz Tkinter)

Aplicación de escritorio en **Python** con **Tkinter** para consultar información de la **Central de Deudores del BCRA** mediante su API pública.

Permite consultar:
- 💰 Deudas actuales  
- 📜 Deudas históricas  
- 🧾 Cheques rechazados  

---

## 🚀 Requisitos

- Python 3.8 o superior (recomendado 3.10+)
- Conexión a Internet
- Paquetes:
  - `requests`
  - `urllib3`

---

## ⚙️ Instalación

1. Cloná este repositorio o copiá los archivos en una carpeta local:

   ```bash
   git clone https://github.com/tuusuario/central-de-deudores-bcra.git
   cd central-de-deudores-bcra
   git clone https://github.com/tuusuario/BRCA_Api.git
  cd central_deudores_BCRA
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt




🧩 Notas técnicas

El programa intenta primero una conexión segura (SSL).

Si el certificado del BCRA no puede validarse, vuelve a intentar sin verificación SSL, mostrando los resultados igualmente.

Los datos se muestran formateados de forma legible, sin formato JSON.

📄 Fuente de datos

API oficial del BCRA:
https://api.bcra.gob.ar/centraldedeudores/v1.0

🧑‍💻 Autor

Desarrollado por Javier Alvaredo
📅 Versión inicial: noviembre 2025
💬 Licencia: MIT