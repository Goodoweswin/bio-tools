import streamlit as st
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scikit_posthocs import posthoc_dunn
from statannotations.Annotator import Annotator
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import datetime
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

# --- Color Palettes ---
PALETTES = {
    "🔴 红蓝经典": ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F', '#8491B4', '#91D1C2', '#DC0000', '#7E6148', '#B09C85'],
    "🔵 冷色专业": ['#3B4992', '#EE0000', '#008B45', '#631879', '#008280', '#BB0021', '#5F559B', '#A20056', '#808180', '#1B1919'],
    "🟠 暖色医学": ['#BC3C29', '#0072B5', '#E18727', '#20854E', '#7876B1', '#6F99AD', '#FFDC91', '#EE4C97'],
    "🟢 柔和自然": "Set2",
    "🟣 高对比": "Set1",
    "🔵 蓝色渐变": "Blues",
    "🤎 色盲友好": ['#0077BB', '#33BBEE', '#009988', '#EE7733', '#CC3311', '#EE3377', '#BBBBBB'],
    "⚫ 灰度单色": ['#000000', '#333333', '#666666', '#999999', '#CCCCCC', '#E5E5E5'],
    "🌈 彩虹渐变": "husl",
    "🧬 科研柔和 (Sci)": ['#B4C7E7', '#E6B8D1', '#C5E0B4', '#FFE699', '#F4B183', '#D9D9D9'],
    "✏️ 自定义...": None  # Triggers custom input
}

CUSTOM_PALETTE_KEY = "✏️ 自定义..."

def get_palette_colors(name, n_colors=None, custom_colors=None):
    """Get palette colors by name. If custom, parse from custom_colors string."""
    if name == CUSTOM_PALETTE_KEY and custom_colors:
        # Parse custom hex colors
        try:
            colors = [c.strip() for c in custom_colors.split(',') if c.strip().startswith('#')]
            if colors:
                return colors[:n_colors] if n_colors else colors
        except:
            pass
        return sns.color_palette("Set2", n_colors=n_colors)  # Fallback
    
    if name in PALETTES:
        param = PALETTES[name]
        if param is None:
            return sns.color_palette("Set2", n_colors=n_colors)
        elif isinstance(param, list):
            return param[:n_colors] if n_colors else param
        else:
            return sns.color_palette(param, n_colors=n_colors)
    return sns.color_palette("Set2", n_colors=n_colors)

# --- Setup Style ---
try:
    from tools.common import nature_style
except ImportError:
    class nature_style:
        @staticmethod
        def apply_nature_style():
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
            sns.set_style("ticks")
            sns.set_context("paper")

st.set_page_config(page_title="Bio-Analysis Suite v4.0", layout="wide", initial_sidebar_state="expanded")

# --- Session State for Report ---
if 'report_items' not in st.session_state:
    st.session_state['report_items'] = []

def add_to_report(title, fig=None, df=None, text=None):
    """Add item to analysis report"""
    # Convert Plot to Image Bytes immediately to avoid state issues
    img_bytes = None
    if fig:
        buf = io.BytesIO()
        try:
            if hasattr(fig, 'savefig'):
                fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
            else:
                fig.figure.savefig(buf, format='png', dpi=300, bbox_inches='tight')
            img_bytes = buf.getvalue()
        except Exception as e:
            st.error(f"Error saving figure for report: {e}")

    item = {
        "title": title,
        "img_bytes": img_bytes,
        "df": df,
        "text": text,
        "time": datetime.datetime.now().strftime("%H:%M:%S")
    }
    st.session_state['report_items'].append(item)
    st.toast(f"✅ 已添加到报告: {title}")

# --- Helper Functions ---
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"文件读取失败: {e}")
        return None

def get_download_buttons(fig, prefix, key_suffix, df_stats=None, report_title=None):
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        custom_name = st.text_input("文件名", value=f"{prefix}_{datetime.datetime.now().strftime('%Y%m%d')}", key=f"fname_{key_suffix}")
    
    # Report Button
    with c3:
        st.write("") # Spacer
        st.write("")
        if st.button("➕ 添加到报告", key=f"rpt_{key_suffix}"):
            add_to_report(report_title or prefix, fig=fig, df=df_stats)
    
    # Save Logic
    buf_pdf = io.BytesIO()
    buf_png = io.BytesIO()
    
    try:
        if hasattr(fig, 'savefig'):
            fig.savefig(buf_pdf, format="pdf", bbox_inches='tight')
            fig.savefig(buf_png, format="png", dpi=300, bbox_inches='tight')
        else:
            fig.figure.savefig(buf_pdf, format="pdf", bbox_inches='tight')
            fig.figure.savefig(buf_png, format="png", dpi=300, bbox_inches='tight')
    except: pass
    
    c_d1, c_d2 = st.columns(2)
    c_d1.download_button("📥 PDF", data=buf_pdf, file_name=f"{custom_name}.pdf", mime="application/pdf", key=f"dl_pdf_{key_suffix}")
    c_d2.download_button("📥 PNG", data=buf_png, file_name=f"{custom_name}.png", mime="image/png", key=f"dl_png_{key_suffix}")

