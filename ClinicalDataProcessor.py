import os
import pandas as pd

class ClinicalDataProcessor:
    def __init__(self, clinical_data_path):
        self.clinical_data_path = clinical_data_path

    def load_clinical_data(self):
        """Carrega os dados clínicos de um arquivo CSV."""
        if not os.path.exists(self.clinical_data_path):
            raise FileNotFoundError(f"Erro: O arquivo {self.clinical_data_path} não foi encontrado.")
        return pd.read_csv(self.clinical_data_path)

    def combine_data(self, clinical_data, mri_features): #
        """Combina dados clínicos com features extraídas das imagens DICOM."""
        clinical_data = clinical_data.set_index("Subject")
        combined_data = clinical_data.join(mri_features, how="inner")
        return combined_data

# Configurações iniciais
CLINICAL_DATA_PATH = r"Collection\MPRAGE_TEST_1_24_2025.csv"  # Nome correto do arquivo

# Verificar se o arquivo existe antes de prosseguir
if not os.path.exists(CLINICAL_DATA_PATH):
    print(f"Erro: O arquivo {CLINICAL_DATA_PATH} não foi encontrado.")
    print("Verifique se o arquivo está na pasta 'Collection' e se o nome está correto.")
    exit()

# Instanciando a classe e carregando dados clínicos
clinical_processor = ClinicalDataProcessor(CLINICAL_DATA_PATH)
try:
    clinical_data = clinical_processor.load_clinical_data()
    print("Dados clínicos carregados com sucesso!")
    print(clinical_data.head())  # Exibe as primeiras linhas do DataFrame para verificação
except FileNotFoundError as e:
    print(e)
    exit()
except pd.errors.EmptyDataError:
    print("Erro: O arquivo CSV está vazio.")
    exit()
except pd.errors.ParserError:
    print("Erro: O arquivo CSV está mal formatado.")
    exit()