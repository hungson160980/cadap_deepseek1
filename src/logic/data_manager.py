class DataManager:
    def __init__(self):
        self.customer_data = {}
        self.financial_data = {}
        self.collateral_data = {}
        self.original_data = {}
    
    def update_from_document(self, extracted_data):
        """Cập nhật dữ liệu từ document được phân tích"""
        self.original_data = extracted_data.copy()
        
        # Cập nhật thông tin khách hàng
        if 'ho_ten' in extracted_data:
            self.customer_data = {
                'ho_ten': extracted_data.get('ho_ten', ''),
                'cccd': extracted_data.get('cccd', ''),
                'dia_chi': extracted_data.get('dia_chi', ''),
                'dien_thoai': extracted_data.get('dien_thoai', '')
            }
        
        # Cập nhật thông tin tài chính
        financial_fields = [
            'tong_nhu_cau_von', 'von_doi_ung', 'so_tien_vay', 
            'ty_le_von_doi_ung', 'lai_suat', 'thoi_gian_vay', 'muc_dich_vay'
        ]
        self.financial_data = {
            field: extracted_data.get(field, 0 if field != 'muc_dich_vay' else '')
            for field in financial_fields
        }
        
        # Cập nhật thông tin tài sản
        collateral_fields = [
            'loai_tai_san', 'gia_tri_thi_truong', 'dia_chi_tai_san', 'ltv', 'giay_to_phap_ly'
        ]
        self.collateral_data = {
            field: extracted_data.get(field, 0 if field not in ['loai_tai_san', 'dia_chi_tai_san', 'giay_to_phap_ly'] else '')
            for field in collateral_fields
        }
    
    def update_customer_data(self, data):
        """Cập nhật thông tin khách hàng"""
        self.customer_data.update(data)
    
    def update_financial_data(self, data):
        """Cập nhật thông tin tài chính"""
        self.financial_data.update(data)
    
    def update_collateral_data(self, data):
        """Cập nhật thông tin tài sản"""
        self.collateral_data.update(data)
    
    def get_customer_data(self):
        """Lấy thông tin khách hàng"""
        return self.customer_data.copy()
    
    def get_financial_data(self):
        """Lấy thông tin tài chính"""
        return self.financial_data.copy()
    
    def get_collateral_data(self):
        """Lấy thông tin tài sản"""
        return self.collateral_data.copy()
    
    def get_original_data(self):
        """Lấy dữ liệu gốc từ file"""
        return self.original_data.copy()