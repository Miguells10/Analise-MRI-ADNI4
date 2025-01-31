import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Classe responsável por visualizar dados e gerar gráficos
class DataVisualizer:
    def __init__(self):
        # Configura o estilo dos gráficos usando seaborn
        sns.set(style="whitegrid")

    def plot_dicom_slice(self, volume, slice_idx, title="DICOM Slice"):
        """Exibe uma fatia do volume 3D."""
        # Exibe uma fatia específica do volume 3D usando matplotlib
        plt.imshow(volume[slice_idx], cmap="gray")  # cmap="gray" para imagens em tons de cinza
        plt.title(title)  # Título do gráfico
        plt.axis("off")  # Remove os eixos
        plt.show()  # Exibe o gráfico
        plt.close()  # Fecha a figura para liberar memória

    def plot_slices_for_all_patients(self, mri_data):
        """Exibe uma fatia do volume 3D para cada paciente."""
        # Itera sobre os volumes 3D de cada paciente
        for patient_id, volume in mri_data.items():
            print(f"Visualizando uma fatia do volume 3D do paciente {patient_id}")
            # Exibe uma fatia do meio do volume 3D
            self.plot_dicom_slice(volume, slice_idx=len(volume) // 2, title=f"Fatia do Paciente {patient_id}")

    def plot_patient_statistics(self, combined_data):
        """Cria gráficos para visualizar estatísticas dos pacientes."""
        # Verifica se as colunas necessárias estão presentes no DataFrame
        required_columns = ['Age', 'Sex', 'Group', 'Mean_Intensity']
        for col in required_columns:
            if col not in combined_data.columns:
                print(f"A coluna '{col}' não foi encontrada no DataFrame. Verifique o arquivo CSV.")
                return

        # Gráfico 1: Distribuição de idades dos pacientes
        plt.figure(figsize=(8, 6))
        sns.histplot(combined_data['Age'], bins=10, kde=True, color='blue')  # Histograma com curva de densidade
        plt.title('Distribuição de Idades dos Pacientes')
        plt.xlabel('Idade')
        plt.ylabel('Frequência')
        plt.show()
        plt.close()

        # Gráfico 2: Distribuição de gênero dos pacientes
        plt.figure(figsize=(8, 6))
        sns.countplot(x='Sex', data=combined_data, hue='Sex', palette='Set2', legend=False)  # Gráfico de contagem
        plt.title('Distribuição de Gênero dos Pacientes')
        plt.xlabel('Gênero')
        plt.ylabel('Contagem')
        plt.show()
        plt.close()

        # Gráfico 3: Relação entre idade e intensidade média, colorido por grupo
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='Age', y='Mean_Intensity', hue='Group', data=combined_data, palette='Set1')  # Scatter plot
        plt.title('Relação entre Idade e Intensidade Média')
        plt.xlabel('Idade')
        plt.ylabel('Intensidade Média')
        plt.legend(title='Grupo')
        plt.show()
        plt.close()

        # Gráfico 4: Distribuição de intensidade média por grupo
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='Group', y='Mean_Intensity', data=combined_data, hue='Group', palette='Set3', legend=False)  # Boxplot
        plt.title('Distribuição de Intensidade Média por Grupo')
        plt.xlabel('Grupo')
        plt.ylabel('Intensidade Média')
        plt.show()
        plt.close()

    def plot_pca(self, combined_data):
        """Executa PCA e plota os resultados."""
        # Padroniza as features (intensidade média e desvio padrão)
        scaler = StandardScaler()
        mri_scaled = scaler.fit_transform(combined_data[["Mean_Intensity", "Std_Intensity"]])

        # Aplica PCA para reduzir a dimensionalidade para 2 componentes
        pca = PCA(n_components=2)
        mri_pca = pca.fit_transform(mri_scaled)

        # Plota os resultados do PCA
        plt.figure(figsize=(8, 6))
        plt.scatter(mri_pca[:, 0], mri_pca[:, 1], c='blue', alpha=0.7)  # Scatter plot dos componentes principais
        plt.title('PCA das Features DICOM')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.grid(True)
        plt.show()
        plt.close()

        # Exibe a variância explicada por cada componente principal
        print(f"Variância explicada por cada componente: {pca.explained_variance_ratio_}")