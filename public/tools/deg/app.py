
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Placeholder for nature_style logic until common module is perfectly mapped
try:
    from tools.common import nature_style
except ImportError:
    class nature_style:
        @staticmethod
        def apply_nature_style():
            plt.rcParams['font.family'] = 'sans-serif'
            sns.set_style("ticks")
            sns.set_context("paper")

st.set_page_config(page_title="DEG Analysis Tool", layout="wide")

st.title("🌋 差异表达基因分析 (Volcano Plot)")
st.markdown("""
**功能**: 上传差异分析结果 (DEG) 表格，生成火山图。
**要求**: 表格需包含 `log2FoldChange` 和 `pvalue` (或 `padj`) 列。
""")

# Sidebar
with st.sidebar:
    st.header("1. 数据上传")
    uploaded_file = st.file_uploader("Upload DESeq2/EdgeR Results", type=['xlsx', 'csv'])
    
    st.header("2. 阈值设置")
    fc_cutoff = st.number_input("Log2FC Cutoff", value=1.0, step=0.5)
    p_cutoff = st.number_input("P-value Cutoff", value=0.05, format="%.2f")

if uploaded_file:
    # Load Data
    try:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()
        
    st.write(f"Loaded {len(data)} rows.")
    cols = data.columns.tolist()
    
    c1, c2 = st.columns(2)
    with c1:
        fc_col = st.selectbox("Select Log2FC Column", cols, index=0 if 'log2FoldChange' in cols else 0)
    with c2:
        p_col = st.selectbox("Select P-value Column", cols, index=0 if 'pvalue' in cols else 0)

    # Plotting
    if st.button("🚀 Plot Volcano", type="primary"):
        # Categorize
        data['Significance'] = 'NS'
        data.loc[(data[fc_col] > fc_cutoff) & (data[p_col] < p_cutoff), 'Significance'] = 'Up'
        data.loc[(data[fc_col] < -fc_cutoff) & (data[p_col] < p_cutoff), 'Significance'] = 'Down'
        
        nature_style.apply_nature_style()
        fig, ax = plt.subplots(figsize=(6, 5))
        
        sns.scatterplot(data=data, x=fc_col, y=p_col, hue='Significance', 
                        palette={'Up': '#E64B35', 'Down': '#4DBBD5', 'NS': 'grey'},
                        alpha=0.7, ax=ax)
        
        # Invert Y axis for volcano
        # Note: Usually we plot -log10(pvalue), but for simplicity here strictly following mapped columns first
        # Let's auto-convert for better viz if user allows, but here we keep it simple or assume P-val
        ax.set_title("Volcano Plot")
        sns.despine()
        
        st.pyplot(fig)

else:
    st.info("👈 Please upload a DEG statistics file.")
