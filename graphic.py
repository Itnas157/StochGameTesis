import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import os

# Función para cargar los datos
def get_data(filename):
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

class Graphic:
    def __init__(self, json_folder):
        self.json_folder = json_folder
    def graph(self, is_ss_ss):
        if is_ss_ss: self.graph_ss_ss()
        else: self.graph_q_ss()

    def graph_ss_ss(self):
        data = get_data(self.json_folder + "/results.json")
        df = pd.DataFrame(data)

        # Crear directorio si no existe
        output_dir = self.json_folder
        os.makedirs(output_dir, exist_ok=True)

        # 1. **Matriz de correlación**
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matriz de Correlación entre Parámetros y Resultados")
        plt.savefig(f"{output_dir}/relacion.png")
        plt.close()

        # 2. **Distribuciones de resultados**
        plt.figure(figsize=(10, 6))
        sns.histplot(df["SS_Max"], bins=30, kde=True, label="SS_Max", color="blue", alpha=0.6)
        sns.histplot(df["SS_Min"], bins=30, kde=True, label="SS_Min", color="red", alpha=0.6)
        sns.histplot(df["Draw"], bins=30, kde=True, label="Draw", color="green", alpha=0.6)
        plt.xlabel("Porcentaje de Resultados")
        plt.ylabel("Frecuencia")
        plt.title("Distribución de Resultados")
        plt.legend()
        plt.savefig(f"{output_dir}/distribucion_resultados.png")
        plt.close()

        # 3. **Evolución de parámetros vs Resultados**
        fig, axes = plt.subplots(1, 2, figsize=(14, 10))
        params = ["smart_sampling_n", "smart_sampling_constant"]

        for i, param in enumerate(params):
            sns.scatterplot(x=df[param], y=df["SS_Max"], ax=axes[i], label="SS_Max", color="blue", alpha=0.5)
            sns.scatterplot(x=df[param], y=df["SS_Min"], ax=axes[i], label="SS_Min", color="red", alpha=0.5)
            sns.scatterplot(x=df[param], y=df["Draw"], ax=axes[i], label="Draw", color="green", alpha=0.5)
            axes[i].set_title(f"{param} vs Resultados")

        plt.tight_layout()
        plt.savefig(f"{output_dir}/parametros_vs_resultados.png")
        plt.close()

        # 4. **Q-learning vs SmartSampling (Trade-off)**
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=df["SS_Max"], y=df["SS_Min"], alpha=0.6)
        plt.xlabel("SS_Max (%)")
        plt.ylabel("SS_Min (%)")
        plt.title("Relación entre SS_Max y SS_Min")
        plt.savefig(f"{output_dir}/ss_vs_ss.png")
        plt.close()

        # 5. **Encontrar los mejores valores promedio de cada parámetro**
        best_params_q = {}
        best_params_smart = {}

        for param in params:
            avg_q = df.groupby(param)["SS_Max"].mean()
            avg_smart = df.groupby(param)["SS_Min"].mean()
            
            best_params_q[param] = avg_q.idxmax()  # Valor del parámetro que maximiza Q-learning en promedio
            best_params_smart[param] = avg_smart.idxmax()  # Valor del parámetro que maximiza SmartSampling en promedio

        # 6. **Cálculo del promedio de victorias**
        avg_q_learning = df["SS_Max"].mean()
        avg_smart_sampling = df["SS_Min"].mean()
        avg_draw = df["Draw"].mean()

        # Guardar los mejores valores promedio en un archivo .txt
        txt_filename = f"{output_dir}/mejores_parametros.txt"
        with open(txt_filename, "w") as f:
            f.write(f"Mejores valores promedio para maximizar SS_Max:\n")
            for param, value in best_params_q.items():
                f.write(f"{param}: {value}\n")
            
            f.write("\nMejores valores promedio para maximizar SS_Min:\n")
            for param, value in best_params_smart.items():
                f.write(f"{param}: {value}\n")
            
            f.write("\nPromedio de victorias:\n")
            f.write(f"SS_Max: {avg_q_learning:.2f}%\n")
            f.write(f"SS_Min: {avg_smart_sampling:.2f}%\n")
            f.write(f"Draw: {avg_draw:.2f}%\n")


    def graph_q_ss(self):
        data = get_data(self.json_folder + "/results.json")
        df = pd.DataFrame(data)

        # Crear directorio si no existe
        output_dir = self.json_folder
        os.makedirs(output_dir, exist_ok=True)

        # 1. **Matriz de correlación**
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matriz de Correlación entre Parámetros y Resultados")
        plt.savefig(f"{output_dir}/relacion.png")
        plt.close()

        # 2. **Distribuciones de resultados**
        plt.figure(figsize=(10, 6))
        sns.histplot(df["Q-learning"], bins=30, kde=True, label="Q-learning", color="blue", alpha=0.6)
        sns.histplot(df["SmartSampling"], bins=30, kde=True, label="SmartSampling", color="red", alpha=0.6)
        sns.histplot(df["Draw"], bins=30, kde=True, label="Draw", color="green", alpha=0.6)
        plt.xlabel("Porcentaje de Resultados")
        plt.ylabel("Frecuencia")
        plt.title("Distribución de Resultados")
        plt.legend()
        plt.savefig(f"{output_dir}/distribucion_resultados.png")
        plt.close()

        # 3. **Evolución de parámetros vs Resultados**
        fig, axes = plt.subplots(3, 3, figsize=(14, 10))
        params = ["alpha", "gamma", "epsilon", "epsilon_decay", "q_learning_episodes", "smart_sampling_n", "q_learning_reset", "smart_sampling_constant", "final_alpha_porc"]

        for i, param in enumerate(params):
            row, col = divmod(i, 3)
            sns.scatterplot(x=df[param], y=df["Q-learning"], ax=axes[row, col], label="Q-learning", color="blue", alpha=0.5)
            sns.scatterplot(x=df[param], y=df["SmartSampling"], ax=axes[row, col], label="SmartSampling", color="red", alpha=0.5)
            sns.scatterplot(x=df[param], y=df["Draw"], ax=axes[row, col], label="Draw", color="green", alpha=0.5)
            axes[row, col].set_title(f"{param} vs Resultados")

        plt.tight_layout()
        plt.savefig(f"{output_dir}/parametros_vs_resultados.png")
        plt.close()

        # 4. **Q-learning vs SmartSampling (Trade-off)**
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=df["Q-learning"], y=df["SmartSampling"], alpha=0.6)
        plt.xlabel("Q-learning (%)")
        plt.ylabel("SmartSampling (%)")
        plt.title("Relación entre Q-learning y SmartSampling")
        plt.savefig(f"{output_dir}/q_vs_smart.png")
        plt.close()

        # 5. **Encontrar los mejores valores promedio de cada parámetro**
        best_params_q = {}
        best_params_smart = {}

        for param in params:
            avg_q = df.groupby(param)["Q-learning"].mean()
            avg_smart = df.groupby(param)["SmartSampling"].mean()
            
            best_params_q[param] = avg_q.idxmax()  # Valor del parámetro que maximiza Q-learning en promedio
            best_params_smart[param] = avg_smart.idxmax()  # Valor del parámetro que maximiza SmartSampling en promedio

        # 6. **Cálculo del promedio de victorias**
        avg_q_learning = df["Q-learning"].mean()
        avg_smart_sampling = df["SmartSampling"].mean()
        avg_draw = df["Draw"].mean()

        # Guardar los mejores valores promedio en un archivo .txt
        txt_filename = f"{output_dir}/mejores_parametros.txt"
        with open(txt_filename, "w") as f:
            f.write(f"Mejores valores promedio para maximizar Q-learning:\n")
            for param, value in best_params_q.items():
                f.write(f"{param}: {value}\n")
            
            f.write("\nMejores valores promedio para maximizar SmartSampling:\n")
            for param, value in best_params_smart.items():
                f.write(f"{param}: {value}\n")
            
            f.write("\nPromedio de victorias:\n")
            f.write(f"Q-learning: {avg_q_learning:.2f}%\n")
            f.write(f"SmartSampling: {avg_smart_sampling:.2f}%\n")
            f.write(f"Draw: {avg_draw:.2f}%\n")