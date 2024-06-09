# Sudoku Solver


Este projeto tem como objetivo ter um algoritmo eficiente para a solução de um sudoku.

O fluxo de execução tem como base duas principais estratégias
- Estratégias de sudoku, baseado em [Sudoku techniques](https://www.conceptispuzzles.com/index.aspx?uri=puzzle/sudoku/techniques):
    - Verificação de apenas um número ser possível na posição para que possa ser preenchido
    baseado em linha, coluna e quadrante
    - Verificação caso só tenha um número possível considerando as outras linhas relacionadas,
    chamado aqui de inferência de linhas para filtrar apenas um valor
    - O mesmo de inferência para colunas com o mesmo conceito
    - Inferência de colunas E linhas ao mesmo tempo, considerando ambas no momento  
- Solução com backtracking para sudokus mais difíceis
    - Consiste em testar os números possíveis em cada posição e verificando sempre se respeita as regras do jogo, inspirado no artigo de [Evangelos Zafeiratos](https://sudoku.com/pt/regras-do-sudoku/pares-a-apontar/)


Tivemos um tempo médio de 1.5ms para sudokus fáceis, 8ms para sudokus médios e 40ms para sudokus difíceis.