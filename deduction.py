import json
import numpy as np
from sklearn.linear_model import LinearRegression

# =========================
# Exemplo de dados (adicione vários!)
# =========================
data = [
    {"CRate": "10", "CDmg": "13", "ATK%": "13", "SPD": "10", "Eff": 89},
    {"CRate": "7", "CDmg": "10", "ATK%": "12", "SPD": "8", "Eff": 70},
    {"CRate": "12", "CDmg": "15", "ATK%": "9", "SPD": "11", "Eff": 95},
    {"CRate": "5", "CDmg": "8", "ATK%": "10", "SPD": "6", "Eff": 55},
]

# =========================
# Preparar dados
# =========================
X = []
y = []

for rune in data:
    crate = float(rune["CRate"])
    cdmg = float(rune["CDmg"])
    atk = float(rune["ATK%"])
    spd = float(rune["SPD"])
    eff = float(rune["Eff"])

    X.append([crate, cdmg, atk, spd])
    y.append(eff)

X = np.array(X)
y = np.array(y)

# =========================
# Treinar modelo
# =========================
model = LinearRegression()
model.fit(X, y)

# =========================
# Resultados
# =========================
weights = model.coef_
intercept = model.intercept_

print("Pesos encontrados:")
print(f"CRate: {weights[0]:.4f}")
print(f"CDmg : {weights[1]:.4f}")
print(f"ATK% : {weights[2]:.4f}")
print(f"SPD  : {weights[3]:.4f}")
print(f"Intercepto: {intercept:.4f}")

# =========================
# Fórmula final
# =========================
print("\nFórmula aproximada:")
print(
    f"Eff = {weights[0]:.2f}*CRate + "
    f"{weights[1]:.2f}*CDmg + "
    f"{weights[2]:.2f}*ATK% + "
    f"{weights[3]:.2f}*SPD + "
    f"{intercept:.2f}"
)
