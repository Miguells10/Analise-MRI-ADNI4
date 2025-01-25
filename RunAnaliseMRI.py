import os
import pydicom
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from skimage.transform import resize  # Para redimensionar as fatia

# Configurações iniciais
MRI_PATH = r"MRI MPRAGE\ADNI"  # Diretório base contendo subpastas com imagens DICOM
CLINICAL_DATA_PATH = r"Collection\MPRAGE_TEST_1_24_2025.csv"  # Caminho completo para o arquivo CSV

# Verificar se os diretórios e arquivos existem
if not os.path.exists(MRI_PATH):
    print(f"Diretório não encontrado: {MRI_PATH}")
    exit()

if not os.path.exists(CLINICAL_DATA_PATH):
    print(f"Arquivo CSV não encontrado: {CLINICAL_DATA_PATH}")
    exit()

# Função para redimensionar uma fatia para um tamanho comum
def resize_slice(slice, target_shape=(128, 128)):  # Reduzindo o tamanho das fatias
    """
    Redimensiona uma fatia para o tamanho especificado.
    """
    return resize(slice, target_shape, preserve_range=True)

# Função para carregar e juntar fatias DICOM de um paciente
def load_and_combine_dicom_slices(patient_path):
    """
    Carrega e combina as fatias DICOM de um paciente em um volume 3D.
    """
    slices = []
    positions = []

    for root, _, files in os.walk(patient_path):
        for file in files:
            if file.endswith(".dcm"):
                img_path = os.path.join(root, file)
                try:
                    ds = pydicom.dcmread(img_path)
                    slice_data = ds.pixel_array
                    # Redimensionar a fatia para um tamanho comum
                    slice_resized = resize_slice(slice_data)
                    slices.append(slice_resized)
                    # Armazenar a posição da fatia (eixo Z)
                    positions.append(float(ds.ImagePositionPatient[2]))
                except Exception as e:
                    print(f"Erro ao carregar a imagem {img_path}: {e}")

    # Ordenar as fatias pela posição no eixo Z
    sorted_indices = np.argsort(positions)  # Índices ordenados
    slices = [slices[i] for i in sorted_indices]  # Reorganizar as fatias

    # Criar o volume 3D
    volume = np.stack(slices)
    return volume

# Função para carregar todas as imagens de cada paciente
def load_all_dicom_per_patient(directory, patient_ids):
    dicom_data = {}
    file_names = {}

    # Laço para cada paciente listado no CSV
    for patient_id in patient_ids:
        patient_path = os.path.join(directory, patient_id)
        if os.path.exists(patient_path):
            print(f"Processando paciente: {patient_id}")
            volume = load_and_combine_dicom_slices(patient_path)
            dicom_data[patient_id] = volume
            file_names[patient_id] = patient_path
        else:
            print(f"Pasta para o paciente {patient_id} não encontrada em {directory}.")

    return dicom_data, file_names

# Função para visualizar uma fatia do volume 3D de um paciente
def plot_dicom_slice(volume, slice_idx, title="DICOM Slice"):
    """
    Exibe uma fatia do volume 3D.
    """
    plt.imshow(volume[slice_idx], cmap="gray")
    plt.title(title)
    plt.axis("off")
    plt.show()
    plt.close()  # Fechar a figura para liberar memória

