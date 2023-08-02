import tempfile
import docx2pdf
import citeproc
from citeproc.source.json import CiteProcJSON


def convert_docx_to_pdf(docx_file):
    """Converts a DOCX file to PDF format."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_pdf:
        # Convert DOCX to temporary PDF file
        docx2pdf.convert(docx_file, tmp_pdf.name)
        # Read the converted PDF file
        with open(tmp_pdf.name, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
    return pdf_data
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc.source.json import CiteProcJSON

def generate_paper_citation(paper, style='apa'):
    """Generates a citation for a research paper."""
    # Create a citation item with paper metadata
    item = {
        'id': paper.slug,
        'title': paper.title,
        'author': [{'family': author.username} for author in paper.authors.all()],
        'issued': {'year': str(paper.publication_date.year)}
    }

    # Create a citation style and register the citation item
    bib_source = CiteProcJSON([item])
    citation_style = CitationStylesStyle(style, validate=False)
    bibliography = CitationStylesBibliography(citation_style, bib_source)

    # Process the citation and return the formatted result
    citation = bibliography[0]
    citation_text = citation.text().replace('\n', ' ')
    return citation_text
