import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def format_currency(value):
    """Định dạng số tiền với dấu phân cách hàng nghìn"""
    try:
        return f"{float(value):,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return "0"

def create_number_input(label, key, value=0, min_value=0, max_value=100000000000, step=1000000):
    """Tạo input số với nút tăng/giảm"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        new_value = st.number_input(
            label,
            min_value=min_value,
            max_value=max_value,
            value=value,
            step=step,
            key=key
        )
    
    with col2:
        if st.button("➕", key=f"inc_{key}"):
            new_value += step
            st.session_state[key] = new_value
            st.rerun()
    
    with col3:
        if st.button("➖", key=f"dec_{key}"):
            new_value = max(min_value, new_value - step)
            st.session_state[key] = new_value
            st.rerun()
    
    return new_value

def display_financial_metrics(metrics):
    """Hiển thị các chỉ số tài chính"""
    if not metrics:
        st.warning("Chưa có dữ liệu để tính toán chỉ số tài chính")
        return
    
    cols = st.columns(4)
    
    with cols[0]:
        st.metric(
            "Nghĩa vụ trả nợ hàng tháng",
            f"{format_currency(metrics.get('monthly_payment', 0))} VNĐ"
        )
    
    with cols[1]:
        st.metric(
            "Tỷ lệ trả nợ (DSR)",
            f"{metrics.get('dsr_ratio', 0):.1f}%"
        )
    
    with cols[2]:
        st.metric(
            "LTV",
            f"{metrics.get('ltv', 0):.1f}%"
        )
    
    with cols[3]:
        st.metric(
            "Biên an toàn trả nợ",
            f"{metrics.get('safety_margin', 0):.1f}%"
        )

def create_payment_schedule_chart(payment_schedule):
    """Tạo biểu đồ lịch trả nợ"""
    if not payment_schedule:
        st.warning("Không có dữ liệu lịch trả nợ")
        return
    
    df = pd.DataFrame(payment_schedule)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Biểu đồ dòng tiền
    ax1.plot(df['thang'], df['goc_con_lai'], marker='o', linewidth=2)
    ax1.set_title('Dư nợ gốc theo thời gian')
    ax1.set_xlabel('Tháng')
    ax1.set_ylabel('Dư nợ gốc (VNĐ)')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Biểu đồ phân bổ trả nợ
    months = df['thang'][::max(1, len(df)//10)]  # Hiển thị 10 mốc
    principal = df['tra_goc'][::max(1, len(df)//10)]
    interest = df['tra_lai'][::max(1, len(df)//10)]
    
    x = range(len(months))
    width = 0.35
    
    ax2.bar(x, principal, width, label='Trả gốc', alpha=0.7)
    ax2.bar([i + width for i in x], interest, width, label='Trả lãi', alpha=0.7)
    ax2.set_title('Phân bổ trả nợ theo tháng')
    ax2.set_xlabel('Tháng')
    ax2.set_ylabel('Số tiền (VNĐ)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks([i + width/2 for i in x])
    ax2.set_xticklabels(months, rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)

def create_financial_pie_chart(financial_data):
    """Tạo biểu đồ tròn phân bổ tài chính"""
    if not financial_data:
        st.warning("Không có dữ liệu để tạo biểu đồ")
        return
    
    labels = ['Vốn vay', 'Vốn đối ứng']
    sizes = [
        financial_data.get('so_tien_vay', 0),
        financial_data.get('von_doi_ung', 0)
    ]
    
    if sum(sizes) == 0:
        st.warning("Không có dữ liệu vốn")
        return
    
    colors = ['#ff9999', '#66b3ff']
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Phân bổ nguồn vốn')
    st.pyplot(fig)