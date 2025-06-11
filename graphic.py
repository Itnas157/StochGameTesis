import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import os
import numpy as np

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
        else: self.graph_q_ss(); self.graph_comparisons()
        
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
        plt.tight_layout()  # <-- Línea clave para evitar que se corten las letras
        plt.savefig(f"{output_dir}/relacion.png")
        plt.close()


        # 2. **Distribuciones de resultados**
        plt.figure(figsize=(10, 6))
        sns.histplot(df["SS_Max"], bins=30, kde=True, label="SS_Max", color="blue", alpha=0.6)
        sns.histplot(df["SS_Min"], bins=30, kde=True, label="SS_Min", color="red", alpha=0.6)
        #sns.histplot(df["Draw"], bins=30, kde=True, label="Draw", color="green", alpha=0.6)
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
            #sns.scatterplot(x=df[param], y=df["Draw"], ax=axes[i], label="Draw", color="green", alpha=0.5)
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
        data = get_data(os.path.join(self.json_folder, "results.json"))
        df = pd.DataFrame(data)

        # Crear directorio si no existe
        output_dir = self.json_folder
        os.makedirs(output_dir, exist_ok=True)

        # ----------------------------------------------------------
        # 0. Convertir "Q-learning_convergence" a arrays NumPy si es necesario
        # ----------------------------------------------------------
        if "Q-learning_convergence" in df.columns:
            df["Q-learning_convergence"] = df["Q-learning_convergence"].apply(
                lambda x: np.array(x) if isinstance(x, (list, np.ndarray)) else np.array([])
            )

        # ----------------------------------------------------------
        # 1. Matriz de correlación
        # ----------------------------------------------------------
        plt.figure(figsize=(10, 6))
        cols_corr = df.select_dtypes(include=[np.number]).columns.tolist()
        # Removemos la columna "Q-learning_convergence" porque es de tipo objeto/array
        cols_corr = [c for c in cols_corr if c != "Q-learning_convergence"]
        sns.heatmap(df[cols_corr].corr(), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matriz de Correlación entre Parámetros y Resultados")
        plt.savefig(os.path.join(output_dir, "relacion.png"))
        plt.close()

        # ----------------------------------------------------------
        # 2. Distribuciones de resultados
        # ----------------------------------------------------------
        plt.figure(figsize=(10, 6))
        if "Q-learning" in df.columns:
            sns.histplot(df["Q-learning"], bins=30, kde=True, label="Q-learning", color="blue", alpha=0.6)
        if "SmartSampling" in df.columns:
            sns.histplot(df["SmartSampling"], bins=30, kde=True, label="SmartSampling", color="red", alpha=0.6)

        plt.xlabel("Porcentaje de Resultados")
        plt.ylabel("Frecuencia")
        plt.title("Distribución de Resultados")
        plt.legend()
        plt.savefig(os.path.join(output_dir, "distribucion_resultados.png"))
        plt.close()

        # ----------------------------------------------------------
        # 3. Evolución de parámetros vs Resultados (dinámico)
        # ----------------------------------------------------------
        resultados = []
        if "Q-learning" in df.columns:
            resultados.append("Q-learning")
        if "SmartSampling" in df.columns:
            resultados.append("SmartSampling")

        exclusions = set(resultados + ["Mejor_z", "Q-learning_convergence"])
        params = [col for col in df.select_dtypes(include=[np.number]).columns if col not in exclusions]

        n_params = len(params)
        ncols = 3
        nrows = (n_params + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
        axes = axes.flatten()

        for i, param in enumerate(params):
            ax = axes[i]
            for resultado in resultados:
                sns.scatterplot(x=df[param], y=df[resultado], ax=ax, label=resultado, alpha=0.5)
            ax.set_title(f"{param} vs Resultados")
            ax.legend()

        for j in range(n_params, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "parametros_vs_resultados.png"))
        plt.close()

        # ----------------------------------------------------------
        # 4. Q-learning vs SmartSampling (Trade-off)
        # ----------------------------------------------------------
        if "Q-learning" in df.columns and "SmartSampling" in df.columns:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=df["Q-learning"], y=df["SmartSampling"], alpha=0.6)
            plt.xlabel("Q-learning (%)")
            plt.ylabel("SmartSampling (%)")
            plt.title("Relación entre Q-learning y SmartSampling")
            plt.savefig(os.path.join(output_dir, "q_vs_smart.png"))
            plt.close()

        # ----------------------------------------------------------
        # 5. Encontrar los mejores valores promedio de cada parámetro
        # ----------------------------------------------------------
        best_params_q = {}
        best_params_smart = {}
        if "Q-learning" in df.columns and "SmartSampling" in df.columns:
            for param in params:
                avg_q = df.groupby(param)["Q-learning"].mean()
                avg_smart = df.groupby(param)["SmartSampling"].mean()

                best_params_q[param] = avg_q.idxmax()
                best_params_smart[param] = avg_smart.idxmax()

        # ----------------------------------------------------------
        # 6. Cálculo del promedio de victorias
        # ----------------------------------------------------------
        avg_q_learning = df["Q-learning"].mean() if "Q-learning" in df.columns else np.nan
        avg_smart_sampling = df["SmartSampling"].mean() if "SmartSampling" in df.columns else np.nan

        txt_filename = os.path.join(output_dir, "mejores_parametros.txt")
        with open(txt_filename, "w") as f:
            if best_params_q:
                f.write("Mejores valores promedio para maximizar Q-learning:\n")
                for param, value in best_params_q.items():
                    f.write(f"{param}: {value}\n")
                f.write("\n")
            if best_params_smart:
                f.write("Mejores valores promedio para maximizar SmartSampling:\n")
                for param, value in best_params_smart.items():
                    f.write(f"{param}: {value}\n")
                f.write("\n")
            f.write("Promedio de victorias:\n")
            f.write(f"Q-learning: {avg_q_learning:.2f}%\n")
            f.write(f"SmartSampling: {avg_smart_sampling:.2f}%\n")

    def graph_comparisons(self):
        data = get_data(os.path.join(self.json_folder, "results.json"))
        df = pd.DataFrame(data)
        output_dir = self.json_folder
        os.makedirs(output_dir, exist_ok=True)

        combinations = [(True, True), (True, False), (False, True), (False, False)]
        results_summary = []

        for q_reset, ss_constant in combinations:
            if "q_learning_reset" not in df.columns or "smart_sampling_constant" not in df.columns:
                continue

            subset = df[(df["q_learning_reset"] == q_reset) & (df["smart_sampling_constant"] == ss_constant)]
            label = f"QL_Reset={q_reset}, SS_Const={ss_constant}"

            if not subset.empty:
                plt.figure(figsize=(10, 6))
                if "Q-learning" in subset.columns:
                    sns.histplot(subset["Q-learning"], bins=30, kde=True, label="Q-learning", color="blue", alpha=0.6)
                if "SmartSampling" in subset.columns:
                    sns.histplot(subset["SmartSampling"], bins=30, kde=True, label="SmartSampling", color="red", alpha=0.6)
                plt.xlabel("Porcentaje de Resultados")
                plt.ylabel("Frecuencia")
                plt.title(f"Distribución de Resultados ({label})")
                plt.legend()
                plt.savefig(os.path.join(output_dir, f"distribucion_resultados_{q_reset}_{ss_constant}.png"))
                plt.close()

                avg_q = subset["Q-learning"].mean() if "Q-learning" in subset.columns else np.nan
                avg_smart = subset["SmartSampling"].mean() if "SmartSampling" in subset.columns else np.nan
                max_q = subset["Q-learning"].max() if "Q-learning" in subset.columns else np.nan
                max_smart = subset["SmartSampling"].max() if "SmartSampling" in subset.columns else np.nan
                min_q = subset["Q-learning"].min() if "Q-learning" in subset.columns else np.nan
                min_smart = subset["SmartSampling"].min() if "SmartSampling" in subset.columns else np.nan
                var_q = subset["Q-learning"].std() if "Q-learning" in subset.columns else np.nan
                var_smart = subset["SmartSampling"].std() if "SmartSampling" in subset.columns else np.nan
                draw_avg = subset["Draw"].mean() if "Draw" in subset.columns else np.nan

                results_summary.append({
                    "Combination": label,
                    "Avg_Q-learning": avg_q,
                    "Avg_SmartSampling": avg_smart,
                    "Max_Q-learning": max_q,
                    "Max_SmartSampling": max_smart,
                    "Min_Q-learning": min_q,
                    "Min_SmartSampling": min_smart,
                    "Var_Q-learning": var_q,
                    "Var_SmartSampling": var_smart,
                    "Avg_Draw": draw_avg
                })

        txt_filename = os.path.join(output_dir, "comparisons_summary.txt")
        with open(txt_filename, "w") as f:
            for result in results_summary:
                f.write(f"Combination: {result['Combination']}\n")
                f.write(f"  Avg Q-learning: {result['Avg_Q-learning']:.2f}%\n")
                f.write(f"  Avg SmartSampling: {result['Avg_SmartSampling']:.2f}%\n")
                f.write(f"  Max Q-learning: {result['Max_Q-learning']:.2f}%\n")
                f.write(f"  Max SmartSampling: {result['Max_SmartSampling']:.2f}%\n")
                f.write(f"  Min Q-learning: {result['Min_Q-learning']:.2f}%\n")
                f.write(f"  Min SmartSampling: {result['Min_SmartSampling']:.2f}%\n")
                f.write(f"  Desviación Q-learning: {result['Var_Q-learning']:.2f}\n")
                f.write(f"  Desviación SmartSampling: {result['Var_SmartSampling']:.2f}\n")
                f.write(f"  Avg Draw: {result['Avg_Draw']:.2f}%\n")
                f.write("\n")