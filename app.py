import streamlit as st
import pandas as pd
from database import create_table, insert_expense, get_expenses
from ai_processor import analyze_receipt

# Force mobile-friendly wide layout layout and configure page app
st.set_page_config(page_title="AI Receipt Auditor", page_icon="📱", layout="centered")

# Initialize database table
create_table()

st.title("📱 AI Personal Finance Auditor")
st.write("Snap a photo of any printed receipt or handwritten shop chit to log it instantly.")

# --- SECTION 1: MOBILE FILE UPLOADER / CAMERA INTERFACE ---
st.subheader("📸 Scan New Receipt")
uploaded_file = st.file_uploader(
    "Choose an image file or use your phone camera to snap a receipt", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    # Preview image directly on mobile interface
    st.image(uploaded_file, caption="Uploaded Receipt Preview", use_column_width=True)
    
    if st.button("🚀 Process & Audit with AI", use_container_width=True):
        with st.spinner("AI is analyzing text and auditing spending values..."):
            # Send file directly to our processing brain
            extracted_data = analyze_receipt(uploaded_file)
            
            # Save the clean extracted fields to our SQLite database
            insert_expense(
                store_name=extracted_data.get("store_name", "Local Vendor"),
                amount=float(extracted_data.get("amount", 0.0)),
                category=extracted_data.get("category", "Other"),
                date=extracted_data.get("date", "2026-08-20")
            )
            st.success(f"Successfully logged ₹{extracted_data.get('amount')} spent at {extracted_data.get('store_name')}!")
            # Trigger app rerun to show updated data records
            st.rerun()

st.markdown("---")

# --- SECTION 2: METRICS & VISUAL DATA RECORDS ---
expenses_data = get_expenses()

if expenses_data:
    # Convert local list data into a Pandas DataFrame for analytics computing
    df = pd.DataFrame(expenses_data, columns=["Store", "Amount (₹)", "Category", "Date"])
    
    total_spent = df["Amount (₹)"].sum()
    
    # Large UI Summary Block 
    st.metric(label="💰 Total Monitored Expenses This Month", value=f"₹{total_spent:,.2f}")
    
    # Categorized Progress Breakdown
    st.subheader("📊 Spending Breakdown by Category")
    category_totals = df.groupby("Category")["Amount (₹)"].sum()
    for cat, amt in category_totals.items():
        percentage = amt / total_spent
        st.write(f"**{cat}**: ₹{amt:,.2f} ({percentage*100:.1f}%)")
        st.progress(float(percentage))
        
    st.markdown("---")
    
    # History logs display
    st.subheader("📋 Expense History Logs")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No recorded expenses found. Upload or snap your first receipt above to begin building logs!")