# --- Educational Modules ---
def render_stat_guide():
    with st.expander("📚 统计学小课堂：我该选什么检验？(Statistical Guide)", expanded=False):
        st.markdown("""
        ### Q1: 我有几组数据？
        
        #### 👉 只有 2 组 (例如: Control vs Treat)
        *   **Student's t-test (t检验)**: 
            *   数据符合**正态分布** (钟形曲线)。
            *   两组数据的**方差相似** (胖瘦差不多)。
        *   **Welch's t-test (校正t检验)**: 
            *   数据符合正态分布。
            *   但是**方差不齐** (一组很散，一组很聚)。*本工具会自动检测并选用此项。*
        *   **Mann-Whitney U test (非参数检验)**: 
            *   数据**不符合**正态分布 (分布很怪，或者样本量极少 <3)。
        
        #### 👉 有 3 组或更多 (例如: Control, Dose1, Dose2)
        *   **One-way ANOVA (单因素方差分析)**: 
            *   数据符合**正态分布**。
            *   **方差齐**。
            *   *后续会配合 Tukey HSD 进行两两比较。*
        *   **Kruskal-Wallis test (非参数方差分析)**: 
            *   数据**不符合**正态分布。
            *   *后续会配合 Dunn's test 进行两两比较。*
            
        ---
        ### 💡 常见名词解释
        *   **正态性 (Normality)**: 数据是否呈现中间高、两边低的对称分布。
        *   **方差齐性 (Homogeneity of Variance)**: 不同组别的数据离散程度是否一致。
        *   **P < 0.05**: 通常认为具有"统计学显著差异" (Statistically Significant)。
        *   **ns**: Not Significant，无显著差异 (P > 0.05)。
        """)

# --- Modules ---

