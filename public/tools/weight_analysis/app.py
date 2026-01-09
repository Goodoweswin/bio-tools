import streamlit as st
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from scikit_posthocs import posthoc_dunn
from statannotations.Annotator import Annotator
import io
import sys
import os
import datetime # Added for timestamp

# Add common directory to path to import nature_style
# In stlite, we map 'tools/common' to a specific path, or simply copy the file content if simpler.
# For robustness in browser, we'll assume nature_style.py is available or copy logic if import fails.
try:
    from tools.common import nature_style
except ImportError:
    # Fallback if path mapping isn't perfect in stlite yet
    class nature_style:
        @staticmethod
        def apply_nature_style():
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
            sns.set_style("ticks")
            sns.set_context("paper")

st.set_page_config(page_title="Difference Analysis Tool", layout="wide")

# --- UI Header ---
st.title("📊 差异分析工具 (Nature Style)")
st.markdown("""
**功能**: 自动进行正态性检验、差异分析(Kruskal-Wallis/ANOVA)、事后检验，并生成学术级图表。
**使用**: 上传 Excel/CSV -> 选择列 -> 下载 PDF。
""")

# --- 1. Upload Data ---
with st.sidebar:
    st.header("1. 数据上传")
    uploaded_file = st.file_uploader("Upload File", type=['xlsx', 'csv'])
    
    st.header("2. 参数设置")
    significance_level = st.selectbox("显著性标记方式", ["简单 (*)", "详细 (p=0.01)"], index=0)
    p_format = 'star' if significance_level == "简单 (*)" else 'simple'

# --- Main Logic ---
if uploaded_file:
    # Load Data
    try:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"文件读取失败: {e}")
        st.stop()

    # Column Selection
    cols = data.columns.tolist()
    c1, c2 = st.columns(2)
    with c1:
        x_col = st.selectbox("选择分组列 (Group Column)", cols, index=0)
    with c2:
        y_col = st.selectbox("选择数值列 (Value Column)", cols, index=1)

    # Reorder Groups
    unique_groups = data[x_col].unique().tolist()
    st.write("### 3. 分组顺序调整")
    group_order = st.multiselect("拖动调整顺序 (默认全选)", unique_groups, default=unique_groups)
    
    if not group_order:
        st.warning("请至少选择一个分组。")
        st.stop()
        
    # Filter Data based on selection
    data_filtered = data[data[x_col].isin(group_order)].copy()
    
    # --- Analysis Button ---
    if st.button("🚀 开始分析 (Run Analysis)", type="primary"):
        st.divider()
        
        # A. Assumptions
        st.subheader("A. 统计假设检验")
        col_res1, col_res2 = st.columns(2)
        
        # Normality
        normality_all_pass = True
        with col_res1:
            st.markdown("**Shapiro-Wilk 正态性检验**")
            for g in group_order:
                g_data = data_filtered[data_filtered[x_col] == g][y_col]
                if len(g_data) < 3:
                     st.write(f"- {g}: 样本量不足 (<3) ⚠️")
                else:
                    stat, p = stats.shapiro(g_data)
                    status = "✅" if p > 0.05 else "❌"
                    if p < 0.05: normality_all_pass = False
                    st.write(f"- {g}: p={p:.4f} {status}")
        
        # Homogeneity
        with col_res2:
            st.markdown("**Levene 方差齐性检验**")
            groups_list = [data_filtered[data_filtered[x_col] == g][y_col] for g in group_order]
            if len(groups_list) > 1:
                stat, p_levene = stats.levene(*groups_list)
                st.write(f"p-value = {p_levene:.4f}")
                if p_levene < 0.05:
                    st.warning("方差不齐，建议使用非参数检验 (Kruskal-Wallis)。")
                else:
                    st.success("方差齐性满足。")
            else:
                st.write("分组少于2组，无法检验。")

        # B. Plotting
        st.subheader("B. 数据可视化 (Nature Style)")
        
        nature_style.apply_nature_style() # Apply Style
        
        fig, ax = plt.subplots(figsize=(4, 5)) # Standard single column width
        
        # 1. Boxplot
        sns.boxplot(x=x_col, y=y_col, data=data_filtered, order=group_order, 
                    palette="Set2", linewidth=1, width=0.6, ax=ax)
        # 2. Strip
        sns.stripplot(x=x_col, y=y_col, data=data_filtered, order=group_order, 
                      color='#333', size=4, alpha=0.7, jitter=True, ax=ax)
        
        # 3. Stats Annotation (Calculated on the fly)
        # Run Kruskal-Wallis first
        try:
            h_stat, k_p = stats.kruskal(*groups_list)
            if k_p < 0.05:
                # Post-hoc Dunn
                dunn = posthoc_dunn(data_filtered, val_col=y_col, group_col=x_col, p_adjust='holm')
                
                # Extract pairs
                pairs = []
                p_values = []
                for i in range(len(group_order)):
                    for j in range(i+1, len(group_order)):
                        g1, g2 = group_order[i], group_order[j]
                        try:
                            pv = dunn.loc[g1, g2]
                            if pv < 0.05:
                                pairs.append((g1, g2))
                                p_values.append(pv)
                        except: pass
                
                if pairs:
                    annotator = Annotator(ax, pairs, data=data_filtered, x=x_col, y=y_col, order=group_order)
                    annotator.configure(text_format=p_format, loc='inside', line_width=1)
                    annotator.set_pvalues_and_annotate(p_values)
            
        except Exception as e:
            st.warning(f"统计计算中出错 (可能是样本量问题): {e}")

        # Final Polish
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        sns.despine()
        
        # Display
        st.pyplot(fig)
        
        # C. Download
        st.subheader("C. 导出结果")
        
        # Smart Filename Generation
        # 1. Get original base name
        if uploaded_file:
            orig_name = os.path.splitext(uploaded_file.name)[0]
        else:
            orig_name = "data"
            
        # 2. Get Timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        
        # 3. Construct default filename: {OriginalName}_{Y_Col}_Analysis_{Date}
        default_base = f"{orig_name}_{y_col}_Analysis_{timestamp}"
        
        # 4. Optional: User custom name
        custom_name = st.text_input("自定义文件名前缀 (可选)", value=default_base)
        
        fn_pdf = f"{custom_name}.pdf"
        fn_png = f"{custom_name}.png"
        
        # Buffer PDF
        buf_pdf = io.BytesIO()
        fig.savefig(buf_pdf, format="pdf", bbox_inches='tight')
        
        # Buffer PNG
        buf_png = io.BytesIO()
        fig.savefig(buf_png, format="png", dpi=300, bbox_inches='tight')
        
        col_d1, col_d2 = st.columns(2)
        col_d1.download_button("📥 下载矢量图 (PDF - 投稿用)", data=buf_pdf, file_name=fn_pdf, mime="application/pdf")
        col_d2.download_button("📥 下载高清图 (PNG - 汇报用)", data=buf_png, file_name=fn_png, mime="image/png")

else:
    st.info("👈 请在左侧上传数据文件开始。")
