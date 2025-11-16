class FinancialCalculator:
    def __init__(self):
        pass
    
    def calculate_payment_schedule(self, financial_data):
        """Tính toán lịch trả nợ"""
        loan_amount = financial_data.get('so_tien_vay', 0)
        interest_rate = financial_data.get('lai_suat', 0) / 100 / 12  # Lãi suất hàng tháng
        loan_term = financial_data.get('thoi_gian_vay', 0)
        
        if not all([loan_amount, interest_rate, loan_term]):
            return []
        
        # Tính toán theo phương thức trả gốc đều
        monthly_payment = self._calculate_monthly_payment(loan_amount, interest_rate, loan_term)
        
        schedule = []
        remaining_balance = loan_amount
        
        for month in range(1, loan_term + 1):
            interest_payment = remaining_balance * interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            
            # Đảm bảo số dư cuối cùng là 0
            if month == loan_term:
                principal_payment += remaining_balance
                remaining_balance = 0
            
            schedule.append({
                'thang': month,
                'tra_goc': round(principal_payment),
                'tra_lai': round(interest_payment),
                'tong_tra': round(principal_payment + interest_payment),
                'goc_con_lai': max(0, round(remaining_balance))
            })
        
        return schedule
    
    def _calculate_monthly_payment(self, loan_amount, monthly_rate, loan_term):
        """Tính toán khoản trả hàng tháng"""
        if monthly_rate == 0:
            return loan_amount / loan_term
        
        return loan_amount * monthly_rate * (1 + monthly_rate) ** loan_term / ((1 + monthly_rate) ** loan_term - 1)
    
    def calculate_financial_metrics(self, financial_data, customer_data):
        """Tính toán các chỉ số tài chính"""
        loan_amount = financial_data.get('so_tien_vay', 0)
        interest_rate = financial_data.get('lai_suat', 0)
        loan_term = financial_data.get('thoi_gian_vay', 0)
        asset_value = financial_data.get('gia_tri_tai_san', 0)
        
        metrics = {}
        
        # Tính nghĩa vụ trả nợ hàng tháng
        if all([loan_amount, interest_rate, loan_term]):
            monthly_rate = interest_rate / 100 / 12
            monthly_payment = self._calculate_monthly_payment(loan_amount, monthly_rate, loan_term)
            metrics['monthly_payment'] = monthly_payment
        
        # Tính LTV (Loan-to-Value)
        if asset_value > 0:
            metrics['ltv'] = (loan_amount / asset_value) * 100
        
        # Tính DSR (Debt Service Ratio) - Giả định thu nhập từ dữ liệu mẫu
        monthly_income = 100000000  # Giả định từ dữ liệu mẫu
        if monthly_payment and monthly_income > 0:
            metrics['dsr_ratio'] = (monthly_payment / monthly_income) * 100
        
        # Tính biên an toàn trả nợ
        monthly_expenses = 45000000  # Giả định từ dữ liệu mẫu
        if monthly_income and monthly_expenses:
            disposable_income = monthly_income - monthly_expenses
            if monthly_payment and disposable_income > 0:
                metrics['safety_margin'] = ((disposable_income - monthly_payment) / disposable_income) * 100
        
        return metrics