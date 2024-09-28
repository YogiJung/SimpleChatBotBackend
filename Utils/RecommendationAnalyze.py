import pandas as pd
import numpy as np
import os

df1 = None
df3 = None

def dataSetUp():
    global df1, df3

    if df1 is None or df3 is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, ".."))

        recommendationSystem = os.path.join(root_dir, "downloaded_folder/RecommendationSystem.xlsx")
        techniciansList = os.path.join(root_dir, "downloaded_folder/TechniciansList.xlsx")
        try:
            df1 = pd.read_excel(recommendationSystem, header=0)
            df3 = pd.read_excel(techniciansList, header=1)

            print("Excel files loaded into memory.")
        except Exception as e:
            print(f"Error loading Excel files: {e}")
            return

    technicians = [str(tech) for tech in df1.iloc[:, 0].values]
    integrated_factors = df1.columns[1:].tolist()

    return technicians, integrated_factors

def recommendation_algorithm(recommendation_weights: [int]):
    global df1, df3
    if df1 is None or df3 is None:
        dataSetUp()
    df1_numeric = df1.iloc[:, 1:]
    integrated_score_array = df1_numeric.to_numpy()
    weights_array = np.array(recommendation_weights)

    matrix_product = np.dot(integrated_score_array, weights_array.T)
    summed_rows = np.sum(matrix_product, axis=1)

    top_3_indices = np.argsort(summed_rows)[-3:]
    top_3_technicians = df3.iloc[top_3_indices - 1]
    top_3_values = summed_rows[top_3_indices]
    return top_3_technicians, top_3_values
