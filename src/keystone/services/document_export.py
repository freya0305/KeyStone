"""Document export service for resume generation."""

from typing import Literal

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
except ImportError:
    A4 = None
    getSampleStyleSheet = None

try:
    from docx import Document as DocxDocument
    from docx.shared import Pt, RGBColor
except ImportError:
    DocxDocument = None


def generate_pdf(context: dict) -> bytes:
    """Generate a PDF resume with suggestions applied."""
    if A4 is None:
        raise RuntimeError(
            "reportlab is required for PDF export. "
            "Install with: pip install reportlab"
        )

    buffer = __import__("io").BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles["Title"]
    story.append(Paragraph(context.get("job_title", "Resume"), title_style))
    story.append(Spacer(1, 5 * mm))

    # Company
    if context.get("company"):
        story.append(Paragraph(f"<i>{context['company']}</i>", styles["Normal"]))
        story.append(Spacer(1, 3 * mm))

    # Skills
    skills = context.get("skills", [])
    if skills:
        story.append(Paragraph("Skills: " + ", ".join(skills), styles["Normal"]))
        story.append(Spacer(1, 5 * mm))

    # Suggestions
    story.append(Paragraph("Resume Suggestions", styles["Heading2"]))
    story.append(Spacer(1, 3 * mm))

    for suggestion in context.get("suggestions", []):
        level = suggestion.get("match_level", "")
        level_color = {
            "strong": "#2e7d32",
            "transferable": "#1976d2",
            "addressable": "#f57c00",
            "fundamental": "#c62828",
        }.get(level, "#666666")

        story.append(
            Paragraph(
                f"<b>[{level.upper()}]</b> {suggestion.get('section', '')}",
                ParagraphStyle(
                    "Level",
                    textColor=__import__("reportlab.lib.colors").HexColor(level_color),
                    fontName="Helvetica-Bold",
                    fontSize=10,
                ),
            )
        )
        if suggestion.get("original_text"):
            story.append(
                Paragraph(
                    f"<b>Original:</b> {suggestion['original_text']}",
                    styles["Normal"],
                )
            )
        if suggestion.get("suggested_text"):
            story.append(
                Paragraph(
                    f"<b>Suggested:</b> {suggestion['suggested_text']}",
                    ParagraphStyle(
                        "Suggested",
                        textColor=__import__("reportlab.lib.colors").HexColor("#1b5e20"),
                        fontName="Helvetica",
                        fontSize=10,
                    ),
                )
            )
        story.append(Spacer(1, 3 * mm))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


def generate_docx(context: dict) -> bytes:
    """Generate a DOCX resume with suggestions applied."""
    if DocxDocument is None:
        raise RuntimeError(
            "python-docx is required for DOCX export. "
            "Install with: pip install python-docx"
        )

    doc = DocxDocument()

    # Title
    title = doc.add_heading(context.get("job_title", "Resume"), 0)

    # Company
    if context.get("company"):
        doc.add_paragraph(context["company"]).runs[0].italic = True

    # Skills
    skills = context.get("skills", [])
    if skills:
        p = doc.add_paragraph()
        p.add_run("Skills: ").bold = True
        p.add_run(", ".join(skills))

    # Suggestions
    doc.add_heading("Resume Suggestions", level=1)

    for suggestion in context.get("suggestions", []):
        level = suggestion.get("match_level", "")
        level_colors = {
            "strong": RGBColor(0x2e, 0x7d, 0x32),
            "transferable": RGBColor(0x19, 0x76, 0xd2),
            "addressable": RGBColor(0xf5, 0x7c, 0x00),
            "fundamental": RGBColor(0xc6, 0x28, 0x28),
        }
        color = level_colors.get(level, RGBColor(0x66, 0x66, 0x66))

        p = doc.add_paragraph()
        run = p.add_run(f"[{level.upper()}] ")
        run.bold = True
        run.font.color.rgb = color
        run2 = p.add_run(suggestion.get("section", ""))
        run2.font.color.rgb = color

        if suggestion.get("original_text"):
            p2 = doc.add_paragraph()
            p2.add_run("Original: ").bold = True
            p2.add_run(suggestion["original_text"])

        if suggestion.get("suggested_text"):
            p3 = doc.add_paragraph()
            p3.add_run("Suggested: ").bold = True
            run_s = p3.add_run(suggestion["suggested_text"])
            run_s.font.color.rgb = RGBColor(0x1b, 0x5e, 0x20)

    buffer = __import__("io").BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.read()
