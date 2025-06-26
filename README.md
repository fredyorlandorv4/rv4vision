
# 🧾 API de Procesamiento de PDFs a Imágenes OCR

Esta API basada en **FastAPI** permite:

- 📄 Recibir archivos PDF mediante un endpoint.
- 🖼 Convertir cada página del PDF a una imagen `.jpg`.
- 🧠 Detectar y corregir la orientación de cada imagen usando **Tesseract OCR**.
- 📤 Retornar las imágenes codificadas en formato **Base64**.

---

## 🚀 Tecnologías Utilizadas

- Python 3.8+
- FastAPI
- OpenCV (`cv2`)
- Tesseract OCR
- PDF2Image
- Imutils

---

## ⚙️ Instalación

```bash
pip install fastapi uvicorn opencv-python pdf2image pytesseract imutils python-multipart
```

Además, necesitas:

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)  
  Asegúrate de configurar correctamente la ruta:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

- [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)  
  Y su ruta para `pdf2image`:
  ```python
  poppler_path=r'C:\Program Files\poppler-24.08.0\Library\bin'
  ```

---

## 🧩 Endpoints

### `POST /files/{id_customer}`

**Descripción:**  
Recibe uno o más archivos PDF, los convierte en imágenes, corrige su orientación y devuelve las imágenes codificadas en Base64.

**Parámetros:**
- `id_customer` (path): Identificador del cliente.

**Body (multipart/form-data):**
- `files`: Lista de archivos `.pdf`

**Respuesta:**

```json
{
  "images": [
    "base64_string_1",
    "base64_string_2",
    ...
  ]
}
```

**Ejemplo con curl:**

```bash
curl -X POST "http://localhost:8000/files/cliente123"   -F "files=@/ruta/al/archivo.pdf"
```

---

## 🛠 Funciones Principales

### `file_to_base64(file_path: str) -> str | None`
Convierte un archivo a una cadena en Base64.

---

### `image_orientation_corrector(image_path: str) -> None`
Corrige la orientación de la imagen usando OCR (`image_to_osd`).

---

### `convertPDFToImages(path_file: str) -> List[str]`
Convierte un archivo PDF en imágenes `.jpg`, corrige la orientación y devuelve la lista de rutas.

---

## 🗂 Estructura del Proyecto

```
.
├── cliente123/
│   └── nombre_archivo.pdf
│   └── nombre_archivo/
│       └── img/
│           ├── page0.jpg
│           ├── page1.jpg
│           └── ...
```

---

## ✅ Consideraciones

- El OCR utiliza el idioma español (`lang="spa"`). Puedes cambiarlo según sea necesario.
- Las imágenes corregidas sobrescriben las originales. Si deseas conservar ambas versiones, modifica `image_orientation_corrector`.
- Asegúrate de manejar adecuadamente los permisos de escritura al guardar archivos en el servidor.

---

## 🏁 Ejecución del Servidor

```bash
uvicorn main:app --reload
```

Asegúrate de que `main.py` sea el nombre de tu archivo principal (ajusta si es diferente).

---

