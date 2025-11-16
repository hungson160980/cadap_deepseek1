import streamlit as st
from src.ui.components import *
from src.logic.document_parser import DocumentParser
from src.logic.financial_calculator import FinancialCalculator
from src.export.excel_exporter import ExcelExporter
from src.export.report_exporter import ReportExporter

def create_sidebar():
    """Tạo sidebar cho API key và upload file"""
    with st.sidebar:
        st.header("🔑 Cài đặt API")
        
        api_key = st.text_input(
            "Google AI Studio API Key",
            type="password",
            help="Nhập API key từ Google AI Studio để sử dụng Gemini AI"
        )
        
        if api_key:
            st.session_state.gemini_client.set_api_key(api_key)
            st.success("✅ API key đã được thiết lập")
        
        st.markdown("---")
        st.header("📤 Upload File")
        
        uploaded_file = st.file_uploader(
            "Tải lên file PASDV.docx",
            type=['docx'],
            help="Tải lên file phương án sử dụng vốn định dạng .docx"
        )
        
        if uploaded_file is not None:
            try:
                parser = DocumentParser()
                extracted_data = parser.parse_document(uploaded_file)
                
                if extracted_data:
                    st.session_state.data_manager.update_from_document(extracted_data)
                    st.success("✅ File đã được xử lý thành công!")
                    
                    # Hiển thị thông tin cơ bản từ file
                    with st.expander("📋 Xem thông tin trích xuất từ file"):
                        if 'khach_hang' in extracted_data:
                            for kh in extracted_data['khach_hang']:
                                st.write(f"**{kh['ho_ten']}** - {kh['cccd']}")
                else:
                    st.error("❌ Không thể trích xuất dữ liệu từ file")
            except Exception as e:
                st.error(f"❌ Lỗi khi xử lý file: {str(e)}")
        
        st.markdown("---")
        st.header("💡 Hướng dẫn")
        st.info("""
        1. Nhập API key Google AI Studio
        2. Upload file PASDV.docx
        3. Kiểm tra và chỉnh sửa dữ liệu ở các tab
        4. Phân tích với AI và xuất báo cáo
        """)

def create_tabs():
    """Tạo các tab chính của ứng dụng"""
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "👤 Thông Tin Khách Hàng",
        "💰 Thông Tin Tài Chính", 
        "🏠 Tài Sản Bảo Đảm",
        "📊 Tính Toán Tài Chính",
        "📈 Biểu Đồ",
        "🤖 Phân Tích AI",
        "💬 Chatbox Gemini",
        "📤 Xuất File"
    ])
    
    with tab1:
        create_customer_info_tab()
    
    with tab2:
        create_financial_info_tab()
    
    with tab3:
        create_collateral_tab()
    
    with tab4:
        create_financial_calculation_tab()
    
    with tab5:
        create_charts_tab()
    
    with tab6:
        create_ai_analysis_tab()
    
    with tab7:
        create_chatbox_tab()
    
    with tab8:
        create_export_tab()

def create_customer_info_tab():
    """Tab thông tin khách hàng"""
    st.header("👤 Thông Tin Định Danh Khách Hàng")
    
    data_manager = st.session_state.data_manager
    customer_data = data_manager.get_customer_data()
    
    st.subheader("Thông tin khách hàng chính")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ho_ten = st.text_input("Họ và tên", 
                             value=customer_data.get('ho_ten', ''),
                             key="customer_name")
    
    with col2:
        cccd = st.text_input("CCCD/CMND", 
                           value=customer_data.get('cccd', ''),
                           key="customer_id")
    
    col3, col4 = st.columns(2)
    
    with col3:
        dia_chi = st.text_input("Địa chỉ", 
                              value=customer_data.get('dia_chi', ''),
                              key="customer_address")
    
    with col4:
        dien_thoai = st.text_input("Số điện thoại", 
                                 value=customer_data.get('dien_thoai', ''),
                                 key="customer_phone")
    
    # Cập nhật dữ liệu
    if st.button("💾 Lưu thông tin khách hàng"):
        updated_data = {
            'ho_ten': ho_ten,
            'cccd': cccd,
            'dia_chi': dia_chi,
            'dien_thoai': dien_thoai
        }
        data_manager.update_customer_data(updated_data)
        st.success("✅ Thông tin khách hàng đã được cập nhật")

