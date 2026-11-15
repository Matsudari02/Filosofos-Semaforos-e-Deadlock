Parte 2 — Threads e Semáforos

1. Dinâmica do Problema e Condição de Corrida

Um semáforo controla o acesso a recursos compartilhados por meio de contadores de permissões, atuando como mecanismo de exclusão mútua quando inicializado com 1 permissão. 

Na versão sem semaforo, múltiplas threads executam simultaneamente operações de leitura, incremento e atribuição da variável global contador. Como essas operações em nível de instrução de máquina não são atômicas, ocorrem condições de corrida: uma thread pode ler um valor intermediário, sobrescrever o incremento de outra thread e causar a perda de atualizações, fazendo com que o valor final seja inferior ao esperado.

Na versão com semáforo, o método acquire() bloqueia a thread caso o recurso esteja ocupado, garantindo que apenas uma thread por vez acesse a seção crítica onde o contador é incrementado. O bloco try...finally assegura que o semáforo seja liberado com release() mesmo se ocorrerem exceções, restabelecendo a consistência e produzindo o valor final exato.

2. Tabela de Resultados

Parâmetros utilizados nos testes: T = 8 threads e M = 200.000 incrementos por thread - Total Esperado = 1.600.000.

| Versão | Execução | Valor Esperado | Valor Obtido | Tempo de Execução (s) |
| :--- | :---: | :---: | :---: | :---: |
| **Sem Semáforo** | 1 | 1.600.000 | 200.341 | 3.7967 s |
| **Sem Semáforo** | 2 | 1.600.000 | 201.098 | 3.7735 s |
| **Sem Semáforo** | 3 | 1.600.000 | 200.740 | 3.8159 s |
| **Com Semáforo** | 1 | 1.600.000 | 1.600.000 | 0.9447 s |
| **Com Semáforo** | 2 | 1.600.000 | 1.600.000 | 1.0808 s |
| **Com Semáforo** | 3 | 1.600.000 | 1.600.000 | 0.9588 s |

Material de Referencia: 
https://docs.github.com/pt/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables


3. Discussão de Trade-offs e Visibilidade

Por que a versão sem sincronização perde incrementos?

Devido à sobreposição de execução das threads. Quando a Thread A e a Thread B leem o valor atual do contador (ex: 100), ambas calculam 101 e escrevem de volta na memória, descartando o incremento da outra.

Por que a versão com semáforo é correta?

O semáforo serializa o acesso à seção crítica, forçando exclusão mútua estrita. Apenas uma thread altera a variável de cada vez, garantindo a atomicidade lógica da operação.

Trade-off de Throughput: 

Observa-se que a versão com semáforo consome mais tempo de execução. Isso ocorre devido à sobrecarga (*overhead*) de chamadas de sistema, alternância de contexto e contenção gerada pelas aquisições e liberações repetidas do semáforo.

Visibilidade e Ordenação em Python: Em Python, o Global Interpreter Lock (GIL) mitiga alguns problemas de corrupção de ponteiros de interpretador, mas operações compostas como contador = temp + 1 ainda sofrem com interrupções de bytecode, exigindo mecanismos explícitos de sincronização (threading.Semaphore) para garantir a visibilidade das alterações entre as threads.