# aa-project01


## Clique of size k

Este trabalho procura mostrar como o algoritmo “Clique of size k” funciona, quer como uma pesquisa de brute-force, 
quer através de uma pesquisa com uma heurística. Todos os algoritmos foram escritos em Python (3.10), e serão feitas analises sobre a complexidade computacional dos mesmos.

## Codigo

O código do projeto pode ser consultado na direrório [src](./src). 
Foram criados as seguintes classes, para fazer a geração de dados:
- [Vertex](./src/vertex.py) 
- [Point](./src/vertex.py) 

A resolução do problema a partir dos 2 algoritmos distintos é feita no ficheiro [generator.py](./src/generator.py)

## Como correr

Instalar um virtual enviroment na root do repo:

```bash
python3 -m venv venv
```

Instalar as dependências:
```bash
pip install -r requirements
```

Correr o gerador e os algoritmos

```bash
python3 generator.py -h
```

## Relatório

O projeto é acompanahdo por um relatório e o memso pode ser consultado no diretório [report](./report/relatorio.pdf)
