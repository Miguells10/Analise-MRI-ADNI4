import os
import pydicom
import numpy as np
from skimage.transform import resize

# Classe responsável por carregar e processar imagens DICOM
class DICOMLoader:
    def __init__(self, base_path):
        # Inicializa a classe com o caminho base onde as pastas dos pacientes estão localizadas
        self.base_path = base_path

    def resize_slice(self, slice, target_shape=(128, 128)):
        """Redimensiona uma fatia para o tamanho especificado."""
        # Redimensiona a fatia (imagem 2D) para o tamanho desejado (target_shape)
        # preserve_range=True garante que os valores originais dos pixels sejam mantidos
        return resize(slice, target_shape, preserve_range=True)

    def load_and_combine_dicom_slices(self, patient_path):
        """Carrega e combina as fatias DICOM de um paciente em um volume 3D."""
        # Listas para armazenar as fatias e suas posições no espaço 3D
        slices = []
        positions = []

        # Percorre todos os arquivos na pasta do paciente
        for root, _, files in os.walk(patient_path):
            for file in files:
                # Verifica se o arquivo é um arquivo DICOM (.dcm)
                if file.endswith(".dcm"):
                    img_path = os.path.join(root, file)
                    try:
                        # Lê o arquivo DICOM usando pydicom
                        ds = pydicom.dcmread(img_path)
                        # Extrai o array de pixels da imagem
                        slice_data = ds.pixel_array
                        # Redimensiona a fatia para o tamanho desejado
                        slice_resized = self.resize_slice(slice_data)
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

    def load_all_dicom_per_patient(self, patient_ids):
        """Carrega todas as imagens DICOM para cada paciente."""
        # Dicionário para armazenar os volumes 3D de cada paciente
        dicom_data = {}
        for patient_id in patient_ids:
            # Cria o caminho completo para a pasta do paciente
            patient_path = os.path.join(self.base_path, patient_id)
            # Verifica se a pasta do paciente existe
            if os.path.exists(patient_path):
                print(f"Processando paciente: {patient_id}")
                # Carrega e combina as fatias DICOM do paciente em um volume 3D
                volume = self.load_and_combine_dicom_slices(patient_path)
                # Armazena o volume no dicionário, usando o ID do paciente como chave
                dicom_data[patient_id] = volume
            else:
                # Se a pasta não existir, exibe uma mensagem de aviso
                print(f"Pasta para o paciente {patient_id} não encontrada em {self.base_path}.")
        return dicom_data