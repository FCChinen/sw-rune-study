import json
import matplotlib.pyplot as plt
import numpy as np

with open('./kept_runes/Gemmed_FastDPS_Slot1.json', 'r') as f:
    data = json.load(f)
rune_type = "DPSScore"
data = sorted(data, key=lambda x: x[rune_type], reverse=True)


# Create histogram
plt.figure(figsize=(10, 6))
slow_dps_scores = [item[rune_type] for item in data if rune_type in item]
# Create histogram with custom styling
plt.hist(slow_dps_scores, bins='auto', edgecolor='black', alpha=0.7, color='skyblue')

# Add labels and title
plt.xlabel(f'{rune_type}', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title(f'Distribution of {rune_type} Values', fontsize=14, fontweight='bold')

# Add grid for better readability
plt.grid(axis='y', alpha=0.3)

# Add statistics text box
if slow_dps_scores:
    stats_text = f'Total Items: {len(slow_dps_scores)}\n'
    stats_text += f'Mean: {np.mean(slow_dps_scores):.2f}\n'
    stats_text += f'Std Dev: {np.std(slow_dps_scores):.2f}\n'
    stats_text += f'Min: {np.min(slow_dps_scores):.2f}\n'
    stats_text += f'Max: {np.max(slow_dps_scores):.2f}'
    
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.show()