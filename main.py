import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from datetime import datetime

def gerar_nota(csv_path, pdf_path):

    df = pd.read_csv(csv_path)
    df["subtotal"] = df["quantidade"] * df["preco_unitario"]
    total_geral = df["subtotal"].sum()

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elementos = []
    styles = getSampleStyleSheet()

    numero_nota = "0001"
    data_atual = datetime.now().strftime("%d/%m/%Y")

    elementos.append(Paragraph("<b>NOTA FISCAL</b>", styles["Title"]))
    elementos.append(Spacer(1, 0.2 * inch))

    elementos.append(Paragraph(f"Nº: {numero_nota}", styles["Normal"]))
    elementos.append(Paragraph(f"Data: {data_atual}", styles["Normal"]))
    elementos.append(Spacer(1, 0.3 * inch))

    elementos.append(Paragraph("<b>Empresa:</b> Minha Empresa LTDA", styles["Normal"]))
    elementos.append(Paragraph("<b>CNPJ:</b> 00.000.000/0001-00", styles["Normal"]))
    elementos.append(Spacer(1, 0.3 * inch))

    dados = [["Produto", "Qtd", "Preço Unit.", "Subtotal"]]

    for _, row in df.iterrows():
        dados.append([
            row["produto"],
            row["quantidade"],
            f"R$ {row['preco_unitario']:.2f}",
            f"R$ {row['subtotal']:.2f}"
        ])

    tabela = Table(dados, colWidths=[220, 50, 100, 100])

    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))

    for i in range(1, len(dados)):
        if i % 2 == 0:
            tabela.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, i), (-1, i), colors.lightgrey)
                ])
            )

    elementos.append(tabela)
    elementos.append(Spacer(1, 0.3 * inch))

    total_table = Table(
        [["TOTAL GERAL:", f"R$ {total_geral:.2f}"]],
        colWidths=[370, 100]
    )

    total_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elementos.append(total_table)
    elementos.append(Spacer(1, 0.5 * inch))

    elementos.append(Paragraph("Documento gerado automaticamente.", styles["Italic"]))

    doc.build(elementos)
    print("Nota fiscal gerada com sucesso!")

if __name__ == "__main__":
    gerar_nota("dados.csv", "nota_fiscal.pdf")