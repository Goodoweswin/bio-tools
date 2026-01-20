import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# --- Setup Style ---
try:
    from tools.common import nature_style
except ImportError:
    # Fallback if module loading fails
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

# Initialize session state for demo data if not exists
if 'demo_df' not in st.session_state:
    st.session_state['demo_df'] = None

# Sidebar Controls
with st.sidebar:
    st.header("1. Upload Data")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
    
    # Check for demo data load request
    if st.button("Load Demo Data"):
        np.random.seed(42)
        n_genes = 2000
        genes = [f"Gene_{i}" for i in range(1, n_genes+1)]
        log2fc = np.random.normal(0, 1.5, n_genes)
        pvals = np.random.uniform(0, 1, n_genes)
        # Make some genes clearly significant
        log2fc[:50] += 3.5  # Upregulated
        pvals[:50] = np.random.uniform(0, 0.0001, 50)
        log2fc[50:100] -= 3.5 # Downregulated
        pvals[50:100] = np.random.uniform(0, 0.0001, 50)
        
        st.session_state['demo_df'] = pd.DataFrame({'Gene': genes, 'log2FC': log2fc, 'P-value': pvals})
        st.experimental_rerun()

    # Logic to determine which dataframe to use
    df = None
    if uploaded_file:
        df = load_data(uploaded_file)
    elif st.session_state['demo_df'] is not None:
        df = st.session_state['demo_df']
        st.success("Loaded Demo Data (2000 synthetic genes)")

    st.header("2. Column mapping")
    if df is not None:
        cols = df.columns.tolist()
        # Intelligent defaults
        default_gene = 0
        default_log2fc = 1
        default_pval = 2
        
        if 'Gene' in cols: default_gene = cols.index('Gene')
        if 'log2FC' in cols: default_log2fc = cols.index('log2FC')
        if 'P-value' in cols: default_pval = cols.index('P-value')

        gene_col = st.selectbox("Gene Name Column", cols, index=default_gene)
        log2fc_col = st.selectbox("Log2FC Column", cols, index=default_log2fc)
        pval_col = st.selectbox("P-value/Padj Column", cols, index=default_pval)
    
    st.header("3. Thresholds")
    log2fc_thresh = st.slider("Log2FC Cutoff", 0.0, 5.0, 1.0, 0.1)
    pval_thresh = st.number_input("P-value Cutoff", value=0.05, format="%.4f")

    st.header("4. Aesthetics")
    color_up = st.color_picker("Up Color", "#DC0000")   # Red
    color_down = st.color_picker("Down Color", "#3C5488") # Blue
    color_ns = st.color_picker("NS Color", "#B0B0B0")     # Grey
    point_size = st.slider("Point Size", 2, 20, 6)

# --- Visualization Logic ---
if df is not None:
    # Classify genes
    df['Regulation'] = df.apply(lambda row: classify_gene(row, log2fc_thresh, pval_thresh, log2fc_col, pval_col), axis=1)
    
    # Calculate -log10(P-value)
    df['neg_log10_p'] = -np.log10(df[pval_col] + 1e-300)

    # Tabs
    tab1, tab2 = st.tabs(["📈 Volcano Plot", "💾 Data Table"])

    with tab1:
        st.subheader("Volcano Plot (Nature Style)")
        
        # Apply style
        nature_style.apply_nature_style()
        
        fig, ax = plt.subplots(figsize=(6, 5))
        
        # Plot groups
        for group, color in [('NS', color_ns), ('Up', color_up), ('Down', color_down)]:
            subset = df[df['Regulation'] == group]
            if not subset.empty:
                ax.scatter(subset[log2fc_col], subset['neg_log10_p'], c=color, s=point_size*2, 
                         alpha=0.8, label=group, edgecolors='none')
        
        # Threshold lines
        ax.axvline(x=log2fc_thresh, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.axvline(x=-log2fc_thresh, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.axhline(y=-np.log10(pval_thresh), color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        
        # Labels
        ax.set_xlabel(f"Log2 Fold Change ({log2fc_col})")
        ax.set_ylabel(f"-Log10 P-value")
        ax.legend(frameon=False)
        sns.despine()
        
        st.pyplot(fig)
        
        # Download PDF
        buf = BytesIO()
        fig.savefig(buf, format="pdf", dpi=300, bbox_inches='tight')
        st.download_button(
            label="Download PDF Figure",
            data=buf.getvalue(),
            file_name="volcano_plot.pdf",
            mime="application/pdf"
        )
        
    with tab2:
        st.subheader("Significant Genes")
        sig_df = df[df['Regulation'] != 'NS'].sort_values('neg_log10_p', ascending=False)
        st.write(f"Found {len(sig_df)} significant genes (Up: {len(df[df['Regulation']=='Up'])}, Down: {len(df[df['Regulation']=='Down'])})")
        st.dataframe(sig_df)
        
        csv = sig_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Significant Genes (CSV)",
            csv,
            "significant_genes.csv",
            "text/csv",
            key='download-csv'
        )
