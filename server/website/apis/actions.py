import csv, io

from datetime import datetime
from django.http import HttpResponse, FileResponse
from django.core import serializers
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta.verbose_name_plural.lower())
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response
    

class ExportJsonMixin:
    def export_as_json(modeladmin, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response
    
    
class ExportPdfMixin:
    def export_as_pdf(self, request, queryset):
        meta = self.model._meta
        model = meta.verbose_name_plural.title()
        staff = request.user.get_full_name() or request.user.username
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(Paragraph(f"{model} Report", styles["Title"]))
        elements.append(Spacer(1, 12))
        
        generated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elements.append(Paragraph(f"<b>Exported by</b>: <i>{staff}</i>", styles["Normal"]))
        elements.append(Paragraph(f"<b>Generated at</b>: <i>{generated}</i>", styles["Normal"]))
        elements.append(Spacer(1, 12))
        
        hidden_fields = dict(created_by="created_by", changed_by="changed_by", is_active="is_active")
        fields = [field.name for field in meta.fields if field.name not in hidden_fields]
        data = [fields]
        
        for obj in queryset:
            row = [str(getattr(obj, field)) for field in fields]
            data.append(row)
        
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="{}.pdf".format(model.lower()))