from pdf2image import convert_from_path
from PIL import Image

def rasterizar_pdf(archivo_pdf_entrada, archivo_pdf_salida, dpi=300):
    # Convertimos cada página del PDF en una imagen
    paginas = convert_from_path(archivo_pdf_entrada, dpi=dpi)
    
    # Guardamos la primera página como PDF y luego anexamos el resto
    paginas[0].save(
        archivo_pdf_salida,
        save_all=True,
        append_images=paginas[1:]
    )

if __name__ == "__main__":
    pdf_entrada = "Actividad2-CampoElectrico.pdf"  # tu PDF de entrada
    pdf_salida = "documento_rasterizado.pdf"
    rasterizar_pdf(pdf_entrada, pdf_salida)
    print(f"PDF rasterizado guardado como: {pdf_salida}")