# Função para visualizar uma fatia de todos os pacientes
def plot_slices_for_all_patients(mri_data):
    """
    Exibe uma fatia do volume 3D para cada paciente.
    """
    for patient_id, volume in mri_data.items():
        print(f"Visualizando uma fatia do volume 3D do paciente {patient_id}")
        plot_dicom_slice(volume, slice_idx=len(volume) // 2, title=f"Fatia do Paciente {patient_id}")

# Função para criar gráficos sobre os pacientes
def plot_patient_statistics(combined_data):
    """
    Cria gráficos para visualizar estatísticas dos pacientes.
    """
    # Configuração do estilo dos gráficos
    sns.set(style="whitegrid")

    # Verificar se as colunas necessárias estão presentes
    required_columns = ['Age', 'Sex', 'Group', 'Mean_Intensity']
    for col in required_columns:
        if col not in combined_data.columns:
            print(f"A coluna '{col}' não foi encontrada no DataFrame. Verifique o arquivo CSV.")
            return

    # 1. Distribuição de Idades
    plt.figure(figsize=(8, 6))
    sns.histplot(combined_data['Age'], bins=10, kde=True, color='blue')
    plt.title('Distribuição de Idades dos Pacientes')
    plt.xlabel('Idade')
    plt.ylabel('Frequência')
    plt.show()
    plt.close()  # Fechar a figura para liberar memória

    # 2. Distribuição de Gênero
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Sex', data=combined_data, hue='Sex', palette='Set2', legend=False)
    plt.title('Distribuição de Gênero dos Pacientes')
    plt.xlabel('Gênero')
    plt.ylabel('Contagem')
    plt.show()
    plt.close()  # Fechar a figura para liberar memória

    # 3. Relação entre Idade e Intensidade Média
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='Age', y='Mean_Intensity', hue='Group', data=combined_data, palette='Set1')
    plt.title('Relação entre Idade e Intensidade Média')
    plt.xlabel('Idade')
    plt.ylabel('Intensidade Média')
    plt.legend(title='Grupo')
    plt.show()
    plt.close()  # Fechar a figura para liberar memória

    # 4. Boxplot de Intensidade Média por Grupo
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Group', y='Mean_Intensity', data=combined_data, hue='Group', palette='Set3', legend=False)
    plt.title('Distribuição de Intensidade Média por Grupo')
    plt.xlabel('Grupo')
    plt.ylabel('Intensidade Média')
    plt.show()
    plt.close()  # Fechar a figura para liberar memória

# Carregar dados clínicos
print("Arquivo CSV encontrado:", CLINICAL_DATA_PATH)
clinical_data = pd.read_csv(CLINICAL_DATA_PATH)

# Verificar as colunas disponíveis
print("Colunas disponíveis no arquivo CSV:")
print(clinical_data.columns)

# Filtrar IDs de pacientes do CSV
if "Subject" in clinical_data.columns:
    patient_ids = clinical_data["Subject"].astype(str).unique()
else:
    print("A coluna 'Subject' não foi encontrada no arquivo CSV.")
    exit()

# Carregar todas as imagens por paciente
print("Carregando todas as imagens DICOM para cada paciente...")
mri_data, file_names = load_all_dicom_per_patient(MRI_PATH, patient_ids)
print(f"{len(mri_data)} pacientes processados.")

# Visualizar uma fatia de todos os pacientes
if mri_data:
    plot_slices_for_all_patients(mri_data)
else:
    print("Nenhuma imagem foi encontrada.")

# Extraindo features das imagens DICOM
print("Extraindo features das imagens DICOM...")
mri_features = []
for patient_id, volume in mri_data.items():
    mean_intensity = np.mean(volume)
    std_intensity = np.std(volume)
    mri_features.append([patient_id, mean_intensity, std_intensity])

mri_features_df = pd.DataFrame(mri_features, columns=["Subject", "Mean_Intensity", "Std_Intensity"])
mri_features_df = mri_features_df.set_index("Subject")

# Combinar dados clínicos e features MRI
print("Combinando dados clínicos e features MRI...")
clinical_data = clinical_data.set_index("Subject")
combined_data = clinical_data.join(mri_features_df, how="inner")
print("Dados combinados:")
print(combined_data.head())

# Criar gráficos sobre os pacientes
print("Criando gráficos sobre os pacientes...")
plot_patient_statistics(combined_data)

# Redução de dimensionalidade com PCA
if not combined_data.empty:
    print("Executando PCA nas features DICOM...")
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
    plt.close()  # Fechar a figura para liberar memória

    print(f"Variância explicada por cada componente: {pca.explained_variance_ratio_}")
else:
    print("Nenhum dado combinado para executar PCA. Verifique os IDs dos pacientes.")

# Conclusão
print("Análises concluídas!")