import os
import pydicom
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from skimage.transform import resize

# Configurar o Pandas para exibir todas as linhas e colunas sem truncamento
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Configurações iniciais
MRI_PATH = r"MRI MPRAGE\ADNI"  # Caminho para o diretório de imagens DICOM
CLINICAL_DATA_PATH = r"Collection\MPRAGE_TEST_1_24_2025.csv"  # Caminho para o arquivo CSV de dados clínicos

# Verificar se os diretórios e arquivos existem
if not os.path.exists(MRI_PATH):
    print(f"Diretório não encontrado: {MRI_PATH}")
    exit()

if not os.path.exists(CLINICAL_DATA_PATH):
    print(f"Arquivo CSV não encontrado: {CLINICAL_DATA_PATH}")
    exit()

# Função para redimensionar uma fatia
def resize_slice(slice, target_shape=(128, 128)):
    """Redimensiona uma fatia para o tamanho especificado."""
    return resize(slice, target_shape, preserve_range=True)

# Função para carregar e juntar fatias DICOM de um paciente
def load_and_combine_dicom_slices(patient_path):
    """Carrega e combina as fatias DICOM de um paciente em um volume 3D."""
    slices = []
    positions = []

    # Percorre todos os arquivos na pasta do paciente
    for root, _, files in os.walk(patient_path):
        for file in files:
            if file.endswith(".dcm"):
                img_path = os.path.join(root, file)
                try:
                    # Lê o arquivo DICOM
                    ds = pydicom.dcmread(img_path)
                    # Extrai o array de pixels da imagem
                    slice_data = ds.pixel_array
                    # Redimensiona a fatia
                    slice_resized = resize_slice(slice_data)
                    # Adiciona a fatia redimensionada à lista de fatias
                    slices.append(slice_resized)
                    # Extrai a posição da fatia no eixo Z (ImagePositionPatient[2])
                    positions.append(float(ds.ImagePositionPatient[2]))
                except Exception as e:
                    # Em caso de erro, exibe uma mensagem de erro
                    print(f"Erro ao carregar a imagem {img_path}: {e}")

    # Ordena as fatias com base na posição no eixo Z
    sorted_indices = np.argsort(positions)
    slices = [slices[i] for i in sorted_indices]
    # Combina as fatias em um volume 3D (numpy array)
    volume = np.stack(slices)
    return volume

# Função para carregar todas as imagens de cada paciente
def load_all_dicom_per_patient(directory, patient_ids):
    """Carrega todas as imagens DICOM para cada paciente."""
    dicom_data = {}
    for patient_id in patient_ids:
        patient_path = os.path.join(directory, patient_id)
        if os.path.exists(patient_path):
            print(f"Processando paciente: {patient_id}")
            # Carrega e combina as fatias DICOM do paciente em um volume 3D
            volume = load_and_combine_dicom_slices(patient_path)
            # Armazena o volume no dicionário, usando o ID do paciente como chave
            dicom_data[patient_id] = volume
        else:
            print(f"Pasta para o paciente {patient_id} não encontrada em {directory}.")
    return dicom_data

# Função para exibir uma fatia do volume 3D
def plot_dicom_slice(volume, slice_idx, title="DICOM Slice"):
    """Exibe uma fatia específica de um volume 3D."""
    plt.imshow(volume[slice_idx], cmap="gray")  # Exibe a fatia em tons de cinza
    plt.title(title)  # Título do gráfico
    plt.axis("off")  # Remove os eixos
    plt.show()  # Exibe o gráfico

# Função para exibir uma fatia de todos os pacientes
def plot_slices_for_all_patients(mri_data):
    """Exibe uma fatia do volume 3D para cada paciente."""
    for patient_id, volume in mri_data.items():
        print(f"Visualizando uma fatia do volume 3D do paciente {patient_id}")
        # Exibe uma fatia do meio do volume 3D
        plot_dicom_slice(volume, slice_idx=len(volume) // 2, title=f"Fatia do Paciente {patient_id}")

# Função para extrair features das imagens DICOM
def extract_mri_features(mri_data):
    """Extrai features (média e desvio padrão) das imagens DICOM."""
    mri_features = []
    for patient_id, volume in mri_data.items():
        # Calcula a intensidade média e o desvio padrão do volume 3D
        mean_intensity = np.mean(volume)
        std_intensity = np.std(volume)
        # Armazena as features em uma lista
        mri_features.append([patient_id, mean_intensity, std_intensity])
    return mri_features

# Função para gerar gráficos estatísticos
def plot_statistics(combined_data):
    """Gera gráficos estatísticos para análise dos dados."""
    # Configuração do estilo dos gráficos
    sns.set(style="whitegrid")

    # 1. Porcentagem de homens e mulheres
    plt.figure(figsize=(8, 6))
    gender_counts = combined_data['Sex'].value_counts()
    plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
    plt.title('Distribuição de Gênero')
    plt.show()

    # 2. Distribuição de idades
    plt.figure(figsize=(8, 6))
    sns.histplot(combined_data['Age'], bins=10, kde=True, color='blue')
    plt.title('Distribuição de Idades')
    plt.xlabel('Idade')
    plt.ylabel('Frequência')
    plt.show()

    # 3. Gráfico de dispersão: Idade vs. Sexo
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='Age', y='Sex', data=combined_data, hue='Sex', palette='Set1')
    plt.title('Relação entre Idade e Sexo')
    plt.xlabel('Idade')
    plt.ylabel('Sexo')
    plt.legend(title='Sexo')
    plt.show()

# Carregar dados clínicos
print("Arquivo CSV encontrado:", CLINICAL_DATA_PATH)
clinical_data = pd.read_csv(CLINICAL_DATA_PATH)

# Verificar as colunas disponíveis
print("Colunas disponíveis no arquivo CSV:")
print(clinical_data.columns)

# Filtrar IDs de pacientes do CSV
if "Subject" in clinical_data.columns:
    # Extrai os IDs dos pacientes da coluna "Subject"
    patient_ids = clinical_data["Subject"].astype(str).unique()
else:
    print("A coluna 'Subject' não foi encontrada no arquivo CSV.")
    exit()

# Carregar todas as imagens por paciente
print("Carregando todas as imagens DICOM para cada paciente...")
mri_data = load_all_dicom_per_patient(MRI_PATH, patient_ids)
print(f"{len(mri_data)} pacientes processados.")

# Exibir uma fatia de todos os pacientes
if mri_data:
    plot_slices_for_all_patients(mri_data)
else:
    print("Nenhuma imagem foi encontrada.")

# Extrair features das imagens DICOM
print("Extraindo features das imagens DICOM...")
mri_features = extract_mri_features(mri_data)

# Criar DataFrame com as features
mri_features_df = pd.DataFrame(mri_features, columns=["Subject", "Mean_Intensity", "Std_Intensity"])
mri_features_df = mri_features_df.set_index("Subject")

# Combinar dados clínicos e features MRI
print("Combinando dados clínicos e features MRI...")
clinical_data = clinical_data.set_index("Subject")
combined_data = clinical_data.join(mri_features_df, how="inner")

# Exibir os dados combinados como uma tabela formatada
print("\nDados combinados (formato de tabela):")
print(tabulate(combined_data, headers='keys', tablefmt='pretty', showindex=True))

# Gerar gráficos estatísticos
print("\nGerando gráficos estatísticos...")
plot_statistics(combined_data)