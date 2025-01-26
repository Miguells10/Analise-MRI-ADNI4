# Configurações iniciais
import pandas as pd

import numpy as np

from ClinicalDataProcessor import ClinicalDataProcessor
from DICOMLoader import DICOMLoader
from DataVisualizer import DataVisualizer

MRI_PATH = r"MRI MPRAGE\ADNI"
CLINICAL_DATA_PATH = r"Collection\MPRAGE_TEST_1_24_2025.csv"

# Instanciando as classes
dicom_loader = DICOMLoader(MRI_PATH)
clinical_processor = ClinicalDataProcessor(CLINICAL_DATA_PATH)
visualizer = DataVisualizer()

# Carregando dados clínicos
clinical_data = clinical_processor.load_clinical_data()
patient_ids = clinical_data["Subject"].astype(str).unique()

# Carregando imagens DICOM
mri_data = dicom_loader.load_all_dicom_per_patient(patient_ids)

# Extraindo features das imagens DICOM
mri_features = []
for patient_id, volume in mri_data.items():
    mean_intensity = np.mean(volume)
    std_intensity = np.std(volume)
    mri_features.append([patient_id, mean_intensity, std_intensity])

mri_features_df = pd.DataFrame(mri_features, columns=["Subject", "Mean_Intensity", "Std_Intensity"])
mri_features_df = mri_features_df.set_index("Subject")

# Combinando dados clínicos e features MRI
combined_data = clinical_processor.combine_data(clinical_data, mri_features_df)

# Visualizando dados
visualizer.plot_slices_for_all_patients(mri_data)
visualizer.plot_patient_statistics(combined_data)
visualizer.plot_pca(combined_data)