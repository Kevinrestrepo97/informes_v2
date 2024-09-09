import pandas as pd
from docx import Document
import locale
from docxcompose.composer import Composer
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from medir_tiempo import medir_tiempo

def combinar_plantillas(doc_paths, output_path):
    if not doc_paths:
        raise ValueError("Se debe proporcionar al menos un documento para combinar.")
    
    # Cargar el primer documento y aplicar cambios de fuente
    master = Document(doc_paths[0])
    composer = Composer(master)
    
    # Añadir los documentos restantes
    for doc_path in doc_paths[1:]:
        doc_to_append = Document(doc_path)
        composer.append(doc_to_append)
    
    # Aplicar cambios de fuente y márgenes al documento combinado
    final_doc = composer.doc
    
    # Guardar el documento combinado
    final_doc.save(output_path)
    