def render_difference_module(data):
    st.header("📊 箱线图 (Boxplot)")
    render_stat_guide() # Insert Guide Here
    
    cols = data.columns.tolist()
    c1, c2, c3 = st.columns(3)
    x_col = c1.selectbox("分组列 (Group)", cols, index=0, key="diff_x")
    y_col = c2.selectbox("数值列 (Value)", cols, index=min(1, len(cols)-1), key="diff_y")
    hue_col = c3.selectbox("颜色分组 (Hue, 可选)", ["无"] + cols, index=0, key="diff_hue")

    group_order = st.multiselect("分组顺序", sorted(data[x_col].unique()), default=sorted(data[x_col].unique()))
    if not group_order: return

    # User input for plot title
    c_opt1, c_opt2, c_opt3 = st.columns([1, 1, 1])
    # Advanced Layout Option
    metric_as_x = c_opt1.checkbox("将数值列名作为X轴 (Single Metric)", value=False, key="diff_metric_x", help="开启后，X轴显示参数名，分组显示在图例中")
    # Palette Selection
    # Try to set default to Scientific if available
    palette_keys = list(PALETTES.keys())
    default_idx = next((i for i, k in enumerate(palette_keys) if "🧬" in k), 0)
    palette_name = c_opt3.selectbox("配色方案", palette_keys, index=default_idx, key="diff_palette")
    
    # Advanced Styling
    with st.expander("🎨 样式与标注设置 (Style & Stats)", expanded=True):
        c_s1, c_s2, c_s3, c_s4 = st.columns(4)
        show_points = c_s1.checkbox("显示散点 (Points)", value=True, key="diff_points")
        show_ns = c_s2.checkbox("显示 'ns'", value=False, key="diff_show_ns", help="勾选后将显示非显著差异 (p>0.05) 的标记")
        p_val_fmt = c_s3.selectbox("P值格式", ["Star (*)", "Simple (p=0.05)"], index=1, key="diff_pfmt")
        italic_xaxis = c_s4.checkbox("斜体X轴 (Italic)", value=True, key="diff_italic")
        # Width Slider
        default_width = 0.4 if metric_as_x else 0.5
        box_width = st.slider("箱体宽度 (Width)", 0.1, 1.0, default_width, 0.1, key="diff_width")
    
    # Custom color input (appears if user selects custom)
    custom_colors = None
    if palette_name == CUSTOM_PALETTE_KEY:
        custom_colors = st.text_input("输入自定义颜色 (逗号分隔)", placeholder="#FF0000, #00FF00, #0000FF", key="diff_custom_colors")

    custom_title = st.text_input("图表标题 (Plot Title)", value="", placeholder="留空则无标题", key="diff_plot_title")

    if st.button("🚀 运行分析 (智能模式)", type="primary"):
        st.session_state['diff_active'] = True
        
    if st.session_state.get('diff_active', False):
        st.divider()
        data_filtered = data[data[x_col].isin(group_order)].copy()
        
        # --- FIX: Type Consistency for Plotting & Stats ---
        data_filtered[x_col] = data_filtered[x_col].astype(str)
        group_order_str = [str(g) for g in group_order]
        
        # Robust Data Cleaning:
        data_filtered[y_col] = pd.to_numeric(data_filtered[y_col], errors='coerce')

        import numpy as np
        data_filtered = data_filtered.replace([np.inf, -np.inf], np.nan)
        data_filtered = data_filtered.dropna(subset=[y_col, x_col])

        # --- Layout Logic Transformation ---
        plot_x_col = x_col
        plot_hue_col = hue_col if hue_col != "无" else None
        plot_order = group_order_str
        hue_order = None
        
        if metric_as_x:
            # Single Metric Mode: X-axis = Metric Name, Hue = Original Group
            metric_name = y_col
            data_filtered["_Metric"] = metric_name
            plot_x_col = "_Metric"
            plot_order = [metric_name]
            
            plot_hue_col = x_col # Original group becomes Hue
            hue_order = group_order_str # Original group order becomes Hue order
        elif plot_hue_col:
             hue_order = sorted(data_filtered[plot_hue_col].astype(str).unique())

        # Prepare Data Groups for Stats (Based on original logic or new logic?)
        # Original logic was comparing X groups.
        # If Metric Mode, we want to compare Hue groups (which was original X).
        # So we can keep using 'groups_data' based on original X_col for global stats.
        groups_data = [data_filtered[data_filtered[x_col]==g][y_col] for g in group_order_str]
        
        if len(groups_data) < 2:
            st.error("需要至少两组数据进行比较")
            return

        # --- 1. Assumption Checks ---
        st.subheader("🧐 统计策略检测 (Statistical Strategy)")
        
        normality_passed = True
        dataset_too_small = False
        shapiro_res = {}
        
        # Normality (Shapiro-Wilk)
        for g, vals in zip(group_order_str, groups_data):
            if len(vals) < 3:
                dataset_too_small = True
                normality_passed = False 
                shapiro_res[g] = (0, 0, "N<3, Fail")
            else:
                stat_val, p = stats.shapiro(vals)
                shapiro_res[g] = (stat_val, p, "Pass" if p > 0.05 else "Fail")
                if p <= 0.05: normality_passed = False

        # Homogeneity (Levene)
        # Only check Levene if we have enough samples to potentially run ANOVA
        if len(groups_data) > 1 and all(len(g) >= 2 for g in groups_data):
            levene_stat, levene_p = stats.levene(*groups_data)
            equal_var = levene_p > 0.05
        else:
            levene_p = 0
            equal_var = False # Conservative fallback

        # Display Report
        with st.expander("📄 查看详细假设检验报告 (Assumption Check Report)", expanded=True):
            c_r1, c_r2 = st.columns(2)
            with c_r1:
                st.markdown("**1. 正态性检验 (Shapiro-Wilk)**")
                for g, res in shapiro_res.items():
                    color = "green" if res[2] == "Pass" else "red"
                    val_str = f"p={res[1]:.4f}" if isinstance(res[1], float) else res[2]
                    st.markdown(f"- {g}: :{color}[{val_str}]")
                if dataset_too_small: st.warning("⚠️ 样本量 < 3，自动视为非正态")
            
            with c_r2:
                st.markdown("**2. 方差齐性检验 (Levene)**")
                color = "green" if equal_var else "red"
                st.markdown(f"- P-Value: :{color}[{levene_p:.4f}]")
                st.markdown(f"- 结论: {'方差齐 (Equal Var)' if equal_var else '方差不齐 (Unequal Var)'}")

        # --- 2. Select Test ---
        test_name = "Unknown"
        p_global = 1.0
        statistic = 0.0
        sig_pairs = []

        if len(groups_data) == 2:
            g1, g2 = groups_data[0], groups_data[1]
            if normality_passed:
                if equal_var:
                    test_name = "Student's t-test"
                    statistic, p_global = stats.ttest_ind(g1, g2, equal_var=True)
                else:
                    test_name = "Welch's t-test"
                    statistic, p_global = stats.ttest_ind(g1, g2, equal_var=False)
            else:
                test_name = "Mann-Whitney U"
                statistic, p_global = stats.mannwhitneyu(g1, g2)
            
            if p_global < 0.05 or show_ns:
                sig_pairs = [((group_order_str[0], group_order_str[1]), p_global)]

        else:
            if normality_passed and equal_var:
                test_name = "One-way ANOVA"
                statistic, p_global = stats.f_oneway(*groups_data)
                st.info(f"👉 数据符合正态分布且方差齐，自动选择: **{test_name} (Post-hoc: Tukey HSD)**")
                
                # Checkbox to force running post-hoc even if global p > 0.05 is generally discouraged, 
                # but if user wants to see "ns", we should allow pairwise checks.
                # Standard practice: Only run post-hoc if global p < 0.05.
                # If show_ns is True, user implies they want to see the comparisons anyway.
                if p_global < 0.05 or show_ns:
                    try:
                        tukey = pairwise_tukeyhsd(endog=data_filtered[y_col], groups=data_filtered[x_col], alpha=0.05)
                        tukey_data = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
                        for _, row in tukey_data.iterrows():
                             if row['reject'] or show_ns:
                                 sig_pairs.append( ((str(row['group1']), str(row['group2'])), row['p-adj']) )
                    except Exception as e:
                        st.warning(f"Tukey Post-hoc failed ({str(e)}), switching to Robust Pairwise T-tests (Holm-Sidak)...")
                        # Fallback: Pairwise T-test with Holm correction
                        from statsmodels.stats.multitest import multipletests
                        p_vals = []
                        pair_indices = []
                        
                        # Calculate raw p-values
                        for i in range(len(group_order_str)):
                            for j in range(i+1, len(group_order_str)):
                                g1 = groups_data[i]
                                g2 = groups_data[j]
                                # Use Welch's T-test for robustness in fallback
                                _, p = stats.ttest_ind(g1, g2, equal_var=False) 
                                p_vals.append(p)
                                pair_indices.append((group_order_str[i], group_order_str[j]))
                        
                        # Apply Correction (Holm)
                        if p_vals:
                            reject, p_adjusted, _, _ = multipletests(p_vals, method='holm')
                            for k, (pai, padj) in enumerate(zip(pair_indices, p_adjusted)):
                                if reject[k] or show_ns:
                                    sig_pairs.append((pai, padj))
            else:
                test_name = "Kruskal-Wallis"
                statistic, p_global = stats.kruskal(*groups_data)
                st.info(f"👉 数据不符合正态分布或方差不齐，自动选择: **{test_name} (Post-hoc: Dunn)**")
                
                if p_global < 0.05 or show_ns:
                    dunn = posthoc_dunn(data_filtered, val_col=y_col, group_col=x_col, p_adjust='holm')
                    for i in range(len(group_order_str)):
                        for j in range(i+1, len(group_order_str)):
                            p_val = dunn.loc[group_order_str[i], group_order_str[j]]
                            if p_val < 0.05 or show_ns:
                                sig_pairs.append( ((group_order_str[i], group_order_str[j]), p_val) )

        if len(groups_data) == 2:
             st.info(f"👉 自动选择: **{test_name}**")

        # --- 3. Plotting ---
        nature_style.apply_nature_style()
        fig, ax = plt.subplots(figsize=(5, 5))
        
        # Get palette colors
        # If Hue is used, we need colors for Hue levels.
        # If Metric Mode, Hue=Original X, so n_colors=len(group_order)
        # If Standard Mode + Hue, n_colors=len(hue_unique)
        # If Standard Mode No Hue, n_colors=len(group_order)
        if plot_hue_col:
            hue_levels = hue_order if hue_order else sorted(data_filtered[plot_hue_col].astype(str).unique())
            n_colors = len(hue_levels)
        else:
            n_colors = len(group_order_str)
            
        colors = get_palette_colors(palette_name, n_colors=n_colors, custom_colors=custom_colors)
        
        if metric_as_x:
            # Robust alignment: standard width 0.8 to match stripplot dodge
            real_width = 0.8
            # Use slider to control "Padding" (Inverse logic)
            padding_factor = (1.1 - box_width) * 1.5 
            ax.set_xlim(-0.5 - padding_factor, 0.5 + padding_factor)
        else:
            real_width = box_width

        # Boxplot
        sns.boxplot(x=plot_x_col, y=y_col, hue=plot_hue_col, data=data_filtered, 
                    order=plot_order, hue_order=hue_order,
                    width=real_width, ax=ax, palette=colors,
                    linewidth=1.0, fliersize=0) 
        
        # Stripplot (Styled)
        if show_points:
            dodge = True if plot_hue_col else False
            sns.stripplot(x=plot_x_col, y=y_col, hue=plot_hue_col, data=data_filtered, 
                          order=plot_order, hue_order=hue_order,
                          dodge=dodge, size=5, jitter=True, ax=ax,
                          color="white", edgecolor="gray", linewidth=1,
                          legend=False) # Legend handled by boxplot
        
        # Annotate
        text_format = 'simple' if 'Simple' in p_val_fmt else 'star'
        
        # Stats Annotation Logic Update for Layouts
        try:
            # Case 1: Standard Mode (No Hue) -> Compare X groups
            if not plot_hue_col:
                if sig_pairs:
                     plot_pairs = [p[0] for p in sig_pairs]
                     p_values = [p[1] for p in sig_pairs]
                     annotator = Annotator(ax, plot_pairs, data=data_filtered, x=plot_x_col, y=y_col, order=plot_order)
                     annotator.configure(test=None, text_format=text_format, loc='inside' if text_format=='star' else 'outside', verbose=False)
                     annotator.set_pvalues(p_values)
                     annotator.annotate()
            
            # Case 2: Metric as X Mode -> Compare Hue groups within the single Metric X
            elif metric_as_x:
                # We want to compare the Hue groups (which are the original X groups)
                # sig_pairs contains (GroupA, GroupB)
                # We need to construct pairs like: (("Metric", GroupA), ("Metric", GroupB))
                if sig_pairs:
                     # Reformat pairs for statannotations with hue
                     hue_plot_pairs = []
                     for (g1, g2), _ in sig_pairs:
                         hue_plot_pairs.append(((metric_name, g1), (metric_name, g2)))
                     
                     p_values = [p[1] for p in sig_pairs]
                     
                     annotator = Annotator(ax, hue_plot_pairs, data=data_filtered, x=plot_x_col, y=y_col, hue=plot_hue_col, 
                                           order=plot_order, hue_order=hue_order)
                     annotator.configure(test=None, text_format=text_format, loc='inside' if text_format=='star' else 'outside', verbose=False)
                     annotator.set_pvalues(p_values)
                     annotator.annotate()
            
            # Case 3: Standard Mode + Hue -> Hue comparisons? Or X comparisons?
            # Typically user wants to compare Hue within X. Not implemented in previous stats logic but useful.
            # For now, let's skip complex stats for Case 3 to avoid breakage, unless user asks.
            
        except Exception as e:
             st.write(f"Annotation Warning: {e}")
        
        if custom_title:
            ax.set_title(custom_title, fontsize=12)
        else:
            ax.set_title("") 

        if italic_xaxis and not metric_as_x: # If metric as X, usually not italic
             ax.set_xticklabels(ax.get_xticklabels(), fontstyle='italic')

        sns.despine()
        
        # Move Legend
        if plot_hue_col:
             plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        st.pyplot(fig)
        
        # Result DataFrame
        res_df = pd.DataFrame({
            "Test Selected": [test_name], 
            "Statistic": [statistic], 
            "Global P-Value": [p_global],
            "Normality": ["Pass" if normality_passed else "Fail"],
            "Equal Variance": ["Pass" if equal_var else "Fail"]
        })
        st.dataframe(res_df)
        
        get_download_buttons(fig, f"Stat_{y_col}", "stat", df_stats=res_df, report_title=f"Analysis: {test_name} on {y_col}")

