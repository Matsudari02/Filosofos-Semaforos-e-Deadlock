Parte 1 — Jantar dos Filósofos

1. Dinâmica do Problema

O problema do Jantar dos Filósofos modela 5 filósofos sentados em uma mesa circular que alternam entre os estados pensando, com fome e comendo. Entre cada par de filósofos há um único garfo compartilhado (totalizando 5 garfos, de 0 a 4). Para comer, cada filósofo necessita adquirir simultaneamente os dois garfos adjacentes (esquerda e direita).

Na versão ingênua, todos os filósofos seguem a mesma regra simétrica: pegam primeiro o garfo à sua esquerda e, em seguida, tentam pegar o garfo à sua direita. Caso os 5 filósofos fiquem com fome ao mesmo tempo e adquiram simultaneamente seus respectivos garfos da esquerda, nenhum garfo permanecerá livre na mesa. Todos ficarão bloqueados indefinidamente aguardando o garfo da direita, configurando um impasse.

Esse travamento ocorre porque as quatro condições de Coffman se manifestam simultaneamente:
1. Exclusão Mútua: Cada garfo só pode ser utilizado por um filósofo por vez.
2. Manter-e-Esperar: Cada filósofo retém o garfo esquerdo enquanto aguarda a liberação do garfo direito.
3. Não Preempção: Um garfo não pode ser retirado à força de um filósofo; apenas ele mesmo pode liberá-lo após comer.
4. Espera Circular: Existe uma cadeia fechada de dependências, onde cada filósofo espera por um recurso segurado pelo próximo.

2. Solução Proposta e Condição de Coffman Negada

Para solucionar o impasse, foi adotada a estratégia de Hierarquia de Recursos. Atribui-se uma ordem global estrita aos garfos (índices de 0 a 4) e impõe-se a regra de que todo filósofo deve adquirir primeiro o garfo de menor índice e, somente depois, o garfo de maior índice.

Condição de Coffman negada: Espera Circular.
Justificativa lógica: Com a ordenação global, os filósofos 0, 1, 2 e 3 pegam primeiro o garfo à sua esquerda (índices 0, 1, 2 e 3, respectivamente). Contudo, o Filósofo 4 — que está entre os garfos 4 e 0 — é obrigado a tentar adquirir primeiro o garfo 0 (menor índice) antes do garfo 4. Se os quatro primeiros filósofos pegarem seus primeiros garfos (0, 1, 2, 3), o Filósofo 4 ficará bloqueado logo na primeira tentativa (pois o garfo 0 já está com o Filósofo 0), deixando o garfo 4 livre na mesa. Com isso, o Filósofo 3 consegue pegar seu segundo garfo (4), comer e liberar ambos os recursos em cascata, tornando matematicamente impossível a formação de um ciclo fechado de espera.

3. Pseudocódigo do Protocolo

CONSTANTES:
  N = 5
  garfos[0..N-1] = array de Mutex/Locks

PARA CADA filosofo p DE 0 ATE N-1:
  // Define a ordem global de aquisição baseada nos índices dos garfos adjacentes
  garfo_esq = p
  garfo_dir = (p + 1) mod N

  primeiro_garfo = min(garfo_esq, garfo_dir)
  segundo_garfo  = max(garfo_esq, garfo_dir)

  ENQUANTO:
    estado[p] <- "PENSANDO"
    pensar()

    estado[p] <- "COM FOME"
    adquirir(garfos[primeiro_garfo])   // Bloqueia até o menor índice estar livre
    adquirir(garfos[segundo_garfo])    // Bloqueia até o maior índice estar livre

    estado[p] <- "COMENDO"
    comer()

    // Liberação dos recursos na ordem inversa
    liberar(garfos[segundo_garfo])
    liberar(garfos[primeiro_garfo])
