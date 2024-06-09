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
 
Fácil:
![image](https://github.com/knowrafa/sudoku-solver/assets/27822288/868f4924-6021-4d0f-aab0-5b0612b61c3a)

Médio:
![image](https://github.com/knowrafa/sudoku-solver/assets/27822288/b9b51702-6c2f-49c0-aad1-f3be3e902860)

Difícil:
![image](https://github.com/knowrafa/sudoku-solver/assets/27822288/b537a304-7db2-4110-845f-f741ae24c630)


Tivemos um tempo médio de 1.5ms para sudokus fáceis, 8ms para sudokus médios e 40ms para sudokus difíceis.