# --- Bar Chart Module ---
def render_barplot_module(data):
    st.header("📊 条形图 (Bar Chart)")
    st.markdown("绘制带误差棒的条形图，支持统计分析和显著性标注。")
    
    cols = data.columns.tolist()
    num_cols = data.select_dtypes(include=['number']).columns.tolist()
    
    c1, c2, c3 = st.columns(3)
    x_col = c1.selectbox("分组列 (X)", cols, index=0, key="bar_x")
    y_col = c2.selectbox("数值列 (Y)", num_cols, index=0, key="bar_y")
    hue_col = c3.selectbox("颜色分组 (Hue, 可选)", ["无"] + cols, index=0, key="bar_hue")
    
    # Options Row 1
    c_opt1, c_opt2, c_opt3 = st.columns(3)
    agg_method = c_opt1.selectbox("聚合方式", ["mean", "median", "sum", "count"], key="bar_agg")
    error_type = c_opt2.selectbox("误差棒", ["sd", "se", "ci", "无"], key="bar_err")
    palette_keys = list(PALETTES.keys())
    default_idx = next((i for i, k in enumerate(palette_keys) if "🧬" in k), 0)
    palette_name = c_opt3.selectbox("配色方案", palette_keys, index=default_idx, key="bar_palette") 

    # Advanced Styling
    with st.expander("🎨 样式与标注设置 (Style & Stats)", expanded=True):
        c_s1, c_s2, c_s3, c_s4 = st.columns(4)
        show_points = c_s1.checkbox("显示散点 (Points)", value=True, key="bar_points")
        show_ns = c_s2.checkbox("显示 'ns'", value=False, key="bar_show_ns")
        p_val_fmt = c_s3.selectbox("P值格式", ["Star (*)", "Simple (p=0.05)"], index=1, key="bar_pfmt")
        italic_xaxis = c_s4.checkbox("斜体X轴 (Italic)", value=True, key="bar_italic")
        # Layout Option
        metric_as_x = st.checkbox("将数值列名作为X轴 (Single Metric)", value=False, key="bar_metric_x", help="开启后，X轴显示参数名，分组以不同颜色展示")
        # Width Slider
        default_bar_width = 0.4 if metric_as_x else 0.6
        bar_width_val = st.slider("条形宽度 (Width)", 0.1, 1.0, default_bar_width, 0.1, key="bar_width")

    # Custom color input
    custom_colors = None
    if palette_name == CUSTOM_PALETTE_KEY:
        custom_colors = st.text_input("输入自定义颜色 (逗号分隔)", placeholder="#FF0000, #00FF00, #0000FF", key="bar_custom_colors")
    
    custom_title = st.text_input("图表标题", value="", placeholder="留空则无标题", key="bar_plot_title")
    
    # Group order
    group_order = st.multiselect("分组顺序 (X)", sorted(data[x_col].unique()), default=sorted(data[x_col].unique()), key="bar_order")
    if not group_order: return
    
    if st.button("🚀 生成条形图", type="primary", key="bar_btn"):
        st.session_state['bar_active'] = True
    
    if st.session_state.get('bar_active', False):
        st.divider()
        import numpy as np
        
        # Data Preparation
        data_filtered = data[data[x_col].isin(group_order)].copy()
        data_filtered[x_col] = data_filtered[x_col].astype(str)
        data_filtered[y_col] = pd.to_numeric(data_filtered[y_col], errors='coerce')
        data_filtered = data_filtered.replace([np.inf, -np.inf], np.nan).dropna(subset=[y_col, x_col])
        group_order_str = [str(g) for g in group_order]
        
        # --- Layout Logic Transformation ---
        plot_x_col = x_col
        plot_hue_col = hue_col if hue_col != "无" else None
        plot_order = group_order_str
        hue_order = None
        
        if metric_as_x:
            # Single Metric Mode
            metric_name = y_col
            data_filtered["_Metric"] = metric_name
            plot_x_col = "_Metric"
            plot_order = [metric_name]
            
            plot_hue_col = x_col # Original Group becomes Hue
            hue_order = group_order_str
        elif plot_hue_col:
             hue_order = sorted(data_filtered[plot_hue_col].astype(str).unique())
        
        # Aggregation
        if agg_method == "mean":
            estimator = np.mean
        elif agg_method == "median":
            estimator = np.median
        elif agg_method == "sum":
            estimator = np.sum
        else:
            estimator = len
        
        # Error Bar
        errorbar_param = None if error_type == "无" else error_type
        
        # Plotting Setup
        nature_style.apply_nature_style()
        fig, ax = plt.subplots(figsize=(5, 5))
        
        hue = None if hue_col == "无" else hue_col
        # Calculate N colors needed
        if plot_hue_col:
            hue_levels = hue_order if hue_order else sorted(data_filtered[plot_hue_col].astype(str).unique())
            n_colors = len(hue_levels)
        else:
            n_colors = len(plot_order)

        colors = get_palette_colors(palette_name, n_colors=n_colors, custom_colors=custom_colors)
        
        if metric_as_x:
            real_width = 0.8 # Standard Seaborn width
            # Control Padding
            padding_factor = (1.1 - bar_width_val) * 1.5
            ax.set_xlim(-0.5 - padding_factor, 0.5 + padding_factor)
        else:
            real_width = bar_width_val

        # 1. Main Bar Plot
        sns.barplot(
            data=data_filtered, x=plot_x_col, y=y_col, order=plot_order,
            hue=plot_hue_col, hue_order=hue_order,
            estimator=estimator, errorbar=errorbar_param,
            palette=colors, ax=ax, capsize=0.1, errwidth=1.5,
            edgecolor="black", linewidth=1.0, 
            width=real_width, dodge=True
        )
        
        # 2. Points Overlay
        if show_points:
            dodge = True if plot_hue_col else False
            sns.stripplot(
                data=data_filtered, x=plot_x_col, y=y_col, 
                hue=plot_hue_col, order=plot_order, hue_order=hue_order,
                dodge=dodge, jitter=True, size=5,
                color="white", edgecolor="gray", linewidth=1, # White points with gray edge like reference
                ax=ax, legend=False, alpha=0.9
            )

        # 3. Statistical Analysis
        text_format = 'simple' if 'Simple' in p_val_fmt else 'star'
        
        # --- Logic for Stats ---
        try:
            if not plot_hue_col:
                # Simple comparisons between X groups
                groups_data = [data_filtered[data_filtered[x_col]==g][y_col] for g in group_order_str]
                if len(groups_data) >= 2:
                    sig_pairs_found = []
                    # KW or Mann-Whitney
                    if len(groups_data) == 2:
                        _, p = stats.mannwhitneyu(groups_data[0], groups_data[1])
                        if p < 0.05 or show_ns:
                            sig_pairs_found.append(((group_order_str[0], group_order_str[1]), p))
                    else:
                        _, k_p = stats.kruskal(*groups_data)
                        if k_p < 0.05 or show_ns:
                            dunn = posthoc_dunn(data_filtered, val_col=y_col, group_col=x_col, p_adjust='holm')
                            for i in range(len(group_order_str)):
                                for j in range(i+1, len(group_order_str)):
                                    p_val = dunn.loc[group_order_str[i], group_order_str[j]]
                                    if p_val < 0.05 or show_ns:
                                        sig_pairs_found.append(((group_order_str[i], group_order_str[j]), p_val))
                    
                    if sig_pairs_found:
                        annotator = Annotator(ax, [p[0] for p in sig_pairs_found], data=data_filtered, x=plot_x_col, y=y_col, order=plot_order)
                        annotator.configure(test=None, text_format=text_format, loc='inside' if text_format=='star' else 'outside', verbose=False)
                        annotator.set_pvalues([p[1] for p in sig_pairs_found])
                        annotator.annotate()

            elif metric_as_x:
                # Metric Mode: Compare Hue groups (Original Groups)
                # Reformat pairs for statannotations with hue
                # Compare all pairs in group_order
                sig_pairs_found = []
                groups_data = [data_filtered[data_filtered[x_col]==g][y_col] for g in group_order_str]
                
                # We need p-values for pairs
                # Let's reuse simple logic, calculating p for pairs
                import itertools
                pairs = list(itertools.combinations(group_order_str, 2))
                
                hue_plot_pairs = []
                p_values = []
                
                for g1, g2 in pairs:
                    v1 = data_filtered[data_filtered[x_col]==g1][y_col]
                    v2 = data_filtered[data_filtered[x_col]==g2][y_col]
                    try:
                        _, p = stats.mannwhitneyu(v1, v2)
                        if p < 0.05 or show_ns:
                            hue_plot_pairs.append(((metric_name, g1), (metric_name, g2)))
                            p_values.append(p)
                    except: pass

                if hue_plot_pairs:
                     annotator = Annotator(ax, hue_plot_pairs, data=data_filtered, x=plot_x_col, y=y_col, hue=plot_hue_col, 
                                           order=plot_order, hue_order=hue_order)
                     annotator.configure(test=None, text_format=text_format, loc='inside' if text_format=='star' else 'outside', verbose=False, line_offset=0.08, line_offset_to_group=0.05)
                     annotator.set_pvalues(p_values)
                     annotator.annotate()

            else:
                # Hue Stats (Standard)
                # Compare hues within each X group (Common requirement)
                hue_order = sorted(data_filtered[hue_col].unique())
                if len(hue_order) == 2:
                    pairs = []
                    for g in group_order_str:
                        pairs.append(((g, hue_order[0]), (g, hue_order[1])))
                    
                    annotator = Annotator(ax, pairs, data=data_filtered, x=x_col, y=y_col, hue=hue_col, order=group_order_str, hue_order=hue_order)
                    annotator.configure(test='Mann-Whitney', text_format=text_format, loc='inside' if text_format=='star' else 'outside', verbose=False)
                    annotator.apply_test()
                    annotator.annotate()
        except Exception as e:
            st.warning(f"Stats Calculation Error: {e}")

        # Formatting
        if custom_title:
             ax.set_title(custom_title, fontsize=12)
        
        if italic_xaxis and not metric_as_x:
             ax.set_xticklabels(ax.get_xticklabels(), fontstyle='italic')
        
        ax.set_xlabel(x_col if not metric_as_x else "") # Hide X label if metric mode (tick is enough)
        ax.set_ylabel(y_col)
        sns.despine()
        
        # Adjust Legend
        # If hue is active, place legend outside or top
        if plot_hue_col:
             plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
        st.pyplot(fig)
        
        get_download_buttons(fig, f"Bar_{y_col}", "bar", report_title=f"Bar Chart: {y_col} by {x_col}")

