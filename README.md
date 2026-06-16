# OlistFlow

Pipeline ETL para processamento e análise do dataset público de e-commerce brasileiro da Olist.

## Sobre o Projeto

Este projeto tem como objetivo desenvolver um pipeline ETL (Extract, Transform, Load) aplicando conceitos de engenharia de dados e boas práticas de desenvolvimento de software.

O pipeline é responsável por:

* Extrair dados de múltiplos formatos de arquivo;
* Realizar transformações e validações;
* Carregar os dados em um banco relacional;
* Garantir qualidade por meio de testes automatizados.

## Dataset

Dataset utilizado:

**Brazilian E-Commerce Public Dataset by Olist**

Contém informações sobre aproximadamente 100 mil pedidos realizados em marketplaces brasileiros entre 2016 e 2018.

Entidades disponíveis:

* Customers
* Orders
* Products
* Sellers
* Payments
* Reviews
* Geolocation

## Tecnologias

* Python 3.x
* Pandas
* Pytest
* PostgreSQL
* Logging
* Docker

## Como Executar

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar ambiente

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar o pipeline

```bash
python main.py
```

### Executar os testes

```bash
pytest -v
```

## Estrutura

```text
src/
├── extract/
├── transform/
└── load/
```

## Licença

Projeto desenvolvido para fins educacionais e de portfólio.
