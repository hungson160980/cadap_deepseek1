from docx import Document
import re
from datetime import datetime

class DocumentParser:
    def __init__(self):
        self.patterns = {
            'ho_ten': r'Họ và tên:\s*([^\n]+)',
            'cccd': r'CMND/CCCD/hộ chiếu:\s*([^\n]+)',
            'dia_chi': r'Nơi cư trú:\s*([^\n]+)',
            'dien_thoai': r'Số điện thoại:\s*([^\n]+)',
            'tong_nhu_cau_von': r'Tổng nhu cầu vốn:\s*([\d.,]+)',
            'von_doi_ung': r'Vốn đối ứng tham gia.*?:\s*([\d.,]+)',
            'so_tien_vay': r'Vốn vay Agribank số tiền:\s*([\d.,]+)',
            'muc_dich_vay': r'Mục đích vay:\s*([^\n]+)',
            'thoi_gian_vay': r'Thời hạn vay:\s*(\d+)',
            'lai_suat': r'Lãi suất:\s*([\d.,]+)%',
            'gia_tri_tai_san': r'Giá trị.*?:\s*([\d.,]+)'
        }
    
    def parse_document(self, file):
        """Phân tích file docx và trích xuất thông tin"""
        try:
            doc = Document(file)
            full_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            extracted_data = self._extract_data(full_text)
            return extracted_data
            
        except Exception as e:
            print(f"Lỗi khi phân tích document: {e}")
            return None
    
    def _extract_data(self, text):
        """Trích xuất dữ liệu từ text sử dụng regex patterns"""
        data = {}
        
        # Thông tin khách hàng
        customers = self._extract_customers(text)
        if customers:
            data['khach_hang'] = customers
            # Lấy thông tin của khách hàng đầu tiên làm chính
            main_customer = customers[0]
            data.update({
                'ho_ten': main_customer['ho_ten'],
                'cccd': main_customer['cccd'],
                'dia_chi': main_customer['dia_chi'],
                'dien_thoai': main_customer['dien_thoai']
            })
        
        # Thông tin tài chính
        financial_data = self._extract_financial_info(text)
        data.update(financial_data)
        
        # Thông tin tài sản
        collateral_data = self._extract_collateral_info(text)
        data.update(collateral_data)
        
        return data
    
    def _extract_customers(self, text):
        """Trích xuất thông tin nhiều khách hàng"""
        customers = []
        
        # Tìm tất cả các khối thông tin khách hàng
        customer_blocks = re.split(r'\d+\. Họ và tên:', text)
        
        for block in customer_blocks[1:]:  # Bỏ phần đầu không chứa thông tin
            customer = {}
            
            # Họ và tên
            name_match = re.search(r'^([^-]+)', block)
            if name_match:
                customer['ho_ten'] = name_match.group(1).strip()
            
            # CCCD
            cccd_match = re.search(self.patterns['cccd'], block)
            if cccd_match:
                customer['cccd'] = cccd_match.group(1).strip()
            
            # Địa chỉ
            address_match = re.search(self.patterns['dia_chi'], block)
            if address_match:
                customer['dia_chi'] = address_match.group(1).strip()
            
            # Số điện thoại
            phone_match = re.search(self.patterns['dien_thoai'], block)
            if phone_match:
                customer['dien_thoai'] = phone_match.group(1).strip()
            
            if customer:  # Chỉ thêm nếu có thông tin
                customers.append(customer)
        
        return customers
    
    def _extract_financial_info(self, text):
        """Trích xuất thông tin tài chính"""
        financial_data = {}
        
        # Tổng nhu cầu vốn
        total_match = re.search(self.patterns['tong_nhu_cau_von'], text)
        if total_match:
            financial_data['tong_nhu_cau_von'] = self._convert_currency_to_number(total_match.group(1))
        
        # Vốn đối ứng
        owner_match = re.search(self.patterns['von_doi_ung'], text, re.DOTALL)
        if owner_match:
            financial_data['von_doi_ung'] = self._convert_currency_to_number(owner_match.group(1))
        
        # Số tiền vay
        loan_match = re.search(self.patterns['so_tien_vay'], text)
        if loan_match:
            financial_data['so_tien_vay'] = self._convert_currency_to_number(loan_match.group(1))
        
        # Mục đích vay
        purpose_match = re.search(self.patterns['muc_dich_vay'], text)
        if purpose_match:
            financial_data['muc_dich_vay'] = purpose_match.group(1).strip()
        
        # Thời gian vay
        term_match = re.search(self.patterns['thoi_gian_vay'], text)
        if term_match:
            financial_data['thoi_gian_vay'] = int(term_match.group(1))
        
        # Lãi suất
        interest_match = re.search(self.patterns['lai_suat'], text)
        if interest_match:
            financial_data['lai_suat'] = float(interest_match.group(1).replace(',', '.'))
        
        # Tính tỷ lệ vốn đối ứng
        if financial_data.get('tong_nhu_cau_von') and financial_data.get('von_doi_ung'):
            financial_data['ty_le_von_doi_ung'] = (
                financial_data['von_doi_ung'] / financial_data['tong_nhu_cau_von'] * 100
            )
        
        return financial_data
    
    def _extract_collateral_info(self, text):
        """Trích xuất thông tin tài sản bảo đảm"""
        collateral_data = {}
        
        # Tìm thông tin tài sản
        asset_match = re.search(r'Tài sản \d+.*?Giá trị.*?:\s*([\d.,]+)', text, re.DOTALL)
        if asset_match:
            collateral_data['gia_tri_thi_truong'] = self._convert_currency_to_number(asset_match.group(1))
            collateral_data['loai_tai_san'] = "Bất động sản"
        
        # Tìm địa chỉ tài sản
        address_match = re.search(r'Địa chỉ.*?:\s*([^\n]+)', text)
        if address_match:
            collateral_data['dia_chi_tai_san'] = address_match.group(1).strip()
        
        # Tính LTV
        if collateral_data.get('gia_tri_thi_truong') and 'so_tien_vay' in self._extract_financial_info(text):
            financial_data = self._extract_financial_info(text)
            loan_amount = financial_data.get('so_tien_vay', 0)
            asset_value = collateral_data['gia_tri_thi_truong']
            if asset_value > 0:
                collateral_data['ltv'] = (loan_amount / asset_value) * 100
        
        return collateral_data
    
    def _convert_currency_to_number(self, currency_str):
        """Chuyển đổi chuỗi tiền tệ sang số"""
        if not currency_str:
            return 0
        
        # Loại bỏ dấu chấm phân cách hàng nghìn và chuyển dấu phẩy thành dấu chấm cho số thập phân
        cleaned = currency_str.replace('.', '').replace(',', '.').split(' ')[0]
        
        try:
            return float(cleaned)
        except ValueError:
            return 0