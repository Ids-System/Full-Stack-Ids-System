import io
from datetime import datetime
from sqlalchemy import func
from db.database import SessionLocal
from models.Alerts import Alerts
from models.Attackips import AttackIP
from models.Attacks import Attacks
from models.Blocked_ips import Blockedips

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically calculate the total page count
    and draw consistent headers, footers, and page numbers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1E293B")) 
        self.drawString(54, 755, "INTRUSION DETECTION SYSTEM (IDS) SECURITY REPORT")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B")) 
        self.drawRightString(558, 755, "CONFIDENTIAL / INTERNAL ONLY")
        self.setLineWidth(0.75)
        self.setStrokeColor(colors.HexColor("#E2E8F0")) 
        self.line(54, 747, 558, 747)

        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#EF4444")) 
        self.drawString(54, 35, "RESTRICTED ACCESS")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B")) 
        self.drawString(160, 35, "|   Automated Security Logs Analysis")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, page_text)
        self.setLineWidth(0.75)
        self.setStrokeColor(colors.HexColor("#E2E8F0")) 
        self.line(54, 47, 558, 47)
        
        self.restoreState()


def draw_visual_bar(percentage, width=100, height=8, fill_hex="#3B82F6"):
    """
    Draws a clean, inline visual progress bar for data breakdown tables.
    """
    d = Drawing(width, height)
    
    d.add(Rect(0, 0, width, height, fillColor=colors.HexColor("#F1F5F9"), strokeColor=None))
    
    fill_w = max(1, int(width * (min(percentage, 100) / 100.0)))
    d.add(Rect(0, 0, fill_w, height, fillColor=colors.HexColor(fill_hex), strokeColor=None))
    return d


