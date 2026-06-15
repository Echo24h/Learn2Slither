import os

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class TrainingStats:
    """
    Tracks and visualizes training statistics for reinforcement learning.
    """

    def __init__(self) -> None:
        self.__scores = []
        self.__exploration_rates = []
        self.__steps_per_episode = []

    def record_episode(self, score: int, exploration_rate: float,
                       steps: int) -> None:
        """Record statistics for a completed episode."""
        self.__scores.append(score)
        self.__exploration_rates.append(exploration_rate)
        self.__steps_per_episode.append(steps)

    def plot(self) -> None:
        """Plot training statistics."""
        if len(self.__scores) == 0:
            print("No statistics to plot.")
            return

        # Set up the figure and subplots
        fig = plt.figure(figsize=(10, 10))
        gs = fig.add_gridspec(3, 1, hspace=0.4)

        ax1 = fig.add_subplot(gs[0, 0])  # Ligne 1 : Score
        ax2 = fig.add_subplot(gs[1, 0])  # Ligne 2 : Steps
        ax3 = fig.add_subplot(gs[2, 0])  # Ligne 3 : Exploration

        fig.patch.set_facecolor('white')

        # Summary stats
        avg_score = np.mean(self.__scores)
        max_score = np.max(self.__scores)
        fig.suptitle(
            f'Training Statistics | Avg: {avg_score:.1f} | Max: {max_score}',
            fontsize=13, fontweight='bold', y=0.98
        )

        episodes = np.array(range(1, len(self.__scores) + 1))

        # Score per episode
        ax1.plot(episodes, self.__scores, color='#3498db', linewidth=1.2, alpha=0.7)

        if len(self.__scores) > 20:
            window = min(50, len(self.__scores) // 10)
            moving_avg = np.convolve(self.__scores, np.ones(window)/window, mode='valid')
            ax1.plot(range(window, len(self.__scores) + 1), moving_avg, color='#e74c3c', linewidth=2, label='Average')
            ax1.legend(loc='best', frameon=False, fontsize=9)

        ax1.set_ylabel('Score', fontsize=10, fontweight='bold')
        ax1.set_title('Score per Episode', fontsize=11, pad=8)
        ax1.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        # Steps per episode
        ax2.plot(episodes, self.__steps_per_episode, color='#2ecc71', linewidth=1.2)
        ax2.set_xlabel('Episode', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Steps', fontsize=10, fontweight='bold')
        ax2.set_title('Episode Duration', fontsize=11, pad=8)
        ax2.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        # Exploration rate per episode
        ax3.plot(episodes, self.__exploration_rates, color='#f39c12', linewidth=1.5)
        ax3.set_xlabel('Episode', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Exploration', fontsize=10, fontweight='bold')
        ax3.set_title('Exploration Rate', fontsize=11, pad=8)
        ax3.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)

        backend = matplotlib.get_backend().lower()
        display_available = os.environ.get('DISPLAY') is not None

        if backend == 'agg' or not display_available:
            output_path = 'training_stats.png'
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"Training plot saved to {output_path}")
        else:
            plt.show()

        plt.close(fig)

    def get_summary(self) -> dict:
        """Return a summary of training statistics."""
        if len(self.__scores) == 0:
            return {}

        return {
            'episodes': len(self.__scores),
            'avg_score': np.mean(self.__scores),
            'max_score': np.max(self.__scores),
            'min_score': np.min(self.__scores),
            'avg_steps': np.mean(self.__steps_per_episode),
            'final_exploration': self.__exploration_rates[-1]
        }
