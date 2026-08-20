import streamlit as st
import pandas as pd
from database import create_table, insert_expense, get_expenses
from ai_processor import analyze_receipt

# Configure mobile-friendly centered app page layout
st.set_page_config(page_title="AI Receipt Auditor", page_icon="📱", layout="centered")

# Initialize database table
create_table()

st.title("📱 AI Personal Finance Auditor")
st.write("Snap a photo of any printed receipt or handwritten shop chit to log it instantly.")

# --- SECTION 1: SCANNING CAPTURE INTERFACE ---
st.subheader("📸 Scan New Receipt")
uploaded_file = st.file_uploader(
    "Choose an image file or use your phone camera to snap a receipt", 
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    # Render preview image instantly on phone screen
    st.image(uploaded_file, caption="Uploaded Receipt Preview")
    
    if st.button("🚀 Process & Audit with AI", use_container_width=True):
        with st.spinner("Gemini AI is reading text and auditing transaction values..."):
            # Route uploaded image data matrix directly into Gemini processor module
            extracted_data = analyze_receipt(uploaded_file)
            
            try:
                # Safely convert extracted amount to a clear float value
                raw_amount = extracted_data.get("amount", 0.0)
                amount_value = float(raw_amount) if raw_amount else 0.0
            except ValueError:
                amount_value = 0.0
                
            # Commit clean structured keys cleanly into SQLite local database box
            insert_expense(
                store_name=extracted_data.get("store_name", "Local Vendor"),
                amount=amount_value,
                category=extracted_data.get("category", "Other"),
                date=extracted_data.get("date", "2026-08-20")
            )
            st.success(f"Logged ₹{amount_value} spent at {extracted_data.get('store_name')}!")
            # Trigger clean view update refresh cycle
            st.rerun()

st.markdown("---")

# --- SECTION 2: ANALYTICS METRICS & HISTORY LOGS ---
expenses_data = get_expenses()

if expenses_data:
    # Parse transaction arrays directly into a structured Pandas DataFrame 
    df = pd.DataFrame(expenses_data, columns=["Store", "Amount (₹)", "Category", "Date"])
    
    # FILTER OUT 0 amounts from analytics calculations to completely protect progress bars from crashing
    analytics_df = df[df["Amount (₹)"] > 0]
    
    if not analytics_df.empty:
        total_spent = analytics_df["Amount (₹)"].sum()
        
        # Render visual layout metric card 
        st.metric(label="💰 Total Monitored Expenses This Month", value=f"₹{total_spent:,.2f}")
        
        # Generate contextual categorized breakdown meters
        st.subheader("📊 Spending Breakdown by Category")
        category_totals = analytics_df.groupby("Category")["Amount (₹)"].sum()
        for cat, amt in category_totals.items():
            percentage = amt / total_spent
            st.write(f"**{cat}**: ₹{amt:,.2f} ({percentage*100:.1f}%)")
            
            # Constrain progress bar value strictly between a safe 0.0 and 1.0 boundary
            safe_progress = max(0.0, min(float(percentage), 1.0))
            st.progress(safe_progress)
    else:
        st.metric(label="💰 Total Monitored Expenses This Month", value="₹0.00")
        st.info("No valid expenses found yet to display category charts.")
        
    st.markdown("---")
    
    # Display clear interactive data historical spreadsheet (shows all logs, even the errors)
    st.subheader("📋 Expense History Logs")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No recorded expenses found. Upload or snap your first receipt above to begin building logs!")
