import os
import pandas as pd

# Classe responsável por processar dados clínicos
class ClinicalDataProcessor:
    def __init__(self, clinical_data_path):
        # Inicializa a classe com o caminho do arquivo CSV contendo os dados clínicos
        self.clinical_data_path = clinical_data_path

    def load_clinical_data(self):
        """Carrega os dados clínicos de um arquivo CSV."""
        # Verifica se o arquivo existe no caminho especificado
        if not os.path.exists(self.clinical_data_path):
            # Se o arquivo não existir, levanta uma exceção
            raise FileNotFoundError(f"Erro: O arquivo {self.clinical_data_path} não foi encontrado.")
        # Carrega o arquivo CSV em um DataFrame do pandas
        return pd.read_csv(self.clinical_data_path)

    def combine_data(self, clinical_data, mri_features):
        """Combina dados clínicos com features extraídas das imagens DICOM."""
        # Define a coluna "Subject" como índice do DataFrame de dados clínicos
        clinical_data = clinical_data.set_index("Subject")
        # Combina os dados clínicos com as features extraídas das imagens DICOM
        # Usa um inner join para manter apenas os registros com correspondência em ambos os DataFrames
        combined_data = clinical_data.join(mri_features, how="inner")
        return combined_data

# Configurações iniciais
# Define o caminho do arquivo CSV contendo os dados clínicos
CLINICAL_DATA_PATH = r"Collection\MPRAGE_TEST_1_24_2025.csv"  # Nome correto do arquivo

# Verificar se o arquivo existe antes de prosseguir
if not os.path.exists(CLINICAL_DATA_PATH):
    # Se o arquivo não existir, exibe uma mensagem de erro e encerra o programa
    print(f"Erro: O arquivo {CLINICAL_DATA_PATH} não foi encontrado.")
    print("Verifique se o arquivo está na pasta 'Collection' e se o nome está correto.")
    exit()

# Instanciando a classe e carregando dados clínicos
clinical_processor = ClinicalDataProcessor(CLINICAL_DATA_PATH)
try:
    # Tenta carregar os dados clínicos
    clinical_data = clinical_processor.load_clinical_data()
    print("Dados clínicos carregados com sucesso!")
    # Exibe as primeiras linhas do DataFrame para verificação
    print(clinical_data.head())
except FileNotFoundError as e:
    # Captura exceção se o arquivo não for encontrado
    print(e)
    exit()
except pd.errors.EmptyDataError:
    # Captura exceção se o arquivo CSV estiver vazio
    print("Erro: O arquivo CSV está vazio.")
    exit()
except pd.errors.ParserError:
    # Captura exceção se o arquivo CSV estiver mal formatado
    print("Erro: O arquivo CSV está mal formatado.")
    exit()