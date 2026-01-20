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

if uploaded_file and df is not None:
    # --- Data Processing ---
    # Classify genes
    df['Regulation'] = df.apply(lambda row: classify_gene(row, log2fc_thresh, pval_thresh, log2fc_col, pval_col), axis=1)
    
    # Calculate -log10(P-value) for plotting
    # Avoid log(0) by adding a tiny epsilon if p=0
    df['neg_log10_p'] = -np.log10(df[pval_col] + 1e-300)

    # Split output into tabs
    tab1, tab2, tab3 = st.tabs(["📈 Interactive Plot", "📄 Publication Plot", "💾 Data Table"])

    # --- Tab 1: Interactive Plotly ---
    with tab1:
        st.subheader("Interactive Exploration")
        
        # Map colors
        color_map = {'Up': color_up, 'Down': color_down, 'NS': color_ns}
        
        fig = px.scatter(
            df, 
            x=log2fc_col, 
            y='neg_log10_p',
            color='Regulation',
            color_discrete_map=color_map,
            hover_name=gene_col,
            hover_data=[log2fc_col, pval_col],
            title=f"Volcano Plot (n={len(df)})",
            template="simple_white"
        )
        
        # Add threshold lines
        fig.add_vline(x=log2fc_thresh, line_width=1, line_dash="dash", line_color="black")
        fig.add_vline(x=-log2fc_thresh, line_width=1, line_dash="dash", line_color="black")
        fig.add_hline(y=-np.log10(pval_thresh), line_width=1, line_dash="dash", line_color="black")

        fig.update_traces(marker=dict(size=point_size, opacity=0.8))
        fig.update_layout(
            xaxis_title="Log2 Fold Change",
            yaxis_title="-Log10(P-value)",
            legend_title_text="Regulation",
            width=800,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # --- Tab 2: Matplotlib (Publication) ---
    with tab2:
        st.subheader("Static Plot (Nature Style)")
        nature_style.apply_nature_style()
        
        plt_fig, ax = plt.subplots(figsize=(5, 4))
        
        # Plot each group manually to ensure order and color
        for group, color in [('NS', color_ns), ('Up', color_up), ('Down', color_down)]:
            subset = df[df['Regulation'] == group]
            ax.scatter(subset[log2fc_col], subset['neg_log10_p'], c=color, s=point_size*2, alpha=0.8, label=group, edgecolors='none')
            
        # Lines
        ax.axvline(x=log2fc_thresh, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.axvline(x=-log2fc_thresh, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        ax.axhline(y=-np.log10(pval_thresh), color='black', linestyle='--', linewidth=0.8, alpha=0.5)
        
        ax.set_xlabel("Log2 Fold Change")
        ax.set_ylabel("-Log10(P-value)")
        ax.legend(frameon=False)
        sns.despine()
        
        st.pyplot(plt_fig)
        
        # Download button
        buf = BytesIO()
        plt_fig.savefig(buf, format="pdf", dpi=300, bbox_inches='tight')
        st.download_button(
            label="Download PDF Figure",
            data=buf.getvalue(),
            file_name="volcano_plot.pdf",
            mime="application/pdf"
        )

    # --- Tab 3: Data Table ---
    with tab3:
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

else:
    # --- Demo Data Generaton ---
    if st.button("Load Demo Data"):
        # Generate some synthetic data
        np.random.seed(42)
        n_genes = 2000
        genes = [f"Gene_{i}" for i in range(1, n_genes+1)]
        log2fc = np.random.normal(0, 1.5, n_genes)
        pvals = np.random.uniform(0, 1, n_genes)
        # Make some genes clearly significant
        log2fc[:50] += 3  # Upregulated
        pvals[:50] /= 1000
        log2fc[50:100] -= 3 # Downregulated
        pvals[50:100] /= 1000
        
        demo_df = pd.DataFrame({'Gene': genes, 'log2FC': log2fc, 'P-value': pvals})
        # Save to session state to simulate upload
        # For simplicity, we just display it directly
        # But in a real app, we'd loop back. Here we just ask user to download demo and upload it?
        # Better: create a CSV in memory to allow 'load_data' to read it? 
        # Easier: Just set a flag
        st.info("Demo mode not fully implemented in this MVP. Please upload a CSV with columns: Gene, log2FC, P-value")
        