def render_survival_module(data):
    st.header("💀 生存分析 (Survival Analysis - KM)")
    cols = data.columns.tolist()
    
    c1, c2, c3 = st.columns(3)
    time_col = c1.selectbox("时间列 (Time)", cols, key="surv_time")
    event_col = c2.selectbox("事件列 (Event, 1=Dead)", cols, key="surv_event")
    group_col = c3.selectbox("分组列 (Group)", cols, key="surv_group")
    
    palette_name = st.selectbox("配色方案", list(PALETTES.keys()), index=0, key="surv_palette")
    
    if st.button("🚀 绘制生存曲线", type="primary"):
        st.session_state['surv_active'] = True

    if st.session_state.get('surv_active', False):
        st.divider()
        nature_style.apply_nature_style()
        fig, ax = plt.subplots(figsize=(6, 6))
        
        kmf = KaplanMeierFitter()
        groups = sorted(data[group_col].unique())
        colors = get_palette_colors(palette_name, n_colors=len(groups))
        
        results_text = []
        
        for i, g in enumerate(groups):
            mask = data[group_col] == g
            kmf.fit(data.loc[mask, time_col], data.loc[mask, event_col], label=str(g))
            kmf.plot_survival_function(ax=ax, ci_show=False, linewidth=2, color=colors[i])
            
        # Log-rank test
        if len(groups) == 2:
            g1, g2 = groups[0], groups[1]
            try:
                res = logrank_test(
                    data[data[group_col]==g1][time_col], data[data[group_col]==g2][time_col],
                    event_observed_A=data[data[group_col]==g1][event_col], event_observed_B=data[data[group_col]==g2][event_col]
                )
                p_val = res.p_value
                ax.text(0.05, 0.1, f"Log-rank p = {p_val:.4f}", transform=ax.transAxes, fontsize=10)
                results_text.append(f"Log-rank test ({g1} vs {g2}): p={p_val:.4f}")
            except Exception as e:
                st.write(f"Log-rank Warning: {e}")

        ax.set_xlabel("Time")
        ax.set_ylabel("Survival Probability")
        ax.set_ylim(0, 1.05)
        sns.despine()
        st.pyplot(fig)
        
        get_download_buttons(fig, "Survival_Curve", "surv", report_title="Kaplan-Meier Survival Analysis")

