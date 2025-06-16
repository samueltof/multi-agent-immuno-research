import streamlit as st
import base64
import re
from pathlib import Path
from typing import List, Optional, Dict
import os

def extract_plot_paths_from_content(content: str) -> List[str]:
    """Extract plot file paths from agent response content"""
    plot_paths = []
    
    # Look for explicit plot path patterns
    patterns = [
        r'PLOT_SAVED: (.+\.png)',
        r'Plot saved as [\'"](.+\.png)[\'"]',
        r'outputs/plots/(.+\.png)',
        r'plots/(.+\.png)',  # Legacy support
        r'- (.+\.png)',  # From the modified python_repl output
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            # Clean up the path
            plot_path = match.strip()
            if os.path.exists(plot_path):
                plot_paths.append(plot_path)
    
    return plot_paths

def get_image_base64(image_path: str) -> Optional[str]:
    """Convert image file to base64 string for display"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image {image_path}: {e}")
        return None

def display_plots(plot_paths: List[str], title: str = "Generated Plots") -> None:
    """Display plots in Streamlit interface"""
    if not plot_paths:
        return
    
    st.markdown(f"### 📊 {title}")
    
    # Display plots in columns if multiple
    if len(plot_paths) == 1:
        # Single plot - full width
        plot_path = plot_paths[0]
        if os.path.exists(plot_path):
            st.image(plot_path, caption=f"Plot: {Path(plot_path).name}")
    else:
        # Multiple plots - in columns
        cols = st.columns(min(len(plot_paths), 3))  # Max 3 columns
        for idx, plot_path in enumerate(plot_paths):
            if os.path.exists(plot_path):
                with cols[idx % 3]:
                    st.image(plot_path, caption=f"Plot {idx + 1}: {Path(plot_path).name}")

def display_plots_in_message(content: str) -> str:
    """Display plots found in message content and return cleaned content"""
    plot_paths = extract_plot_paths_from_content(content)
    
    if plot_paths:
        display_plots(plot_paths)
        
        # Clean the content to remove plot path references
        cleaned_content = content
        for plot_path in plot_paths:
            # Remove various plot path patterns
            patterns_to_remove = [
                f"PLOT_SAVED: {plot_path}",
                f"Plot saved as '{plot_path}'",
                f"Plot saved as \"{plot_path}\"",
                f"- {plot_path}",
                f"Plots generated:\n- {plot_path}",
                f"\n\nPlots generated:\n- {plot_path}",
            ]
            
            for pattern in patterns_to_remove:
                cleaned_content = cleaned_content.replace(pattern, "")
        
        # Clean up extra newlines
        cleaned_content = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_content)
        cleaned_content = cleaned_content.strip()
        
        return cleaned_content
    
    return content

def create_download_button_for_plots(plot_paths: List[str]) -> None:
    """Create download buttons for generated plots"""
    if not plot_paths:
        return
    
    st.markdown("### 📥 Download Plots")
    
    for plot_path in plot_paths:
        if os.path.exists(plot_path):
            plot_name = Path(plot_path).name
            with open(plot_path, "rb") as file:
                st.download_button(
                    label=f"Download {plot_name}",
                    data=file.read(),
                    file_name=plot_name,
                    mime="image/png",
                    key=f"download_{plot_name}"
                )

def display_plots_with_html(plot_paths: List[str]) -> str:
    """Generate HTML for displaying plots inline with chat messages"""
    if not plot_paths:
        return ""
    
    html_parts = []
    html_parts.append('<div style="margin: 1rem 0;">')
    html_parts.append('<div style="font-weight: 600; color: #1e3a8a; margin-bottom: 0.5rem;">📊 Generated Plots:</div>')
    
    for plot_path in plot_paths:
        if os.path.exists(plot_path):
            img_base64 = get_image_base64(plot_path)
            if img_base64:
                plot_name = Path(plot_path).name
                html_parts.append(f'''
                <div style="margin: 0.5rem 0; padding: 0.5rem; border: 1px solid #e2e8f0; border-radius: 8px; background: white;">
                    <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">{plot_name}</div>
                    <img src="data:image/png;base64,{img_base64}" 
                         style="max-width: 100%; height: auto; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" 
                         alt="{plot_name}" />
                </div>
                ''')
    
    html_parts.append('</div>')
    return ''.join(html_parts)

def cleanup_old_plots(max_plots: int = 100) -> None:
    """Clean up old plot files to prevent disk space issues"""
    plots_dir = Path("outputs/plots")
    if not plots_dir.exists():
        return
    
    # Get all plot files sorted by creation time
    plot_files = [f for f in plots_dir.glob("*.png") if f.is_file()]
    plot_files.sort(key=lambda x: x.stat().st_ctime, reverse=True)
    
    # Remove old files if we exceed max_plots
    if len(plot_files) > max_plots:
        for plot_file in plot_files[max_plots:]:
            try:
                plot_file.unlink()
            except Exception as e:
                st.warning(f"Could not delete old plot file {plot_file.name}: {e}") 