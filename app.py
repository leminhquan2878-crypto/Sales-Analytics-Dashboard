
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")
st.title("Sales Analytics Dashboard ")
st.write("""
Ứng dụng này phân tích dữ liệu bán hàng :
- Doanh thu theo tháng
- Doanh thu theo thành phố
- Phân bố đơn hàng theo giờ
- Top sản phẩm bán chạy
- Sản phẩm thường được mua cùng nhau
""")

# 1. Upload CSV files

uploaded_files = st.file_uploader(
    "Tải lên các file CSV bán hàng (có thể nhiều file, ví dụ 12 tháng)",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    # Đọc và gộp dữ liệu
    frames = [pd.read_csv(file) for file in uploaded_files]
    df = pd.concat(frames, ignore_index=True)
    st.success(f"Đã tải {len(uploaded_files)} file, tổng {len(df)} dòng dữ liệu.")

    # 2. Clean data
    
    df = df.dropna(how='all')
    df = df[df['Order Date'].str[0:2] != 'Or']
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
    df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
    df = df.dropna(subset=['Quantity Ordered', 'Price Each'])
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']
    df['Month'] = df['Order Date'].str[0:2]
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Hour'] = df['Order Date'].dt.hour

    # Extract city
    if 'Purchase Address' in df.columns:
        df['City'] = df['Purchase Address'].apply(lambda x: x.split(',')[1] if ',' in x else 'Unknown')
    else:
        df['City'] = 'Unknown'

 
    # 3. Sidebar filters
   
    st.sidebar.header("Bộ lọc dữ liệu")
    months = sorted(df['Month'].dropna().unique())
    cities = sorted(df['City'].dropna().unique())

    selected_months = st.sidebar.multiselect("Chọn tháng:", months, default=months)
    selected_cities = st.sidebar.multiselect("Chọn thành phố:", cities, default=cities)

    df = df[df['Month'].isin(selected_months)]
    df = df[df['City'].isin(selected_cities)]


    # 4. Key metrics
  
    st.header("Tổng quan doanh thu")
    col1, col2, col3 = st.columns(3)
    total_sales = df['Sales'].sum()
    total_orders = df['Order ID'].nunique()
    avg_order_value = total_sales / total_orders if total_orders else 0

    col1.metric("Tổng doanh thu", f"${total_sales:,.2f}")
    col2.metric("Số đơn hàng", f"{total_orders}")
    col3.metric("Giá trị trung bình / đơn", f"${avg_order_value:,.2f}")


    # 5. Charts
  
    st.subheader("Doanh thu theo tháng")
    sales_by_month = df.groupby('Month')['Sales'].sum().sort_index()
    fig, ax = plt.subplots()
    ax.bar(sales_by_month.index, sales_by_month.values, color='skyblue')
    ax.set_xlabel("Tháng")
    ax.set_ylabel("Doanh thu (USD)")
    st.pyplot(fig)

    st.subheader("Doanh thu theo thành phố")
    sales_by_city = df.groupby('City')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.bar(sales_by_city.index, sales_by_city.values, color='lightgreen')
    plt.xticks(rotation=90)
    ax.set_ylabel("Doanh thu (USD)")
    st.pyplot(fig)

    st.subheader("Phân bố đơn hàng theo giờ trong ngày")
    hourly_sales = df.groupby('Hour')['Order ID'].count()
    fig, ax = plt.subplots()
    ax.plot(hourly_sales.index, hourly_sales.values, marker='o')
    ax.set_xlabel("Giờ trong ngày")
    ax.set_ylabel("Số lượng đơn hàng")
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("Top 10 sản phẩm bán chạy nhất")
    top_products = df.groupby('Product')['Quantity Ordered'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    ax.bar(top_products.index, top_products.values, color='orange')
    plt.xticks(rotation=90)
    ax.set_ylabel("Số lượng bán ra")
    st.pyplot(fig)


    # 6. Top products + price 

    st.subheader("Top sản phẩm bán chạy & Giá trung bình")
    all_products = df.groupby('Product')['Quantity Ordered'].sum()
    prices = df.groupby('Product')['Price Each'].mean()
    products_ls = all_products.index.tolist()

    fig, ax1 = plt.subplots(figsize=(12,5))
    ax2 = ax1.twinx()
    ax1.bar(products_ls, all_products, color='g')
    ax2.plot(products_ls, prices, color='b', marker='o')
    ax1.set_xticklabels(products_ls, rotation=90, fontsize=8)
    ax1.set_xlabel('Products')
    ax1.set_ylabel('Quantity Ordered', color='g')
    ax2.set_ylabel('Price Each (USD)', color='b')
    st.pyplot(fig)

    # 7. Products often sold together
 
    st.header("Sản phẩm thường được mua cùng nhau")
    df_dup = df[df['Order ID'].duplicated(keep=False)]
    df_dup['All Products'] = df_dup.groupby('Order ID')['Product'].transform(lambda x: ', '.join(x))
    df_dup = df_dup[['Order ID', 'All Products']].drop_duplicates()
    combo_counts = df_dup['All Products'].value_counts().head(10)
    st.write("Top 10 combo sản phẩm được mua cùng nhau:")
    st.table(combo_counts.reset_index().rename(columns={'index': 'Combo sản phẩm', 'All Products': 'Số lượng'}))

else:
    st.info("Hãy tải lên dữ liệu CSV để bắt đầu phân tích.")
