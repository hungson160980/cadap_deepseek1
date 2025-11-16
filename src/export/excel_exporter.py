import pandas as pd
from io import BytesIO

class ExcelExporter:
    def __init__(self):
        pass
    
    def export_payment_schedule(self, payment_schedule):
        """Xuất lịch trả nợ ra file Excel"""
        df = pd.DataFrame(payment_schedule)
        
        # Định dạng số tiền
        currency_columns = ['tra_goc', 'tra_lai', 'tong_tra', 'goc_con_lai']
        for col in currency_columns:
            df[col] = df[col].apply(lambda x: f"{x:,.0f}".replace(",", "."))
        
        # Tạo file Excel trong memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='KeHoachTraNo', index=False)
            
            # Định dạng worksheet
            workbook = writer.book
            worksheet = writer.sheets['KeHoachTraNo']
            
            # Đặt độ rộng cột
            worksheet.column_dimensions['A'].width = 8
            worksheet.column_dimensions['B'].width = 15
            worksheet.column_dimensions['C'].width = 15
            worksheet.column_dimensions['D'].width = 15
            worksheet.column_dimensions['E'].width = 15
        
        output.seek(0)
        return output.getvalue()