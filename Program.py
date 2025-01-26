import os
import pydicom
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from skimage.transform import resize

# Configurar o Pandas para exibir todas as linhas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Configurações iniciais
MRI_PATH = r"MRI MPRAGE\ADNI"
CLINICAL_DATA_PATH = r"Collection\MPRAGE_TEST_1_24_2025.csv"

# Verificar se os diretórios e arquivos existem
if not os.path.exists(MRI_PATH):
    print(f"Diretório não encontrado: {MRI_PATH}")
    exit()

if not os.path.exists(CLINICAL_DATA_PATH):
    print(f"Arquivo CSV não encontrado: {CLINICAL_DATA_PATH}")
    exit()

# Função para redimensionar uma fatia
def resize_slice(slice, target_shape=(128, 128)):
    return resize(slice, target_shape, preserve_range=True)

# Função para carregar e juntar fatias DICOM de um paciente
def load_and_combine_dicom_slices(patient_path):
    slices = []
    positions = []

    for root, _, files in os.walk(patient_path):
        for file in files:
            if file.endswith(".dcm"):
                img_path = os.path.join(root, file)
                try:
                    ds = pydicom.dcmread(img_path)
                    slice_data = ds.pixel_array
                    slice_resized = resize_slice(slice_data)
                    slices.append(slice_resized)
                    positions.append(float(ds.ImagePositionPatient[2]))
                except Exception as e:
                    print(f"Erro ao carregar a imagem {img_path}: {e}")

    sorted_indices = np.argsort(positions)
    slices = [slices[i] for i in sorted_indices]
    volume = np.stack(slices)
    return volume

# Função para carregar todas as imagens de cada paciente
def load_all_dicom_per_patient(directory, patient_ids):
    dicom_data = {}
    for patient_id in patient_ids:
        patient_path = os.path.join(directory, patient_id)
        if os.path.exists(patient_path):
            print(f"Processando paciente: {patient_id}")
            volume = load_and_combine_dicom_slices(patient_path)
            dicom_data[patient_id] = volume
        else:
            print(f"Pasta para o paciente {patient_id} não encontrada em {directory}.")
    return dicom_data

# Função para exibir uma fatia do volume 3D
def plot_dicom_slice(volume, slice_idx, title="DICOM Slice"):
    plt.imshow(volume[slice_idx], cmap="gray")
    plt.title(title)
    plt.axis("off")
    plt.show()

# Função para exibir uma fatia de todos os pacientes
def plot_slices_for_all_patients(mri_data):
    for patient_id, volume in mri_data.items():
        print(f"Visualizando uma fatia do volume 3D do paciente {patient_id}")
        plot_dicom_slice(volume, slice_idx=len(volume) // 2, title=f"Fatia do Paciente {patient_id}")

# Função para extrair features das imagens DICOM
def extract_mri_features(mri_data):
    mri_features = []
    for patient_id, volume in mri_data.items():
        mean_intensity = np.mean(volume)
        std_intensity = np.std(volume)
        mri_features.append([patient_id, mean_intensity, std_intensity])
    return mri_features

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