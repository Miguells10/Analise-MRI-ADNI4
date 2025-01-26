import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class DataVisualizer:
    def __init__(self):
        sns.set(style="whitegrid")

    def plot_dicom_slice(self, volume, slice_idx, title="DICOM Slice"):
        """Exibe uma fatia do volume 3D."""
        plt.imshow(volume[slice_idx], cmap="gray")
        plt.title(title)
        plt.axis("off")
        plt.show()
        plt.close()

    def plot_slices_for_all_patients(self, mri_data):
        """Exibe uma fatia do volume 3D para cada paciente."""
        for patient_id, volume in mri_data.items():
            print(f"Visualizando uma fatia do volume 3D do paciente {patient_id}")
            self.plot_dicom_slice(volume, slice_idx=len(volume) // 2, title=f"Fatia do Paciente {patient_id}")

    def plot_patient_statistics(self, combined_data):
        """Cria gráficos para visualizar estatísticas dos pacientes."""
        required_columns = ['Age', 'Sex', 'Group', 'Mean_Intensity']
        for col in required_columns:
            if col not in combined_data.columns:
                print(f"A coluna '{col}' não foi encontrada no DataFrame. Verifique o arquivo CSV.")
                return

        plt.figure(figsize=(8, 6))
        sns.histplot(combined_data['Age'], bins=10, kde=True, color='blue')
        plt.title('Distribuição de Idades dos Pacientes')
        plt.xlabel('Idade')
        plt.ylabel('Frequência')
        plt.show()
        plt.close()

        plt.figure(figsize=(8, 6))
        sns.countplot(x='Sex', data=combined_data, hue='Sex', palette='Set2', legend=False)
        plt.title('Distribuição de Gênero dos Pacientes')
        plt.xlabel('Gênero')
        plt.ylabel('Contagem')
        plt.show()
        plt.close()

        plt.figure(figsize=(8, 6))
        sns.scatterplot(x='Age', y='Mean_Intensity', hue='Group', data=combined_data, palette='Set1')
        plt.title('Relação entre Idade e Intensidade Média')
        plt.xlabel('Idade')
        plt.ylabel('Intensidade Média')
        plt.legend(title='Grupo')
        plt.show()
        plt.close()

        plt.figure(figsize=(8, 6))
        sns.boxplot(x='Group', y='Mean_Intensity', data=combined_data, hue='Group', palette='Set3', legend=False)
        plt.title('Distribuição de Intensidade Média por Grupo')
        plt.xlabel('Grupo')
        plt.ylabel('Intensidade Média')
        plt.show()
        plt.close()

    def plot_pca(self, combined_data):
        """Executa PCA e plota os resultados."""
        scaler = StandardScaler()
        mri_scaled = scaler.fit_transform(combined_data[["Mean_Intensity", "Std_Intensity"]])

        pca = PCA(n_components=2)
        mri_pca = pca.fit_transform(mri_scaled)

        plt.figure(figsize=(8, 6))
        plt.scatter(mri_pca[:, 0], mri_pca[:, 1], c='blue', alpha=0.7)
        plt.title('PCA das Features DICOM')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.grid(True)
        plt.show()
        plt.close()

        print(f"Variância explicada por cada componente: {pca.explained_variance_ratio_}")