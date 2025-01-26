import os
import pydicom
import numpy as np
from skimage.transform import resize

class DICOMLoader:
    def __init__(self, base_path):
        self.base_path = base_path

    def resize_slice(self, slice, target_shape=(128, 128)):
        """Redimensiona uma fatia para o tamanho especificado."""
        return resize(slice, target_shape, preserve_range=True)

    def load_and_combine_dicom_slices(self, patient_path):
        """Carrega e combina as fatias DICOM de um paciente em um volume 3D."""
        slices = []
        positions = []

        for root, _, files in os.walk(patient_path):
            for file in files:
                if file.endswith(".dcm"):
                    img_path = os.path.join(root, file)
                    try:
                        ds = pydicom.dcmread(img_path)
                        slice_data = ds.pixel_array
                        slice_resized = self.resize_slice(slice_data)
                        slices.append(slice_resized)
                        positions.append(float(ds.ImagePositionPatient[2]))
                    except Exception as e:
                        print(f"Erro ao carregar a imagem {img_path}: {e}")

        sorted_indices = np.argsort(positions)
        slices = [slices[i] for i in sorted_indices]
        volume = np.stack(slices)
        return volume

    def load_all_dicom_per_patient(self, patient_ids):
        """Carrega todas as imagens DICOM para cada paciente."""
        dicom_data = {}
        for patient_id in patient_ids:
            patient_path = os.path.join(self.base_path, patient_id)
            if os.path.exists(patient_path):
                print(f"Processando paciente: {patient_id}")
                volume = self.load_and_combine_dicom_slices(patient_path)
                dicom_data[patient_id] = volume
            else:
                print(f"Pasta para o paciente {patient_id} não encontrada em {self.base_path}.")
        return dicom_data