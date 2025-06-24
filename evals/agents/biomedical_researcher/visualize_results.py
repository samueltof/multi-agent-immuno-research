#!/usr/bin/env python3
"""
Visualization script for biomedical researcher evaluation results.
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np


def load_latest_results(output_dir: str = "evals/outputs/biomedical_researcher") -> Optional[Dict[str, Any]]:
    """Load the most recent visualization data file."""
    output_path = Path(output_dir)
    
    # Find the most recent visualization data file
    viz_files = list(output_path.glob("biomedical_researcher_visualization_data_*.json"))
    if not viz_files:
        print("❌ No visualization data files found!")
        return None
    
    latest_file = max(viz_files, key=lambda f: f.stat().st_mtime)
    print(f"📊 Loading visualization data from: {latest_file}")
    
    with open(latest_file, 'r') as f:
        return json.load(f)


def create_domain_performance_plot(data: Dict[str, Any], save_path: Optional[str] = None):
    """Create a bar plot showing performance by domain."""
    domain_analysis = data["domain_analysis"]
    
    domains = list(domain_analysis.keys())
    avg_scores = [domain_analysis[domain]["average_score"] for domain in domains]
    counts = [domain_analysis[domain]["count"] for domain in domains]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Average scores by domain
    bars1 = ax1.bar(domains, avg_scores, color='skyblue', alpha=0.7)
    ax1.set_title('Average Performance by Medical Domain', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Average Score', fontsize=12)
    ax1.set_xlabel('Medical Domain', fontsize=12)
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, score in zip(bars1, avg_scores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Test case counts by domain
    bars2 = ax2.bar(domains, counts, color='lightcoral', alpha=0.7)
    ax2.set_title('Test Cases by Medical Domain', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Number of Test Cases', fontsize=12)
    ax2.set_xlabel('Medical Domain', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, count in zip(bars2, counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📈 Domain performance plot saved to: {save_path}")
    
    plt.show()


def create_metrics_heatmap(data: Dict[str, Any], save_path: Optional[str] = None):
    """Create a heatmap showing metric performance across domains."""
    domain_analysis = data["domain_analysis"]
    metrics = data["metadata"]["metrics"]
    
    # Prepare data for heatmap
    heatmap_data = []
    domains = list(domain_analysis.keys())
    
    for domain in domains:
        row = []
        for metric in metrics:
            avg_score = domain_analysis[domain]["metrics"][metric]["average"]
            row.append(avg_score)
        heatmap_data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(heatmap_data, 
                     index=[domain.replace('_', ' ').title() for domain in domains],
                     columns=[metric.replace('_', ' ').title() for metric in metrics])
    
    # Create heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df, annot=True, cmap='RdYlGn', center=0.5, 
                vmin=0, vmax=1, fmt='.3f', cbar_kws={'label': 'Score'})
    plt.title('Evaluation Metrics Heatmap by Medical Domain', fontsize=16, fontweight='bold')
    plt.xlabel('Evaluation Metrics', fontsize=12)
    plt.ylabel('Medical Domains', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"🔥 Metrics heatmap saved to: {save_path}")
    
    plt.show()


def create_difficulty_analysis(data: Dict[str, Any], save_path: Optional[str] = None):
    """Create a plot showing performance by difficulty level."""
    difficulty_analysis = data["difficulty_analysis"]
    
    difficulties = list(difficulty_analysis.keys())
    avg_scores = [difficulty_analysis[diff]["average_score"] for diff in difficulties]
    counts = [difficulty_analysis[diff]["count"] for diff in difficulties]
    
    # Sort by difficulty level
    difficulty_order = ["basic", "intermediate", "expert"]
    sorted_data = [(diff, avg_scores[difficulties.index(diff)], counts[difficulties.index(diff)]) 
                   for diff in difficulty_order if diff in difficulties]
    
    if sorted_data:
        difficulties, avg_scores, counts = zip(*sorted_data)
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    x = np.arange(len(difficulties))
    width = 0.6
    
    bars = ax.bar(x, avg_scores, width, color=['lightgreen', 'orange', 'lightcoral'], alpha=0.7)
    
    ax.set_title('Performance by Difficulty Level', fontsize=14, fontweight='bold')
    ax.set_ylabel('Average Score', fontsize=12)
    ax.set_xlabel('Difficulty Level', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels([diff.title() for diff in difficulties])
    ax.set_ylim(0, 1)
    
    # Add value labels and counts
    for i, (bar, score, count) in enumerate(zip(bars, avg_scores, counts)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{score:.3f}\n({count} cases)', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Difficulty analysis plot saved to: {save_path}")
    
    plt.show()


def create_overall_summary_plot(data: Dict[str, Any], save_path: Optional[str] = None):
    """Create a comprehensive summary plot."""
    individual_results = data["individual_results"]
    metadata = data["metadata"]
    
    # Extract scores
    overall_scores = [result["overall_score"] for result in individual_results]
    factual_scores = [result["factual_correctness_score"] for result in individual_results]
    relevance_scores = [result["relevance_score"] for result in individual_results]
    source_scores = [result["source_quality_score"] for result in individual_results]
    confidence_scores = [result["confidence_alignment_score"] for result in individual_results]
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Overall score distribution
    ax1.hist(overall_scores, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_title('Overall Score Distribution', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Overall Score')
    ax1.set_ylabel('Frequency')
    ax1.axvline(np.mean(overall_scores), color='red', linestyle='--', 
                label=f'Mean: {np.mean(overall_scores):.3f}')
    ax1.legend()
    
    # Individual metrics comparison
    metric_names = ['Factual\nCorrectness', 'Relevance', 'Source\nQuality', 'Confidence\nAlignment']
    metric_scores = [
        np.mean(factual_scores),
        np.mean(relevance_scores), 
        np.mean(source_scores),
        np.mean(confidence_scores)
    ]
    
    bars = ax2.bar(metric_names, metric_scores, color=['green', 'blue', 'orange', 'purple'], alpha=0.7)
    ax2.set_title('Average Metric Performance', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Score')
    ax2.set_ylim(0, 1)
    
    for bar, score in zip(bars, metric_scores):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Score correlation matrix
    scores_df = pd.DataFrame({
        'Overall': overall_scores,
        'Factual': factual_scores,
        'Relevance': relevance_scores,
        'Source': source_scores,
        'Confidence': confidence_scores
    })
    
    corr_matrix = scores_df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax3,
                fmt='.2f', square=True)
    ax3.set_title('Score Correlation Matrix', fontsize=12, fontweight='bold')
    
    # Summary statistics
    stats_text = f"""
    Total Test Cases: {metadata['total_test_cases']}
    Evaluator Model: {metadata['evaluator_model']}
    
    Overall Performance:
    • Mean Score: {np.mean(overall_scores):.3f}
    • Std Dev: {np.std(overall_scores):.3f}
    • Min Score: {np.min(overall_scores):.3f}
    • Max Score: {np.max(overall_scores):.3f}
    
    Domains Tested: {len(metadata['domains'])}
    • {', '.join(metadata['domains'])}
    """
    
    ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('Evaluation Summary', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📋 Summary plot saved to: {save_path}")
    
    plt.show()


def main():
    """Main function to generate all visualization plots."""
    print("📊 BIOMEDICAL RESEARCHER EVALUATION - VISUALIZATION")
    print("=" * 60)
    
    # Load data
    data = load_latest_results()
    if not data:
        return
    
    # Create output directory for plots
    plots_dir = Path("evals/outputs/biomedical_researcher/plots")
    plots_dir.mkdir(exist_ok=True)
    
    timestamp = data["metadata"]["timestamp"].replace(":", "-").replace(".", "-")
    
    # Generate all plots
    print("\n🎨 Generating visualization plots...")
    
    create_domain_performance_plot(data, plots_dir / f"domain_performance_{timestamp}.png")
    create_metrics_heatmap(data, plots_dir / f"metrics_heatmap_{timestamp}.png")
    create_difficulty_analysis(data, plots_dir / f"difficulty_analysis_{timestamp}.png")
    create_overall_summary_plot(data, plots_dir / f"summary_overview_{timestamp}.png")
    
    print(f"\n✅ All plots saved to: {plots_dir}")
    print("📊 Visualization complete!")


if __name__ == "__main__":
    main() 