def create_financial_info_tab():
    """Tab thông tin tài chính"""
    st.header("💰 Thông Tin Tài Chính / Phương Án Sử Dụng Vốn")
    
    data_manager = st.session_state.data_manager
    financial_data = data_manager.get_financial_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        muc_dich_vay = st.text_area("Mục đích vay",
                                  value=financial_data.get('muc_dich_vay', ''),
                                  height=100,
                                  key="loan_purpose")
        
        tong_nhu_cau_von = create_number_input(
            "Tổng nhu cầu vốn (VNĐ)",
            "total_capital_needed",
            value=financial_data.get('tong_nhu_cau_von', 0)
        )
        
        von_doi_ung = create_number_input(
            "Vốn đối ứng (VNĐ)", 
            "owner_capital",
            value=financial_data.get('von_doi_ung', 0)
        )
    
    with col2:
        so_tien_vay = create_number_input(
            "Số tiền vay (VNĐ)",
            "loan_amount", 
            value=financial_data.get('so_tien_vay', 0)
        )
        
        ty_le_von_doi_ung = st.number_input(
            "Tỷ lệ vốn đối ứng (%)",
            min_value=0.0,
            max_value=100.0,
            value=financial_data.get('ty_le_von_doi_ung', 0.0),
            key="owner_capital_ratio"
        )
        
        lai_suat = st.number_input(
            "Lãi suất vay (%/năm)",
            min_value=0.0,
            max_value=50.0,
            value=financial_data.get('lai_suat', 0.0),
            step=0.1,
            key="interest_rate"
        )
        
        thoi_gian_vay = st.number_input(
            "Thời gian vay (tháng)",
            min_value=1,
            max_value=360,
            value=financial_data.get('thoi_gian_vay', 0),
            key="loan_term"
        )
    
    if st.button("💾 Lưu thông tin tài chính"):
        updated_data = {
            'muc_dich_vay': muc_dich_vay,
            'tong_nhu_cau_von': tong_nhu_cau_von,
            'von_doi_ung': von_doi_ung,
            'so_tien_vay': so_tien_vay,
            'ty_le_von_doi_ung': ty_le_von_ung,
            'lai_suat': lai_suat,
            'thoi_gian_vay': thoi_gian_vay
        }
        data_manager.update_financial_data(updated_data)
        st.success("✅ Thông tin tài chính đã được cập nhật")

def create_collateral_tab():
    """Tab tài sản bảo đảm"""
    st.header("🏠 Tài Sản Bảo Đảm")
    
    data_manager = st.session_state.data_manager
    collateral_data = data_manager.get_collateral_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        loai_tai_san = st.selectbox(
            "Loại tài sản",
            ["Bất động sản", "Xe ô tô", "Thiết bị máy móc", "Tài sản khác"],
            key="asset_type"
        )
        
        gia_tri_thi_truong = create_number_input(
            "Giá trị thị trường (VNĐ)",
            "market_value",
            value=collateral_data.get('gia_tri_thi_truong', 0)
        )
    
    with col2:
        dia_chi_tai_san = st.text_input(
            "Địa chỉ tài sản",
            value=collateral_data.get('dia_chi_tai_san', ''),
            key="asset_address"
        )
        
        ltv = st.number_input(
            "LTV (%)",
            min_value=0.0,
            max_value=100.0,
            value=collateral_data.get('ltv', 0.0),
            key="ltv_ratio"
        )
        
        giay_to_phap_ly = st.text_area(
            "Giấy tờ pháp lý",
            value=collateral_data.get('giay_to_phap_ly', ''),
            height=100,
            key="legal_docs"
        )
    
    if st.button("💾 Lưu thông tin tài sản"):
        updated_data = {
            'loai_tai_san': loai_tai_san,
            'gia_tri_thi_truong': gia_tri_thi_truong,
            'dia_chi_tai_san': dia_chi_tai_san,
            'ltv': ltv,
            'giay_to_phap_ly': giay_to_phap_ly
        }
        data_manager.update_collateral_data(updated_data)
        st.success("✅ Thông tin tài sản đã được cập nhật")

def create_financial_calculation_tab():
    """Tab tính toán tài chính"""
    st.header("📊 Tính Toán Chỉ Tiêu Tài Chính / Dòng Tiền")
    
    data_manager = st.session_state.data_manager
    financial_data = data_manager.get_financial_data()
    customer_data = data_manager.get_customer_data()
    
    if not financial_data.get('so_tien_vay') or not financial_data.get('lai_suat'):
        st.warning("Vui lòng nhập đầy đủ thông tin tài chính ở tab trước")
        return
    
    # Tính toán các chỉ số
    calculator = FinancialCalculator()
    metrics = calculator.calculate_financial_metrics(financial_data, customer_data)
    payment_schedule = calculator.calculate_payment_schedule(financial_data)
    
    # Hiển thị các chỉ số
    display_financial_metrics(metrics)
    
    st.subheader("📋 Kế hoạch trả nợ")
    
    if payment_schedule:
        # Hiển thị bảng kế hoạch trả nợ
        df = pd.DataFrame(payment_schedule)
        st.dataframe(df, use_container_width=True)
        
        # Lưu vào session state để sử dụng ở tab export
        st.session_state.payment_schedule = payment_schedule
        st.session_state.financial_metrics = metrics

