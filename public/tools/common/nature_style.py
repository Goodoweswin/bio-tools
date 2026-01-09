import matplotlib.pyplot as plt
import seaborn as sns

def apply_nature_style():
    """
    Applies publication-quality (Nature-style) settings to matplotlib and seaborn.
    Call this function before plotting.
    """
    # Font settings (Arial/Helvetica is standard)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']
    
    # Font sizes
    plt.rcParams['font.size'] = 8         # Main text/axes: 7-9pt
    plt.rcParams['axes.labelsize'] = 9    # Axis labels
    plt.rcParams['axes.titlesize'] = 10   # Titles
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 8
    
    # Line weights
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['grid.linewidth'] = 0.5
    plt.rcParams['lines.linewidth'] = 1.0
    plt.rcParams['lines.markersize'] = 4
    
    # PDF export settings (Text as paths vs vectors)
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    
    # General Aesthetic
    sns.set_context("paper", rc={"font.size":8,"axes.titlesize":10,"axes.labelsize":9}) 
    sns.set_style("ticks") # Ticks only, no background grid (Publication standard)
    
    return "Nature-style plotting parameters applied."