def render_heatmap_module(data):
    st.header("🔥 热图聚类 (Heatmap)")
    num_cols = data.select_dtypes(include=['number']).columns.tolist()
    all_cols = data.columns.tolist()
    
    cols = st.multiselect("数据列", num_cols, default=num_cols[:10])
    idx = st.selectbox("索引列 (Row Label)", ["Auto-Index"] + all_cols)
    
    if st.button("🚀 绘制热图", type="primary"):
        st.session_state['heat_active'] = True

    if st.session_state.get('heat_active', False):
        df_heat = data[cols].copy()
        if idx != "Auto-Index": df_heat.index = data[idx]
        df_heat = df_heat.dropna()
        
        nature_style.apply_nature_style()
        g = sns.clustermap(df_heat, z_score=0, cmap="vlag", center=0, figsize=(6,6))
        st.pyplot(g)
        get_download_buttons(g, "Heatmap", "heat", report_title="Hierarchical Clustering Heatmap")

def render_pca_module(data):
    st.header("🧬 PCA 分析 (3D Supported)")
    num_cols = data.select_dtypes(include=['number']).columns.tolist()
    feats = st.multiselect("特征列", num_cols, default=num_cols[:5])
    
    c1, c2 = st.columns(2)
    label = c1.selectbox("着色", data.columns)
    palette_name = c2.selectbox("配色方案", list(PALETTES.keys()), index=0, key="pca_palette")
    
    use_3d = st.checkbox("3D 模式")
    
    if st.button("🚀 运行 PCA"):
        st.session_state['pca_active'] = True

    if st.session_state.get('pca_active', False):
        df_pca = data[feats].dropna()
        scaler = StandardScaler()
        pcs = PCA(n_components=3).fit_transform(scaler.fit_transform(df_pca))
        pca_df = pd.DataFrame(pcs, columns=['PC1','PC2','PC3'])
        
        # Ensure label matches index of cleaned data
        labels_aligned = data.loc[df_pca.index, label].values
        pca_df['Label'] = labels_aligned
        
        unique_labels = sorted(list(set(labels_aligned)))
        colors = get_palette_colors(palette_name, n_colors=len(unique_labels))
        
        nature_style.apply_nature_style()
        fig = plt.figure(figsize=(6,6))
        
        if use_3d:
            ax = fig.add_subplot(111, projection='3d')
            # Manually map colors for 3D scatter
            color_map = {lbl: col for lbl, col in zip(unique_labels, colors)}
            c_array = [color_map[l] for l in pca_df['Label']]
            
            sc = ax.scatter(pca_df.PC1, pca_df.PC2, pca_df.PC3, c=c_array, s=50)
            
            # Create manual legend
            import matplotlib.patches as mpatches
            patches = [mpatches.Patch(color=color_map[l], label=l) for l in unique_labels]
            ax.legend(handles=patches)
            
        else:
            sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Label', palette=colors)
            
        st.pyplot(fig)
        get_download_buttons(fig, "PCA", "pca", report_title="PCA Analysis")

