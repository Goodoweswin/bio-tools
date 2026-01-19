# 图表参数手动调优指南 (Code Parameter Adjustment Guide)

如果您觉得现在的自动布局（Single Metric Mode）还有瑕疵，可以通过修改 `public/tools/stat_analysis/app.py` 中的关键参数来微调。

## 📍 核心代码位置

修改文件: `/home/cy410080/biotools/bio-tools/public/tools/stat_analysis/app.py`

---

## 1. 调整 图表间距 (Padding) & 视觉宽度

在 "Barplot" (约 590行) 和 "Boxplot" (约 400行) 模块中，有一段控制 X轴范围的代码：

```python
# --- 原始代码 ---
if metric_as_x:
    real_width = 0.8  # [关键参数A] 物理宽度 (0.8是标准对齐值)
    
    # [关键参数B] 间距系数
    # 系数越大，两边留白越多，图看起来越"细"
    padding_factor = (1.1 - box_width) * 1.5 
    
    ax.set_xlim(-0.5 - padding_factor, 0.5 + padding_factor)
```

### 如何调整：
*   **想让图看起来更"细"**: 增大 `padding_factor` 的倍数 (比如把 `* 1.5` 改为 `* 2.0` 或 `* 3.0`)。
*   **想让图看起来更"胖"**: 减小倍数 (改为 `* 0.5`)。
*   **想改变物理宽度**: 修改 `real_width = 0.6` (注意：这可能会导致散点和柱子不对齐，需同步修改 stripplot 的 dodge 参数)。

---

## 2. 调整 统计标注的高度 (Stats Height)

如果您觉得 P值 (如 `p < 0.05`) 离柱子太近或太远，请查找 `annotator.configure`:

```python
# --- 原始代码 (约 688行 和 702行) ---
annotator.configure(
    test=None, 
    text_format=text_format, 
    loc='inside' ..., 
    line_offset=0.08,          # [关键参数C] 标注线距离图形的垂直距离
    line_offset_to_group=0.05  # [关键参数D] 组间标注的额外距离
)
```

### 如何调整：
*   **如果不希望标注压住散点**: 增大 `line_offset` (例如从 `0.08` 改为 `0.15` 或 `0.2`)。
*   **如果觉得标注飞得太高**: 减小该值。

---

## 3. 调整 散点样式 (Points Style)

查找 `sns.stripplot`:

```python
# --- 原始代码 (约 604行) ---
sns.stripplot(
    ...,
    size=5,             # [关键参数E] 点的大小
    alpha=0.9,          # [关键参数F] 透明度 (0~1)
    edgecolor="gray",   # [关键参数G] 描边颜色
    linewidth=1,        # [关键参数H] 描边粗细
    jitter=True         # [关键参数I] 抖动范围
)
```

### 常见调整：
*   **点太密**: 减小 `size` (如改为 `3`) 或 增大透明度 (减小 `alpha`)。
*   **点太散**: 修改 `jitter` (如改为 `jitter=0.1`)。

---

## 4. 调整 P值字体大小

在代码最后部分 (约 780行)，Seaborn 的字体受全局上下文控制，但也可用 `plt.setp` 强行修改：

```python
# 在 annotator.annotate() 之后添加:
for text in ax.texts:
    text.set_fontsize(12) # 修改为想要的字号
```

建议您每次只修改一个参数，保存后刷新网页查看效果。
