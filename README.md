# Análise de Imagens DICOM e Dados Clínicos

Este repositório contém um script em Python para processar imagens DICOM (resonância magnética) e dados clínicos, realizar análises estatísticas e aplicar técnicas de redução de dimensionalidade, como PCA (Principal Component Analysis).

---

## 📃 Descrição
O código realiza as seguintes etapas:

1. **Carregamento de imagens DICOM:** Processa as imagens de pacientes armazenadas em subdiretórios.
2. **Redimensionamento das imagens:** Ajusta todas as imagens para um tamanho comum.
3. **Combinação de fatias:** Organiza as imagens em volumes 3D.
4. **Extração de features:** Calcula atributos como intensidade média e desvio padrão das imagens.
5. **Integração com dados clínicos:** Combina as features das imagens com informações clínicas de um arquivo CSV.
6. **Visualização de dados:** Gera gráficos para explorar distribuições de idade, gênero e outras features.
7. **Redução de dimensionalidade:** Aplica PCA para simplificar as features extraídas.

---

## ⚙️ Requisitos
Certifique-se de ter o seguinte instalado:

- **Python 3.8 ou superior**
- **Bibliotecas:** As dependências estão listadas no arquivo `requirements.txt`.

### Instalação das dependências
Use o comando abaixo para instalar as bibliotecas:

```bash
pip install -r requirements.txt
```

### Principais bibliotecas:
- `pydicom`: Para leitura de arquivos DICOM.
- `numpy` e `pandas`: Manipulação de dados.
- `matplotlib` e `seaborn`: Visualização de dados.
- `scikit-learn`: PCA e padronização de dados.
- `scikit-image`: Para redimensionar imagens.

### Exemplo de `requirements.txt`
Se você ainda não tem um arquivo `requirements.txt`, aqui está um exemplo:

```
pydicom==2.3.1
numpy==1.23.5
pandas==1.5.3
matplotlib==3.6.2
seaborn==0.12.1
scikit-learn==1.2.0
scikit-image==0.19.3
```

---

## 📂 Estrutura do Projeto
O projeto segue a seguinte estrutura de diretórios:

```
/projeto
│
├── MRI_MPRAGE/            # Pasta com as imagens DICOM
│   ├── ADNI/              # Subpastas com imagens por paciente
│   │   ├── Patient1/
│   │   ├── Patient2/
│   │   └── ...
│
├── Collection/            # Pasta com o arquivo CSV de dados clínicos
│   └── MPRAGE_TEST_1_24_2025.csv
│
├── ClinicalDataProcessor.py  # Processamento de dados clínicos
├── DICOMLoader.py            # Carregamento de imagens DICOM
├── DataVisualizer.py         # Visualização de dados
├── Program.py                # Script principal
├── requirements.txt          # Dependências
└── README.md                 # Este arquivo
```

---

## 🚀 Como Executar

1. **Preparar os arquivos:**
   - Extraia o arquivo `.zip` das imagens DICOM na pasta `MRI MPRAGE/ADNI/`.
   - Certifique-se de que cada subpasta dentro de `ADNI/` corresponde a um paciente e contém arquivos `.dcm`.
   - Coloque o arquivo CSV `MPRAGE_TEST_1_24_2025.csv` na pasta `Collection/`.

2. **Executar o script:**
   - Navegue até o diretório do projeto no terminal e execute:

   ```bash
   python Program.py
   ```

3. **Resultados esperados:**
   - O script processará as imagens DICOM e os dados clínicos, gerando gráficos estatísticos e resultados de PCA.

---

## 🔧 Saídas Esperadas
### Gráficos:
- Distribuição de idades.
- Distribuição de gênero.
- Correlação entre idade e intensidade média.
- Boxplot de intensidade média por grupo.

### PCA:
- Gráfico de dispersão das duas primeiras componentes principais.
- Variância explicada por cada componente.

---

## ⚠️ Observações
1. **Estrutura de diretórios:**
   - O script depende da organização correta das pastas e arquivos. Certifique-se de seguir a estrutura descrita.

2. **CSV e IDs dos pacientes:**
   - A coluna `Subject` no CSV deve conter IDs que correspondam aos nomes das subpastas em `MRI MPRAGE/ADNI/`.

3. **Memória:**
   - O processamento de imagens DICOM pode consumir muita memória. Para grandes volumes de dados, considere usar uma máquina com mais RAM.

---

## 📚 Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.

