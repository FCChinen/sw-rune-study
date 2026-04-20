import json
import matplotlib.pyplot as plt
import numpy as np

with open('./analysis/Everything_Slot1.json', 'r') as f:
    data = json.load(f)

print(json.dumps(data[0], indent=4))

new_data = ["SlowDPSSCore", "DPSScore","TankScore", "ControlScore", "BruiserScore", "BEff"]

data = sorted(data, key=lambda x: x["SlowDPSSCore"], reverse=True)
slow_dps = data[:5]
data = sorted(data[5:30], key=lambda x: x["DPSScore"], reverse=True)
# tank = sorted(data, key=lambda x: x["TankScore"], reverse=True)
# control = sorted(data, key=lambda x: x["ControlScore"], reverse=True)
# bruiser = sorted(data, key=lambda x: x["BruiserScore"], reverse=True)
# overall = sorted(data, key=lambda x: x["BEff"], reverse=True)
with open(f'./kept_runes/SlowDPSSCore_Slot1.json', 'w') as f:
    f.write(json.dumps(slow_dps, indent=4))

with open(f'./kept_runes/DPSScore_Slot1.json', 'w') as f:
    f.write(json.dumps(data, indent=4))
# runes = {
#     "SlowDPSSCore": [],
#     "DPSScore": [],
#     "TankScore": [],
#     "ControlScore": [],
#     "BruiserScore": [],
#     "BEff": [],
# }

# for type in new_data:
#     with open(f'./kept_runes/{type}_Slot1.json', 'w') as f:
#         runes[type] = sorted(data, key=lambda x: x[type], reverse=True)
#         f.write(json.dumps(runes[type], indent=4))

type = "DPSScore"
# Create histogram
plt.figure(figsize=(10, 6))
slow_dps_scores = [item[type] for item in data if type in item]
# Create histogram with custom styling
plt.hist(slow_dps_scores, bins='auto', edgecolor='black', alpha=0.7, color='skyblue')

# Add labels and title
plt.xlabel(f'{type}', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title(f'Distribution of {type} Values', fontsize=14, fontweight='bold')

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