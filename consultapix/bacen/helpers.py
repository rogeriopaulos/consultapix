import io
import logging

import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

logger = logging.getLogger(__name__)


def camelcase_to_snake_case(data: dict) -> dict:
    """
    Convert camelCase keys in a dictionary to snake_case.
    """

    def camel_to_snake(name: str) -> str:
        return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip(
            "_",
        )

    return {camel_to_snake(k): v for k, v in data.items()}


def has_object(classmodel, **kwargs) -> bool:
    try:
        classmodel.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return False
    else:
        return True


class BacenRequestApi:
    def __init__(self):
        self.base_url = settings.BACEN_API_DICT_BASEURL
        self.informes_url = settings.BACEN_API_INFORMES

        self.username = settings.BACEN_API_DICT_USER
        self.password = settings.BACEN_API_DICT_PASSWORD

        self.headers = {
            "Accept": "application/json",
        }

        self.pix_endpoint = "/consultar-vinculos-pix"

        self.TIMEOUT_REQUEST = 60  # seconds

    def _execute_pix_request(self, payload: dict) -> dict:
        url = f"{self.base_url}{self.pix_endpoint}"
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=payload,
                auth=(self.username, self.password),
                timeout=self.TIMEOUT_REQUEST,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

        return response.json()

    def get_pix_by_cpf_cnpj(self, cpf: str, reason: str) -> dict:
        payload = {"cpfCnpj": cpf, "motivo": reason}
        return self._execute_pix_request(payload)

    def get_pix_by_key(self, key: str, reason: str) -> dict:
        payload = {"chave": key, "motivo": reason}
        return self._execute_pix_request(payload)

    def get_bank_info(self, cnpj: str) -> dict:
        """
        Obtém informações bancárias de um CNPJ usando a API de Informes do Bacen.
        """
        try:
            response = requests.get(
                f"{self.informes_url}/pessoasJuridicas",
                params={"cnpj": cnpj},
                timeout=self.TIMEOUT_REQUEST,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            logger.exception("Erro ao obter informações do banco")
            return {}

        return response.json()


class PixReportGenerator:
    def __init__(self):
        self.buffer = io.BytesIO()
        self.pagesize = landscape(A4)
        self.width, self.height = self.pagesize
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        self.bacen_api = BacenRequestApi()
        self.banks_info = {}

    def setup_styles(self):
        """Configura os estilos de texto para o documento"""
        self.styles.add(
            ParagraphStyle(
                name="Header",
                fontName="Helvetica-Bold",
                fontSize=12,
                alignment=1,  # Centralizado
                spaceAfter=2,
            ),
        )

        self.styles.add(
            ParagraphStyle(
                name="SubHeader",
                fontName="Helvetica-Bold",
                fontSize=10,
                alignment=1,  # Centralizado
                spaceAfter=2,
            ),
        )

        self.styles.add(
            ParagraphStyle(
                name="ChaveTitle",
                fontName="Helvetica-Bold",
                fontSize=9,
                alignment=0,  # Esquerda
                spaceAfter=2,
            ),
        )

        self.styles["Normal"].fontName = "Helvetica"
        self.styles["Normal"].fontSize = 9

    def create_header(self, canvas, doc):
        """Cria o cabeçalho em cada página"""
        canvas.saveState()

        # Cabeçalho
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawCentredString(
            self.width / 2,
            self.height - 20,
            "POLÍCIA CIVIL DO PIAUÍ",
        )
        canvas.drawCentredString(
            self.width / 2,
            self.height - 35,
            "DIRETORIA DE INTELIGÊNCIA DA POLÍCIA CIVIL",
        )
        canvas.drawCentredString(
            self.width / 2,
            self.height - 50,
            "LABORATÓRIO DE TECNOLOGIA CONTRA LAVAGEM DE DINHEIRO",
        )
        canvas.drawCentredString(
            self.width / 2,
            self.height - 65,
            "RELAÇÃO DE CHAVES PIX - DETALHADA",
        )

        # Linha horizontal
        canvas.setStrokeColor(colors.black)
        canvas.line(30, self.height - 75, self.width - 30, self.height - 75)

        # Rodapé
        canvas.setFont("Helvetica", 8)
        canvas.drawCentredString(self.width / 2, 15, "CONFIDENCIAL")
        canvas.drawRightString(self.width - 30, 15, f"{doc.page}/XX")

        canvas.restoreState()

    def generate_report(self, requisicao_data, chaves_pix):
        """Gera o relatório completo"""
        left_margin = 30
        right_margin = 30
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=self.pagesize,
            leftMargin=left_margin,
            rightMargin=right_margin,
            topMargin=80,
            bottomMargin=30,
        )

        story = []

        busca = (
            f"{requisicao_data['tipo_requisicao']}: {requisicao_data['termo_busca']}"
        )
        story.append(Paragraph(busca, self.styles["ChaveTitle"]))
        story.append(Spacer(1, 5))

        # Largura total disponível para a tabela
        total_width = self.width - left_margin - right_margin
        # Proporção das colunas (soma deve ser 1.0)
        col_proportions = [0.10, 0.10, 0.18, 0.13, 0.18, 0.23, 0.08]
        col_widths = [total_width * p for p in col_proportions]

        for chave in chaves_pix:
            # Título da chave
            chave_title = f"Chave: {chave['chave']} - {chave['status']}"
            story.append(Paragraph(chave_title, self.styles["ChaveTitle"]))
            story.append(Spacer(1, 5))

            # Tabela de eventos
            data = [
                [
                    Paragraph("Data", self.styles["Normal"]),
                    Paragraph("Evento", self.styles["Normal"]),
                    Paragraph("Motivo", self.styles["Normal"]),
                    Paragraph("CPF/CNPJ", self.styles["Normal"]),
                    Paragraph("Nome", self.styles["Normal"]),
                    Paragraph("Banco", self.styles["Normal"]),
                    Paragraph("Abertura Conta", self.styles["Normal"]),
                ],
            ]

            for evento in chave["eventos_vinculo"]:
                banco = "Dados bancários não disponíveis"
                if chave.get("banco"):
                    banco = self.format_bank_cell(evento, chave.get("banco"))

                data_evento = "N/A"
                if evento.get("data_evento"):
                    data_evento = evento.get("data_evento").strftime(
                        "%d/%m/%Y %H:%M:%S",
                    )

                data_abertura_conta = "N/A"
                if evento.get("data_abertura_conta"):
                    data_abertura_conta = evento.get("data_abertura_conta").strftime(
                        "%d/%m/%Y",
                    )

                row = [
                    Paragraph(data_evento, self.styles["Normal"]),
                    Paragraph(
                        str(evento.get("tipo_evento", "")),
                        self.styles["Normal"],
                    ),
                    Paragraph(
                        str(evento.get("motivo_evento", "")),
                        self.styles["Normal"],
                    ),
                    Paragraph(str(evento.get("cpf_cnpj", "")), self.styles["Normal"]),
                    Paragraph(
                        str(evento.get("nome_proprietario", "")),
                        self.styles["Normal"],
                    ),
                    Paragraph(banco, self.styles["Normal"]),
                    Paragraph(data_abertura_conta, self.styles["Normal"]),
                ]
                data.append(row)

            # Criar tabela
            table = Table(data, colWidths=col_widths)

            # Estilo da tabela
            table_style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
                ],
            )

            table.setStyle(table_style)
            story.append(table)
            story.append(Spacer(1, 10))

        # Construir o documento
        doc.build(
            story,
            onFirstPage=self.create_header,
            onLaterPages=self.create_header,
        )
        self.buffer.seek(0)
        return self.buffer

    def format_bank_cell(self, event: dict, bank: str) -> str:
        agencia = event.get("agencia", "N/A")
        conta = event.get("numero_conta", "N/A")
        tipo_conta = event.get("tipo_conta", "N/A")

        return f"{bank}\nAgência: {agencia}\nConta: {conta}\nTipo: {tipo_conta}"
