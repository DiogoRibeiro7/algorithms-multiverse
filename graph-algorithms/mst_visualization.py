"""
MST Visualization Module
========================

Provides interactive visualization of MST algorithm execution:
- Step-by-step construction visualization
- Side-by-side algorithm comparison
- Network graph representation
- Animation of edge selection process
- Real-world network design examples

Requires: matplotlib, networkx
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
import networkx as nx
from typing import List, Tuple, Dict
from mst_algorithms import MSTAlgorithms, Edge
import numpy as np


class MSTVisualizer:
    """Visualizer for MST algorithms"""

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int, float]]):
        """
        Initialize visualizer

        Args:
            num_vertices: Number of vertices
            edges: List of (u, v, weight) tuples
        """
        self.num_vertices = num_vertices
        self.edges = edges
        self.mst = MSTAlgorithms(num_vertices, edges)

        # Create NetworkX graph for layout
        self.G = nx.Graph()
        for u, v, w in edges:
            self.G.add_edge(u, v, weight=w)

        # Compute spring layout for nice visualization
        self.pos = nx.spring_layout(self.G, k=2, iterations=50, seed=42)

    def visualize_kruskal(self, save_path: str = None, show_animation: bool = True):
        """
        Visualize Kruskal's algorithm step by step

        Args:
            save_path: Path to save animation (optional)
            show_animation: Whether to show animation in window
        """
        _, _, steps = self.mst.kruskal_with_visualization()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle("Kruskal's MST Algorithm Visualization", fontsize=16, fontweight='bold')

        def update(frame):
            ax1.clear()
            ax2.clear()

            step = steps[frame]
            iteration = step['iteration']
            edge_considered = step['edge_considered']
            action = step['action']
            mst_edges = step['mst_so_far']
            total_weight = step['total_weight']

            # Left panel: Graph visualization
            ax1.set_title(f"Step {iteration + 1}: Edge ({edge_considered.u}, {edge_considered.v}) - {action}")
            ax1.axis('off')

            # Draw all edges in light gray
            for u, v, w in self.edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                ax1.plot([x1, x2], [y1, y2], 'gray', alpha=0.3, linewidth=1, zorder=1)

            # Draw MST edges in green
            for edge in mst_edges:
                x1, y1 = self.pos[edge.u]
                x2, y2 = self.pos[edge.v]
                ax1.plot([x1, x2], [y1, y2], 'green', linewidth=3, zorder=2)
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                ax1.text(mid_x, mid_y, f'{edge.weight:.0f}',
                        fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='lightgreen'))

            # Draw current edge being considered
            x1, y1 = self.pos[edge_considered.u]
            x2, y2 = self.pos[edge_considered.v]
            color = 'green' if action == 'added' else 'red'
            ax1.plot([x1, x2], [y1, y2], color, linewidth=3, linestyle='--', zorder=3)

            # Draw vertices
            for node in self.G.nodes():
                x, y = self.pos[node]
                circle = plt.Circle((x, y), 0.08, color='skyblue', zorder=4)
                ax1.add_patch(circle)
                ax1.text(x, y, str(node), fontsize=12, ha='center', va='center',
                        fontweight='bold', zorder=5)

            # Right panel: Algorithm state
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.axis('off')

            # Display algorithm info
            info_text = [
                f"Algorithm: Kruskal's",
                f"Iteration: {iteration + 1}/{len(steps)}",
                f"",
                f"Current Edge: ({edge_considered.u}, {edge_considered.v})",
                f"Edge Weight: {edge_considered.weight:.2f}",
                f"Action: {action}",
                f"",
                f"MST Edges: {len(mst_edges)}/{self.num_vertices - 1}",
                f"Total Weight: {total_weight:.2f}",
            ]

            y_pos = 0.9
            for text in info_text:
                if text == "":
                    y_pos -= 0.03
                else:
                    ax2.text(0.1, y_pos, text, fontsize=12, verticalalignment='top', fontfamily='monospace')
                    y_pos -= 0.06

            # Show edge list
            ax2.text(0.1, y_pos - 0.05, "MST Edges So Far:", fontsize=12, fontweight='bold')
            y_pos -= 0.1
            for i, edge in enumerate(mst_edges[-5:]):  # Show last 5 edges
                ax2.text(0.15, y_pos, f"({edge.u}, {edge.v}): {edge.weight:.2f}",
                        fontsize=10, fontfamily='monospace')
                y_pos -= 0.05

        anim = animation.FuncAnimation(fig, update, frames=len(steps),
                                      interval=1000, repeat=True)

        if save_path:
            anim.save(save_path, writer='pillow', fps=1)

        if show_animation:
            plt.show()

        return anim

    def visualize_prim(self, save_path: str = None, show_animation: bool = True):
        """
        Visualize Prim's algorithm step by step

        Args:
            save_path: Path to save animation (optional)
            show_animation: Whether to show animation in window
        """
        _, _, steps = self.mst.prim_with_visualization(start=0)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle("Prim's MST Algorithm Visualization", fontsize=16, fontweight='bold')

        def update(frame):
            ax1.clear()
            ax2.clear()

            step = steps[frame]
            iteration = step['iteration']
            edge_considered = step['edge_considered']
            action = step['action']
            mst_edges = step['mst_so_far']
            visited = step['visited']
            total_weight = step['total_weight']

            # Left panel: Graph visualization
            ax1.set_title(f"Step {iteration + 1}: Edge ({edge_considered.u}, {edge_considered.v}) - {action}")
            ax1.axis('off')

            # Draw all edges in light gray
            for u, v, w in self.edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                ax1.plot([x1, x2], [y1, y2], 'gray', alpha=0.3, linewidth=1, zorder=1)

            # Draw MST edges in green
            for edge in mst_edges:
                x1, y1 = self.pos[edge.u]
                x2, y2 = self.pos[edge.v]
                ax1.plot([x1, x2], [y1, y2], 'green', linewidth=3, zorder=2)
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                ax1.text(mid_x, mid_y, f'{edge.weight:.0f}',
                        fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='lightgreen'))

            # Draw current edge being considered
            x1, y1 = self.pos[edge_considered.u]
            x2, y2 = self.pos[edge_considered.v]
            color = 'green' if action == 'added' else 'orange'
            ax1.plot([x1, x2], [y1, y2], color, linewidth=3, linestyle='--', zorder=3)

            # Draw vertices (color visited nodes differently)
            for node in self.G.nodes():
                x, y = self.pos[node]
                node_color = 'lightgreen' if node in visited else 'lightgray'
                circle = plt.Circle((x, y), 0.08, color=node_color, zorder=4)
                ax1.add_patch(circle)
                ax1.text(x, y, str(node), fontsize=12, ha='center', va='center',
                        fontweight='bold', zorder=5)

            # Right panel: Algorithm state
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.axis('off')

            # Display algorithm info
            info_text = [
                f"Algorithm: Prim's",
                f"Iteration: {iteration + 1}/{len(steps)}",
                f"",
                f"Current Edge: ({edge_considered.u}, {edge_considered.v})",
                f"Edge Weight: {edge_considered.weight:.2f}",
                f"Action: {action}",
                f"",
                f"Visited Vertices: {len(visited)}",
                f"MST Edges: {len(mst_edges)}/{self.num_vertices - 1}",
                f"Total Weight: {total_weight:.2f}",
            ]

            y_pos = 0.9
            for text in info_text:
                if text == "":
                    y_pos -= 0.03
                else:
                    ax2.text(0.1, y_pos, text, fontsize=12, verticalalignment='top', fontfamily='monospace')
                    y_pos -= 0.06

        anim = animation.FuncAnimation(fig, update, frames=len(steps),
                                      interval=1000, repeat=True)

        if save_path:
            anim.save(save_path, writer='pillow', fps=1)

        if show_animation:
            plt.show()

        return anim

    def visualize_boruvka(self, save_path: str = None, show_animation: bool = True):
        """
        Visualize Borůvka's algorithm step by step

        Args:
            save_path: Path to save animation (optional)
            show_animation: Whether to show animation in window
        """
        _, _, steps = self.mst.boruvka_with_visualization()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle("Borůvka's MST Algorithm Visualization", fontsize=16, fontweight='bold')

        def update(frame):
            ax1.clear()
            ax2.clear()

            step = steps[frame]
            phase = step['phase']
            edges_added = step['edges_added']
            num_components = step['num_components']
            mst_edges = step['mst_so_far']
            total_weight = step['total_weight']

            # Left panel: Graph visualization
            ax1.set_title(f"Phase {phase + 1}: Added {len(edges_added)} edges ({num_components} components remaining)")
            ax1.axis('off')

            # Draw all edges in light gray
            for u, v, w in self.edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                ax1.plot([x1, x2], [y1, y2], 'gray', alpha=0.3, linewidth=1, zorder=1)

            # Draw previous MST edges in green
            prev_edges = mst_edges[:-len(edges_added)] if edges_added else mst_edges
            for edge in prev_edges:
                x1, y1 = self.pos[edge.u]
                x2, y2 = self.pos[edge.v]
                ax1.plot([x1, x2], [y1, y2], 'green', linewidth=3, zorder=2)

            # Draw edges added in this phase in bright green
            for edge in edges_added:
                x1, y1 = self.pos[edge.u]
                x2, y2 = self.pos[edge.v]
                ax1.plot([x1, x2], [y1, y2], 'lime', linewidth=4, zorder=3)
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                ax1.text(mid_x, mid_y, f'{edge.weight:.0f}',
                        fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='yellow'))

            # Draw vertices
            for node in self.G.nodes():
                x, y = self.pos[node]
                circle = plt.Circle((x, y), 0.08, color='skyblue', zorder=4)
                ax1.add_patch(circle)
                ax1.text(x, y, str(node), fontsize=12, ha='center', va='center',
                        fontweight='bold', zorder=5)

            # Right panel: Algorithm state
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
            ax2.axis('off')

            # Display algorithm info
            info_text = [
                f"Algorithm: Borůvka's",
                f"Phase: {phase + 1}/{len(steps)}",
                f"",
                f"Edges Added This Phase: {len(edges_added)}",
                f"Components Remaining: {num_components}",
                f"",
                f"Total MST Edges: {len(mst_edges)}/{self.num_vertices - 1}",
                f"Total Weight: {total_weight:.2f}",
            ]

            y_pos = 0.9
            for text in info_text:
                if text == "":
                    y_pos -= 0.03
                else:
                    ax2.text(0.1, y_pos, text, fontsize=12, verticalalignment='top', fontfamily='monospace')
                    y_pos -= 0.06

            # Show edges added in this phase
            if edges_added:
                ax2.text(0.1, y_pos - 0.05, "Edges Added This Phase:", fontsize=12, fontweight='bold')
                y_pos -= 0.1
                for edge in edges_added:
                    ax2.text(0.15, y_pos, f"({edge.u}, {edge.v}): {edge.weight:.2f}",
                            fontsize=10, fontfamily='monospace')
                    y_pos -= 0.05

        anim = animation.FuncAnimation(fig, update, frames=len(steps),
                                      interval=1500, repeat=True)

        if save_path:
            anim.save(save_path, writer='pillow', fps=0.67)

        if show_animation:
            plt.show()

        return anim

    def compare_algorithms(self, save_path: str = None):
        """
        Create side-by-side comparison of all three algorithms

        Args:
            save_path: Path to save figure (optional)
        """
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle("MST Algorithms Comparison", fontsize=16, fontweight='bold')

        # Run all algorithms
        k_result, k_weight, _ = self.mst.kruskal()
        p_result, p_weight, _ = self.mst.prim()
        b_result, b_weight = self.mst.boruvka()

        algorithms = [
            ('Kruskal', k_result, k_weight),
            ('Prim', p_result, p_weight),
            ('Borůvka', b_result, b_weight)
        ]

        # Top row: MST visualizations
        for i, (name, edges, weight) in enumerate(algorithms):
            ax = axes[0, i]
            ax.set_title(f"{name}'s Algorithm\nWeight: {weight:.2f}")
            ax.axis('off')

            # Draw all edges in light gray
            for u, v, w in self.edges:
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                ax.plot([x1, x2], [y1, y2], 'gray', alpha=0.3, linewidth=1)

            # Draw MST edges
            for edge in edges:
                x1, y1 = self.pos[edge.u]
                x2, y2 = self.pos[edge.v]
                ax.plot([x1, x2], [y1, y2], 'green', linewidth=3)

            # Draw vertices
            for node in self.G.nodes():
                x, y = self.pos[node]
                circle = plt.Circle((x, y), 0.08, color='skyblue')
                ax.add_patch(circle)
                ax.text(x, y, str(node), fontsize=12, ha='center', va='center', fontweight='bold')

        # Bottom row: Performance comparison
        results = self.mst.compare_algorithms(num_runs=100)

        # Mean time comparison
        ax_time = axes[1, 0]
        algos = list(results.keys())
        times = [results[algo]['mean_time'] for algo in algos]
        bars = ax_time.bar(algos, times, color=['#ff9999', '#99ccff', '#99ff99'])
        ax_time.set_ylabel('Mean Time (ms)')
        ax_time.set_title('Execution Time Comparison')
        ax_time.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax_time.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.4f}ms', ha='center', va='bottom', fontsize=10)

        # Weight comparison (should all be the same)
        ax_weight = axes[1, 1]
        weights = [results[algo]['weight'] for algo in algos]
        bars = ax_weight.bar(algos, weights, color=['#ff9999', '#99ccff', '#99ff99'])
        ax_weight.set_ylabel('MST Weight')
        ax_weight.set_title('MST Weight (Should be Equal)')
        ax_weight.grid(axis='y', alpha=0.3)

        # Time complexity info
        ax_complexity = axes[1, 2]
        ax_complexity.axis('off')
        complexity_text = [
            "Time Complexities:",
            "",
            "Kruskal's:",
            "  O(E log E) or O(E log V)",
            "  Best for sparse graphs",
            "",
            "Prim's:",
            "  O((V+E) log V) - binary heap",
            "  O(V²) - simple array",
            "  Best for dense graphs",
            "",
            "Borůvka's:",
            "  O(E log V)",
            "  Naturally parallel",
        ]

        y_pos = 0.95
        for text in complexity_text:
            if text == "":
                y_pos -= 0.04
            else:
                fontsize = 11 if ":" in text and text.endswith(":") else 10
                fontweight = 'bold' if ":" in text and text.endswith(":") else 'normal'
                ax_complexity.text(0.05, y_pos, text, fontsize=fontsize,
                                 fontweight=fontweight, fontfamily='monospace',
                                 verticalalignment='top')
                y_pos -= 0.06

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()


def demo_visualization():
    """Demonstrate MST visualization"""
    print("MST Visualization Demo")
    print("=" * 80)

    # Example graph
    edges = [
        (0, 1, 4),
        (0, 7, 8),
        (1, 2, 8),
        (1, 7, 11),
        (2, 3, 7),
        (2, 5, 4),
        (2, 8, 2),
        (3, 4, 9),
        (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1),
        (6, 8, 6),
        (7, 8, 7)
    ]

    viz = MSTVisualizer(9, edges)

    print("\n1. Creating algorithm comparison...")
    viz.compare_algorithms(save_path='mst_comparison.png')

    print("\n2. Creating Kruskal animation...")
    viz.visualize_kruskal(show_animation=False)

    print("\n3. Creating Prim animation...")
    viz.visualize_prim(show_animation=False)

    print("\n4. Creating Boruvka animation...")
    viz.visualize_boruvka(show_animation=False)

    print("\nVisualization complete!")


if __name__ == "__main__":
    demo_visualization()
