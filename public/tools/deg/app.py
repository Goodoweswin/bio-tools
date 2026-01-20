import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# --- Setup Style ---
try:
    from tools.common import nature_style
except ImportError:
    # Fallback if module loading fails (though stlite handles file mapping)
    class nature_style:
        @staticmethod
        def apply_nature_style():
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
            sns.set_style("ticks")

st.set_page_config(page_title="DEG Analysis (Volcano Plot)", layout="wide")

# --- Helper Functions ---
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def classify_gene(row, log2fc_thresh, pval_thresh, log2fc_col, pval_col):
    if row[pval_col] > pval_thresh:
        return 'NS'
    if row[log2fc_col] >= log2fc_thresh:
        return 'Up'
    if row[log2fc_col] <= -log2fc_thresh:
        return 'Down'
    return 'NS'

# --- Main App ---

st.title("🌋 DEG Analysis: Volcano Plot")
st.markdown("""
Upload your differential expression results (CSV/Excel) to explore key genes.
**Required Columns**: `Gene` (name), `Log2FC` (fold change), `P-value` (significance).
""")

# Sidebar Controls
with st.sidebar:
    st.header("1. Upload Data")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
    
    st.header("2. Column mapping")
    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            cols = df.columns.tolist()
            gene_col = st.selectbox("Gene Name Column", cols, index=0 if 'Gene' not in cols else cols.index('Gene'))
            log2fc_col = st.selectbox("Log2FC Column", cols, index=1 if 'log2FC' not in cols else cols.index('log2FC'))
            pval_col = st.selectbox("P-value/Padj Column", cols, index=2 if 'P-value' not in cols else cols.index('P-value'))
    
    st.header("3. Thresholds")
    log2fc_thresh = st.slider("Log2FC Cutoff", 0.0, 5.0, 1.0, 0.1)
    pval_thresh = st.number_input("P-value Cutoff", value=0.05, format="%.4f")

    st.header("4. Aesthetics")
    color_up = st.color_picker("Up Color", "#DC0000")   # Red
    color_down = st.color_picker("Down Color", "#3C5488") # Blue
    color_ns = st.color_picker("NS Color", "#B0B0B0")     # Grey
    point_size = st.slider("Point Size", 2, 20, 6)

    # --- Data Processing ---
    # Classify genes
    df['Regulation'] = df.apply(lambda row: classify_gene(row, log2fc_thresh, pval_thresh, log2fc_col, pval_col), axis=1)
    
    # Calculate -log10(P-value)
    df['neg_log10_p'] = -np.log10(df[pval_col] + 1e-300)

    # --- Debug Mode: Direct Plotting (No Tabs, No Style) ---
    st.subheader("Static Plot (Simplified)")
    
    # Create simple figure without custom nature_style (to rule out font issues)
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Simple scatter
    colors = {'Up': '#DC0000', 'Down': '#3C5488', 'NS': '#B0B0B0'}
    for group in ['NS', 'Up', 'Down']:
        subset = df[df['Regulation'] == group]
        ax.scatter(subset[log2fc_col], subset['neg_log10_p'], c=colors[group], label=group, alpha=0.6)
    
    ax.axvline(x=log2fc_thresh, c='k', ls='--')
    ax.axvline(x=-log2fc_thresh, c='k', ls='--')
    ax.axhline(y=-np.log10(pval_thresh), c='k', ls='--')
    ax.legend()
    
    st.pyplot(fig)
    
    st.write("Debug: Plot generation code executed.")

else:
    # --- Demo Data Generaton ---
    # --- Demo Data Generation ---
    if st.button("Load Demo Data"):
        np.random.seed(42)
        n_genes = 2000
        genes = [f"Gene_{i}" for i in range(1, n_genes+1)]
        log2fc = np.random.normal(0, 1.5, n_genes)
        pvals = np.random.uniform(0, 1, n_genes)
        # Make some genes clearly significant
        log2fc[:50] += 3.5  # Upregulated
        pvals[:50] = np.random.uniform(0, 0.001, 50)
        log2fc[50:100] -= 3.5 # Downregulated
        pvals[50:100] = np.random.uniform(0, 0.001, 50)
        
        # Store in session state to persist across reruns
        st.session_state['demo_df'] = pd.DataFrame({'Gene': genes, 'log2FC': log2fc, 'P-value': pvals})
        st.experimental_rerun()

# Check for demo data in session state if no file is uploaded
if uploaded_file is None and 'demo_df' in st.session_state:
    df = st.session_state['demo_df']
    st.success("Loaded Demo Data (2000 synthetic genes)")
    
    # Auto-map columns for demo
    with st.sidebar:
        st.header("2. Column mapping (Demo)")
        gene_col = "Gene"
        log2fc_col = "log2FC"
        pval_col = "P-value"
        st.caption(f"Gene: {gene_col}, Log2FC: {log2fc_col}, P-val: {pval_col}")

        