def create_charts_tab():
    """Tab biểu đồ"""
    st.header("📈 Biểu Đồ Phân Tích Tài Chính")
    
    data_manager = st.session_state.data_manager
    financial_data = data_manager.get_financial_data()
    
    if not financial_data:
        st.warning("Chưa có dữ liệu tài chính để vẽ biểu đồ")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Phân bổ nguồn vốn")
        create_financial_pie_chart(financial_data)
    
    with col2:
        st.subheader("Lịch trả nợ")
        payment_schedule = getattr(st.session_state, 'payment_schedule', [])
        create_payment_schedule_chart(payment_schedule)

def create_ai_analysis_tab():
    """Tab phân tích AI"""
    st.header("🤖 Phân Tích AI Gemini")
    
    if not st.session_state.gemini_client.is_configured():
        st.warning("Vui lòng nhập API key ở sidebar để sử dụng tính năng AI")
        return
    
    data_manager = st.session_state.data_manager
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Phân tích từ File Upload")
        if st.button("🔍 Phân tích dữ liệu gốc", key="analyze_original"):
            with st.spinner("AI đang phân tích dữ liệu từ file..."):
                original_data = data_manager.get_original_data()
                analysis = st.session_state.gemini_client.analyze_financial_data(
                    original_data, "dữ liệu gốc từ file upload"
                )
                st.text_area("Kết quả phân tích", analysis, height=300)
    
    with col2:
        st.subheader("✏️ Phân tích dữ liệu đã chỉnh sửa")
        if st.button("🔍 Phân tích dữ liệu hiện tại", key="analyze_current"):
            with st.spinner("AI đang phân tích dữ liệu hiện tại..."):
                current_data = {
                    'customer': data_manager.get_customer_data(),
                    'financial': data_manager.get_financial_data(),
                    'collateral': data_manager.get_collateral_data(),
                    'metrics': getattr(st.session_state, 'financial_metrics', {})
                }
                analysis = st.session_state.gemini_client.analyze_financial_data(
                    current_data, "dữ liệu sau khi hiệu chỉnh tại giao diện"
                )
                st.text_area("Kết quả phân tích", analysis, height=300)

def create_chatbox_tab():
    """Tab chatbox với Gemini"""
    st.header("💬 Chatbox Gemini")
    
    if not st.session_state.gemini_client.is_configured():
        st.warning("Vui lòng nhập API key ở sidebar để sử dụng chatbox")
        return
    
    # Hiển thị lịch sử chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input chat
    prompt = st.chat_input("Nhập câu hỏi của bạn...")
    
    if prompt:
        # Thêm câu hỏi vào lịch sử
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Nhận phản hồi từ AI
        with st.spinner("AI đang suy nghĩ..."):
            response = st.session_state.gemini_client.chat(prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.write(response)
    
    # Nút xóa hội thoại
    if st.button("🗑️ Xóa hội thoại"):
        st.session_state.chat_history = []
        st.rerun()

def create_export_tab():
    """Tab xuất file"""
    st.header("📤 Xuất File Báo Cáo")
    
    data_manager = st.session_state.data_manager
    
    export_option = st.selectbox(
        "Chọn loại file xuất",
        [
            "Xuất bảng kê kế hoạch trả nợ (Excel)",
            "Xuất báo cáo thẩm định (Word/PDF)"
        ]
    )
    
    if export_option == "Xuất bảng kê kế hoạch trả nợ (Excel)":
        if st.button("📊 Xuất file Excel"):
            payment_schedule = getattr(st.session_state, 'payment_schedule', [])
            if payment_schedule:
                exporter = ExcelExporter()
                excel_file = exporter.export_payment_schedule(payment_schedule)
                
                st.download_button(
                    label="📥 Tải xuống file Excel",
                    data=excel_file,
                    file_name="ke_hoach_tra_no.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Không có dữ liệu kế hoạch trả nợ để xuất")
    
    else:  # Xuất báo cáo thẩm định
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.radio(
                "Định dạng báo cáo",
                ["Word (.docx)", "PDF (.pdf)"]
            )
        
        with col2:
            include_charts = st.checkbox("Bao gồm biểu đồ", value=True)
        
        if st.button("📄 Tạo báo cáo thẩm định"):
            with st.spinner("Đang tạo báo cáo..."):
                exporter = ReportExporter()
                
                # Thu thập dữ liệu cho báo cáo
                report_data = {
                    'customer': data_manager.get_customer_data(),
                    'financial': data_manager.get_financial_data(),
                    'collateral': data_manager.get_collateral_data(),
                    'metrics': getattr(st.session_state, 'financial_metrics', {}),
                    'payment_schedule': getattr(st.session_state, 'payment_schedule', [])
                }
                
                if report_type == "Word (.docx)":
                    report_file = exporter.export_word_report(report_data, include_charts)
                    mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    file_name = "bao_cao_tham_dinh.docx"
                else:
                    report_file = exporter.export_pdf_report(report_data, include_charts)
                    mime_type = "application/pdf"
                    file_name = "bao_cao_tham_dinh.pdf"
                
                st.download_button(
                    label=f"📥 Tải xuống {file_name}",
                    data=report_file,
                    file_name=file_name,
                    mime=mime_type
                )