# --- Report Generation Page ---
def render_report_page():
    st.title("📝 实验报告生成 (Generator)")
    
    if not st.session_state['report_items']:
        st.info("购物车是空的。请在分析模块中点击 '➕ 添加到报告'。")
        return

    st.write(f"当前共有 {len(st.session_state['report_items'])} 个项目。")
    
    # Preview
    for i, item in enumerate(st.session_state['report_items']):
        with st.expander(f"{i+1}. {item['title']} ({item['time']})"):
            if item['text']: st.write(item['text'])
            if item['img_bytes']: st.image(item['img_bytes'])
            if item['df'] is not None: st.dataframe(item['df'])
            if st.button("❌ 删除", key=f"del_{i}"):
                st.session_state['report_items'].pop(i)
                st.rerun()

    if st.button("💾 生成 Word 报告 (.docx)", type="primary"):
        doc = Document()
        doc.add_heading('Bio-Analysis Experiment Report', 0)
        doc.add_paragraph(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        for item in st.session_state['report_items']:
            doc.add_heading(item['title'], level=1)
            
            if item['text']:
                doc.add_paragraph(item['text'])
            
            if item['img_bytes']:
                try:
                    doc.add_picture(io.BytesIO(item['img_bytes']), width=Inches(5.5))
                except Exception as e:
                    doc.add_paragraph(f"[Image Error: {e}]")
            
            if item['df'] is not None:
                # Add Table
                df = item['df']
                table = doc.add_table(rows=df.shape[0]+1, cols=df.shape[1])
                table.style = 'Table Grid'
                
                # Header
                for j, col_name in enumerate(df.columns):
                    table.cell(0, j).text = str(col_name)
                
                # Rows
                for r in range(df.shape[0]):
                    for c in range(df.shape[1]):
                        table.cell(r+1, c).text = str(df.iloc[r, c])
                doc.add_paragraph("") # Space
        
        # Save
        bio = io.BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="📥 点击下载 Word 报告",
            data=bio.getvalue(),
            file_name=f"Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# --- Data Format Guide ---
def render_data_guide():
    with st.expander("📌 数据格式指南 (Data Format Guide)", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 1. 长格式 (Long Format)")
            st.info("适用于：差异分析、生存分析 (Diff/Survival)")
            st.dataframe(pd.DataFrame({
                "Group": ["Ctrl", "Ctrl", "Treat", "Treat"],
                "Weight": [20.1, 20.5, 25.3, 24.8],
                "Time": [10, 12, 10, 11]
            }), height=150)
            
        with c2:
            st.markdown("### 2. 宽格式 (Wide Format)")
            st.info("适用于：PCA、热图 (PCA/Heatmap)")
            st.dataframe(pd.DataFrame({
                "Sample": ["S1", "S2", "S3"],
                "GeneA": [1.2, 5.6, 1.1],
                "GeneB": [3.4, 1.2, 3.5],
                "Group": ["WT", "KO", "WT"]
            }), height=150)

# --- Main App Structure ---
st.sidebar.title("控制面板")
mode = st.sidebar.radio("功能模块", [
    "🏠 首页 & 指南",
    "📊 箱线图 (Boxplot)",
    "📊 条形图",
    "💀 生存分析",
    "🧬 PCA (3D)",
    "🔥 热图聚类",
    "📈 相关性",
    "📝 导出报告"
])

if mode == "🏠 首页 & 指南":
    st.title("🧬 Bio-Analysis Suite v4.0")
    st.markdown("欢迎使用生物分析套件。请在左侧上传数据并选择模块。")
    render_data_guide()
    
elif mode == "📝 导出报告":
    render_report_page()
    
else:
    uploaded_file = st.sidebar.file_uploader("📂 上传 Excel/CSV 数据", type=['xlsx', 'csv'])
    if uploaded_file:
        data = load_data(uploaded_file)
        if data is not None:
            # Use the top-level 'mode' variable directly to cleaner logic
            if "描述" in mode: render_desc_stats(data)
            elif "箱线图" in mode: render_difference_module(data)
            elif "条形图" in mode: render_barplot_module(data)
            elif "PCA" in mode: render_pca_module(data)
            elif "热图" in mode: render_heatmap_module(data)
            elif "生存" in mode: render_survival_module(data)
            elif "相关" in mode: 
                # Re-implement simple correlation for v4
                st.header("📈 相关性分析")
                num_cols = data.select_dtypes(include=['number']).columns
                x = st.selectbox("X", num_cols, key="cx")
                y = st.selectbox("Y", num_cols, key="cy")
                
                col_w1, col_w2 = st.columns(2)
                fig_width = col_w1.slider("图表宽度 (inches)", 3, 15, 6)
                fig_height = col_w2.slider("图表高度 (inches)", 3, 15, 6)

                if st.button("Run"):
                    st.session_state['corr_active'] = True

                if st.session_state.get('corr_active', False):
                    nature_style.apply_nature_style()
                    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                    sns.regplot(data=data, x=x, y=y, ax=ax)
                    st.pyplot(fig)
                    get_download_buttons(fig, "Corr", "corr", report_title=f"Correlation {x} vs {y}")
    else:
        st.info("👈 请先上传数据")
