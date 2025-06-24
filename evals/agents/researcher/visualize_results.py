"""
Visualization tools for Web Researcher agent evaluation results.

This module provides comprehensive visualization capabilities for analyzing
evaluation results, including performance across domains, difficulty levels,
and individual metrics.
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class ResearcherResultsVisualizer:
    """Visualizer for researcher evaluation results."""
    
    def __init__(self, results_file: Optional[str] = None):
        """Initialize visualizer with optional results file."""
        self.results_file = results_file
        self.results = None
        if results_file:
            self.load_results(results_file)
    
    def load_results(self, results_file: str):
        """Load evaluation results from JSON file."""
        with open(results_file, 'r') as f:
            self.results = json.load(f)
    
    def create_comprehensive_dashboard(self, save_path: Optional[str] = None):
        """Create a comprehensive evaluation dashboard."""
        if not self.results:
            raise ValueError("No results loaded. Please load results first.")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # Plot 1: Overall Score Distribution
        ax1 = fig.add_subplot(gs[0, 0:2])
        self.plot_overall_score_distribution(ax1)
        
        # Plot 2: Performance by Domain
        ax2 = fig.add_subplot(gs[0, 2:4])
        self.plot_domain_performance(ax2)
        
        # Plot 3: Performance by Difficulty
        ax3 = fig.add_subplot(gs[1, 0:2])
        self.plot_difficulty_performance(ax3)
        
        # Plot 4: Metric Performance Heatmap
        ax4 = fig.add_subplot(gs[1, 2:4])
        self.plot_metric_heatmap(ax4)
        
        # Plot 5: Search Quality vs Crawling Quality
        ax5 = fig.add_subplot(gs[2, 0:2])
        self.plot_search_vs_crawling_quality(ax5)
        
        # Plot 6: Source Quality Distribution
        ax6 = fig.add_subplot(gs[2, 2:4])
        self.plot_source_quality_distribution(ax6)
        
        # Plot 7: Information Synthesis Performance
        ax7 = fig.add_subplot(gs[3, 0:2])
        self.plot_synthesis_performance(ax7)
        
        # Plot 8: RAG Effectiveness Analysis
        ax8 = fig.add_subplot(gs[3, 2:4])
        self.plot_rag_effectiveness(ax8)
        
        plt.suptitle('Web Researcher Agent - Comprehensive Evaluation Dashboard', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_overall_score_distribution(self, ax):
        """Plot distribution of overall scores."""
        results = self.results['detailed_results']
        scores = [r.get('overall_score', 0) for r in results if 'overall_score' in r]
        
        ax.hist(scores, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        ax.axvline(np.mean(scores), color='red', linestyle='--', 
                  label=f'Mean: {np.mean(scores):.2f}')
        ax.set_xlabel('Overall Score')
        ax.set_ylabel('Frequency')
        ax.set_title('Overall Score Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_domain_performance(self, ax):
        """Plot performance across different domains."""
        results = self.results['detailed_results']
        
        domain_scores = {}
        for result in results:
            if 'overall_score' in result and 'domain' in result:
                domain = result['domain']
                score = result['overall_score']
                if domain not in domain_scores:
                    domain_scores[domain] = []
                domain_scores[domain].append(score)
        
        domains = list(domain_scores.keys())
        avg_scores = [np.mean(domain_scores[domain]) for domain in domains]
        std_scores = [np.std(domain_scores[domain]) for domain in domains]
        
        bars = ax.bar(domains, avg_scores, yerr=std_scores, capsize=5, 
                     alpha=0.7, color='lightgreen', edgecolor='black')
        ax.set_xlabel('Domain')
        ax.set_ylabel('Average Score')
        ax.set_title('Performance by Domain')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, score in zip(bars, avg_scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{score:.2f}', ha='center', va='bottom')
    
    def plot_difficulty_performance(self, ax):
        """Plot performance across difficulty levels."""
        results = self.results['detailed_results']
        
        difficulty_scores = {}
        for result in results:
            if 'overall_score' in result and 'difficulty' in result:
                difficulty = result['difficulty']
                score = result['overall_score']
                if difficulty not in difficulty_scores:
                    difficulty_scores[difficulty] = []
                difficulty_scores[difficulty].append(score)
        
        difficulties = ['basic', 'intermediate', 'expert']  # Ordered by complexity
        avg_scores = [np.mean(difficulty_scores.get(diff, [0])) for diff in difficulties]
        
        colors = ['green', 'orange', 'red']
        bars = ax.bar(difficulties, avg_scores, color=colors, alpha=0.7, edgecolor='black')
        ax.set_xlabel('Difficulty Level')
        ax.set_ylabel('Average Score')
        ax.set_title('Performance by Difficulty Level')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, score in zip(bars, avg_scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{score:.2f}', ha='center', va='bottom')
    
    def plot_metric_heatmap(self, ax):
        """Plot heatmap of metric performance across test cases."""
        results = self.results['detailed_results']
        
        metrics = ['search_quality', 'crawling_quality', 'information_synthesis', 
                  'source_quality', 'research_completeness']
        
        # Create matrix of scores
        score_matrix = []
        test_case_ids = []
        
        for result in results:
            if 'individual_scores' in result:
                test_case_ids.append(result.get('test_case_id', 'Unknown'))
                row = []
                for metric in metrics:
                    if metric in result['individual_scores']:
                        score = result['individual_scores'][metric].get('score', 0)
                    else:
                        score = 0
                    row.append(score)
                score_matrix.append(row)
        
        if score_matrix:
            df = pd.DataFrame(score_matrix, columns=metrics, index=test_case_ids)
            sns.heatmap(df, annot=True, cmap='RdYlGn', vmin=0, vmax=1, 
                       ax=ax, cbar_kws={'label': 'Score'})
            ax.set_title('Metric Performance Heatmap')
            ax.set_xlabel('Metrics')
            ax.set_ylabel('Test Cases')
    
    def plot_search_vs_crawling_quality(self, ax):
        """Plot search quality vs crawling quality scatter plot."""
        results = self.results['detailed_results']
        
        search_scores = []
        crawling_scores = []
        domains = []
        
        for result in results:
            if 'individual_scores' in result:
                search_score = result['individual_scores'].get('search_quality', {}).get('score', 0)
                crawling_score = result['individual_scores'].get('crawling_quality', {}).get('score', 0)
                domain = result.get('domain', 'unknown')
                
                search_scores.append(search_score)
                crawling_scores.append(crawling_score)
                domains.append(domain)
        
        # Create scatter plot with different colors for domains
        unique_domains = list(set(domains))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_domains)))
        
        for i, domain in enumerate(unique_domains):
            domain_indices = [j for j, d in enumerate(domains) if d == domain]
            domain_search = [search_scores[j] for j in domain_indices]
            domain_crawling = [crawling_scores[j] for j in domain_indices]
            
            ax.scatter(domain_search, domain_crawling, c=[colors[i]], 
                      label=domain, alpha=0.7, s=50)
        
        ax.set_xlabel('Search Quality Score')
        ax.set_ylabel('Crawling Quality Score')
        ax.set_title('Search Quality vs Crawling Quality')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Add diagonal line for reference
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Perfect Correlation')
    
    def plot_source_quality_distribution(self, ax):
        """Plot distribution of source quality scores."""
        results = self.results['detailed_results']
        
        source_scores = []
        for result in results:
            if 'individual_scores' in result:
                score = result['individual_scores'].get('source_quality', {}).get('score', 0)
                source_scores.append(score)
        
        ax.hist(source_scores, bins=10, alpha=0.7, color='coral', edgecolor='black')
        ax.axvline(np.mean(source_scores), color='red', linestyle='--', 
                  label=f'Mean: {np.mean(source_scores):.2f}')
        ax.set_xlabel('Source Quality Score')
        ax.set_ylabel('Frequency')
        ax.set_title('Source Quality Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def plot_synthesis_performance(self, ax):
        """Plot information synthesis performance across domains."""
        results = self.results['detailed_results']
        
        domain_synthesis = {}
        for result in results:
            if 'individual_scores' in result and 'domain' in result:
                domain = result['domain']
                score = result['individual_scores'].get('information_synthesis', {}).get('score', 0)
                
                if domain not in domain_synthesis:
                    domain_synthesis[domain] = []
                domain_synthesis[domain].append(score)
        
        domains = list(domain_synthesis.keys())
        avg_scores = [np.mean(domain_synthesis[domain]) for domain in domains]
        
        bars = ax.bar(domains, avg_scores, alpha=0.7, color='purple', edgecolor='black')
        ax.set_xlabel('Domain')
        ax.set_ylabel('Information Synthesis Score')
        ax.set_title('Information Synthesis Performance by Domain')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, score in zip(bars, avg_scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{score:.2f}', ha='center', va='bottom')
    
    def plot_rag_effectiveness(self, ax):
        """Plot RAG effectiveness analysis."""
        results = self.results['detailed_results']
        
        # Combine search, crawling, and synthesis as RAG components
        rag_scores = []
        test_cases = []
        
        for result in results:
            if 'individual_scores' in result:
                search = result['individual_scores'].get('search_quality', {}).get('score', 0)
                crawling = result['individual_scores'].get('crawling_quality', {}).get('score', 0)
                synthesis = result['individual_scores'].get('information_synthesis', {}).get('score', 0)
                
                # Calculate composite RAG score
                rag_score = (search + crawling + synthesis) / 3
                rag_scores.append(rag_score)
                test_cases.append(result.get('test_case_id', 'Unknown'))
        
        # Plot top and bottom performers
        sorted_data = sorted(zip(rag_scores, test_cases), reverse=True)
        top_5 = sorted_data[:5]
        bottom_5 = sorted_data[-5:]
        
        y_pos = np.arange(len(top_5))
        
        # Top performers
        ax.barh(y_pos, [score for score, _ in top_5], alpha=0.7, color='green')
        ax.set_yticks(y_pos)
        ax.set_yticklabels([case for _, case in top_5])
        ax.set_xlabel('RAG Effectiveness Score')
        ax.set_title('Top 5 RAG Performance')
        ax.grid(True, alpha=0.3)
    
    def generate_detailed_report(self, save_path: Optional[str] = None):
        """Generate a detailed text report of evaluation results."""
        if not self.results:
            raise ValueError("No results loaded. Please load results first.")
        
        report = []
        report.append("="*80)
        report.append("WEB RESEARCHER AGENT - DETAILED EVALUATION REPORT")
        report.append("="*80)
        report.append("")
        
        # Summary statistics
        summary = self.results.get('summary', {})
        report.append("SUMMARY STATISTICS:")
        report.append(f"Total Test Cases: {summary.get('total_test_cases', 'N/A')}")
        report.append(f"Successful Evaluations: {summary.get('successful_evaluations', 'N/A')}")
        report.append(f"Failed Evaluations: {summary.get('failed_evaluations', 'N/A')}")
        report.append(f"Overall Score: {summary.get('overall_score', 'N/A'):.2f}")
        report.append("")
        
        # Domain analysis
        results = self.results['detailed_results']
        domain_analysis = {}
        for result in results:
            if 'overall_score' in result and 'domain' in result:
                domain = result['domain']
                score = result['overall_score']
                if domain not in domain_analysis:
                    domain_analysis[domain] = []
                domain_analysis[domain].append(score)
        
        report.append("DOMAIN PERFORMANCE:")
        for domain, scores in domain_analysis.items():
            avg_score = np.mean(scores)
            std_score = np.std(scores)
            report.append(f"{domain}: {avg_score:.2f} (±{std_score:.2f}) [{len(scores)} cases]")
        report.append("")
        
        # Metric analysis
        metrics = ['search_quality', 'crawling_quality', 'information_synthesis', 
                  'source_quality', 'research_completeness']
        
        report.append("METRIC PERFORMANCE:")
        for metric in metrics:
            scores = []
            for result in results:
                if 'individual_scores' in result and metric in result['individual_scores']:
                    scores.append(result['individual_scores'][metric].get('score', 0))
            
            if scores:
                avg_score = np.mean(scores)
                std_score = np.std(scores)
                report.append(f"{metric}: {avg_score:.2f} (±{std_score:.2f})")
        
        report_text = "\n".join(report)
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)
            print(f"Report saved to: {save_path}")
        
        return report_text


def visualize_results(results_file: str, output_dir: str = "evals/outputs/researcher/visualizations"):
    """Main function to create all visualizations."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize visualizer
    visualizer = ResearcherResultsVisualizer(results_file)
    
    # Create comprehensive dashboard
    print("Creating comprehensive dashboard...")
    visualizer.create_comprehensive_dashboard(
        save_path=output_path / "comprehensive_dashboard.png"
    )
    
    # Generate detailed report
    print("Generating detailed report...")
    visualizer.generate_detailed_report(
        save_path=output_path / "detailed_report.txt"
    )
    
    print(f"Visualizations saved to: {output_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python visualize_results.py <results_file>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    visualize_results(results_file) 