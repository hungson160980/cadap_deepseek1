import google.generativeai as genai
import json

class GeminiClient:
    def __init__(self):
        self.api_key = None
        self.model = None
    
    def set_api_key(self, api_key):
        """Thiết lập API key"""
        self.api_key = api_key
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            print(f"Lỗi khi thiết lập Gemini: {e}")
    
    def is_configured(self):
        """Kiểm tra xem client đã được cấu hình chưa"""
        return self.api_key is not None and self.model is not None
    
    def analyze_financial_data(self, data, data_source):
        """Phân tích dữ liệu tài chính"""
        if not self.is_configured():
            return "API key chưa được thiết lập"
        
        try:
            prompt = f"""
            Bạn là chuyên gia phân tích tín dụng ngân hàng. Hãy phân tích dữ liệu sau đây và đưa ra đánh giá:
            
            NGUỒN DỮ LIỆU: {data_source}
            
            DỮ LIỆU PHÂN TÍCH:
            {json.dumps(data, indent=2, ensure_ascii=False)}
            
            Hãy cung cấp phân tích với các nội dung:
            1. Đánh giá rủi ro tín dụng
            2. Khả năng trả nợ của khách hàng
            3. Đề xuất cho cán bộ tín dụng
            4. Các điểm cần lưu ý
            
            Phân tích ngắn gọn nhưng đầy đủ, chuyên sâu.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Lỗi khi phân tích: {str(e)}"
    
    def chat(self, message):
        """Chat với Gemini"""
        if not self.is_configured():
            return "API key chưa được thiết lập"
        
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"Lỗi khi chat: {str(e)}"