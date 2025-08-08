#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 06:33:02 2024

@author: adriandominguezcastro
"""

import random
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict

def monte_carlo_dice_simulation(trials: int = 10000, sides: int = 6) -> Dict[int, int]:
    """
    Simula lanzamientos de un dado y calcula la frecuencia de cada resultado.
    
    Parameters:
    - trials (int): Número de lanzamientos del dado.
    - sides (int): Número de caras del dado (por defecto es 6).

    Returns:
    - Dict[int, int]: Diccionario con la frecuencia de cada resultado.
    """
    outcomes = {i: 0 for i in range(1, sides + 1)}

    for _ in range(trials):
        # Generación de un número aleatorio de manera uniforme
        roll = random.randint(1, sides)  # Distribución uniforme discreta
        outcomes[roll] += 1

    return outcomes


def visualize_results(outcomes: Dict[int, int], trials: int):
    """
    Visualiza los resultados de la simulación en un gráfico de barras.

    Parameters:
    - outcomes (Dict[int, int]): Diccionario con las frecuencias de cada resultado.
    - trials (int): Número total de lanzamientos.
    """
    df = pd.DataFrame(list(outcomes.items()), columns=['Outcome', 'Frequency'])
    df['Probability (%)'] = (df['Frequency'] / trials) * 100

    # Imprimir resultados
    print(df)

    # Visualización de los resultados
    plt.bar(df['Outcome'], df['Frequency'], color='skyblue', edgecolor='black')
    plt.xlabel('Outcome')
    plt.ylabel('Frequency')
    plt.title(f'Dice Roll Simulation ({trials} trials)')
    plt.xticks(range(1, len(outcomes) + 1))
    plt.show()

# Ejecutar la simulación y visualizar los resultados
trials = 10000
outcomes = monte_carlo_dice_simulation(trials=trials, sides=6)
visualize_results(outcomes, trials)
