from package_203_project import package_203_project
from package_203_project import *
from package_203_project.portfolio_information import return_portfolio
import numpy as np

# Définir un portefeuille
portfolio = {"Asset1": 0.5, "Asset2": 0.3, "Asset3": 0.2}

# Définir un ensemble d'informations
information_set = {
    "expected_returns": np.array([0.08, 0.12, 0.10])  # Rendements attendus pour chaque actif
}

# Calculer le rendement
portfolio_return = return_portfolio(portfolio, information_set)
print(f"Le rendement attendu du portefeuille est : {portfolio_return:.2%}")