def generate_pdf_report():
    """
    Generates a beautifully formatted cybersecurity incident PDF report.
    Returns the report as an in-memory BytesIO buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=65,
        bottomMargin=65
    )

    story = []
    
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'), 
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748B'), 
        spaceAfter=15
    )
    
    section_title_style = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'), 
        fontName='Helvetica-Bold',
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )
    
    tb_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#334155') 
    )
    
    tb_bold_style = ParagraphStyle(
        'TableBodyBold',
        parent=tb_style,
        fontName='Helvetica-Bold'
    )

    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#475569'), 
        fontName='Helvetica-Bold',
        alignment=1 
    )

    card_value_style = ParagraphStyle(
        'CardValue',
        parent=styles['Normal'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'), 
        fontName='Helvetica-Bold',
        alignment=1 
    )

   
    with SessionLocal() as db:
        
        total_attacks = db.query(Attacks).count()
        total_blocked = db.query(Blockedips).count()
        
       
        sev_raw = db.query(Alerts.severity, func.count(Alerts.alert_id)).group_by(Alerts.severity).all()
        sev_counts = {r[0]: r[1] for r in sev_raw}
        high_severity = sev_counts.get("High", 0)
        med_severity = sev_counts.get("Medium", 0)
        low_severity = sev_counts.get("Low", 0)

        
        attack_types_raw = db.query(
            Attacks.attack, 
            func.count(Attacks.attack_id)
        ).group_by(Attacks.attack).order_by(func.count(Attacks.attack_id).desc()).all()

        
        protocol_raw = db.query(
            AttackIP.protocol, 
            func.count(Attacks.attack_id)
        ).join(Attacks, Attacks.ip_id == AttackIP.ip_id).group_by(AttackIP.protocol).order_by(func.count(Attacks.attack_id).desc()).all()


        recent_incidents = db.query(Alerts, Attacks, AttackIP).join(
            Attacks, Alerts.Attackid == Attacks.attack_id
        ).join(
            AttackIP, Attacks.ip_id == AttackIP.ip_id
        ).order_by(Alerts.timestamp.desc()).limit(15).all()

        
        blocked_list = db.query(Blockedips).order_by(Blockedips.Date_of_block.desc()).limit(10).all()

    
    story.append(Paragraph("INTRUSION DETECTION SYSTEM", title_style))
    story.append(Paragraph(
        f"Security Intelligence Report  |  Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}  |  Systems Admin", 
        subtitle_style
    ))
    
    
    card_table_data = [
        [
            Paragraph("TOTAL INCIDENTS", card_title_style),
            Paragraph("HIGH SEVERITY", card_title_style),
            Paragraph("BLOCKED IPS", card_title_style)
        ],
        [
            Paragraph(str(total_attacks), card_value_style),
            Paragraph(f"<font color='#EF4444'>{high_severity}</font>", card_value_style),
            Paragraph(str(total_blocked), card_value_style)
        ]
    ]
    
    card_table = Table(card_table_data, colWidths=[168, 168, 168])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(card_table)
    story.append(Spacer(1, 10))

    
    story.append(Paragraph("Threat Distributions", section_title_style))
    
    
    left_table_data = [[
        Paragraph("Attack Type", th_style), 
        Paragraph("Count", th_style), 
        Paragraph("Ratio", th_style)
    ]]
    tot_attacks_divisor = total_attacks if total_attacks > 0 else 1
    for name, count in attack_types_raw[:5]:
        pct = (count / tot_attacks_divisor) * 100
        left_table_data.append([
            Paragraph(name, tb_style),
            Paragraph(str(count), tb_style),
            draw_visual_bar(pct, width=80, fill_hex="#3B82F6")
        ])
    if len(left_table_data) == 1:
        left_table_data.append([Paragraph("No threats recorded", tb_style), Paragraph("0", tb_style), ""])

    left_table = Table(left_table_data, colWidths=[100, 44, 94])
    left_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    
    right_table_data = [[
        Paragraph("Protocol", th_style), 
        Paragraph("Count", th_style), 
        Paragraph("Ratio", th_style)
    ]]
    for proto, count in protocol_raw[:5]:
        pct = (count / tot_attacks_divisor) * 100
        right_table_data.append([
            Paragraph(proto or "Unknown", tb_style),
            Paragraph(str(count), tb_style),
            draw_visual_bar(pct, width=80, fill_hex="#0D9488")
        ])
    if len(right_table_data) == 1:
        right_table_data.append([Paragraph("No traffic logged", tb_style), Paragraph("0", tb_style), ""])

    right_table = Table(right_table_data, colWidths=[90, 44, 104])
    right_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    
    dist_layout = Table([[left_table, "", right_table]], colWidths=[238, 28, 238])
    dist_layout.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(dist_layout)
    story.append(Spacer(1, 10))

    
    story.append(Paragraph("Recent Security Alerts Log", section_title_style))
    alerts_data = [[
        Paragraph("Timestamp", th_style),
        Paragraph("Source IP", th_style),
        Paragraph("Target IP", th_style),
        Paragraph("Attack Type", th_style),
        Paragraph("Protocol/Port", th_style),
        Paragraph("Severity", th_style)
    ]]
    
    for alert, attack, ip in recent_incidents:
        
        sev = alert.severity
        if sev == "High":
            sev_text = f"<font color='#EF4444'><b>{sev}</b></font>"
        elif sev == "Medium":
            sev_text = f"<font color='#F59E0B'><b>{sev}</b></font>"
        else:
            sev_text = f"<font color='#10B981'><b>{sev}</b></font>"
            
        time_str = alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        alerts_data.append([
            Paragraph(time_str, tb_style),
            Paragraph(ip.source_ip, tb_style),
            Paragraph(ip.destination_ip, tb_style),
            Paragraph(attack.attack, tb_style),
            Paragraph(f"{ip.protocol} / {ip.port}", tb_style),
            Paragraph(sev_text, tb_bold_style)
        ])
        
    if len(alerts_data) == 1:
        alerts_data.append([Paragraph("No alerts detected", tb_style), "", "", "", "", ""])

    
    alerts_table = Table(alerts_data, colWidths=[105, 80, 80, 110, 75, 54])
    alerts_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(alerts_table)
    story.append(Spacer(1, 10))

    
    story.append(Paragraph("Currently Blocked IP Addresses", section_title_style))
    blocked_data = [[
        Paragraph("Blocked IP Address", th_style),
        Paragraph("Triggering Threat", th_style),
        Paragraph("Block Date", th_style)
    ]]
    for bip in blocked_list:
        date_str = bip.Date_of_block.strftime("%Y-%m-%d")
        blocked_data.append([
            Paragraph(bip.ip, tb_style),
            Paragraph(bip.Attack, tb_style),
            Paragraph(date_str, tb_style)
        ])
    if len(blocked_data) == 1:
        blocked_data.append([Paragraph("No IP addresses currently blacklisted.", tb_style), "", ""])

    blocked_table = Table(blocked_data, colWidths=[150, 234, 120])
    blocked_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(blocked_table)

    
    doc.build(story, canvasmaker=NumberedCanvas)
    
    buffer.seek(0)
    return buffer
