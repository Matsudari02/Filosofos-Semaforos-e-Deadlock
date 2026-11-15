Parte 3 — Deadlock

1. Dinâmica do Problema

Deadlock acontece quando um grupo de threads para de andar porque cada uma espera por algo que só outra do grupo pode liberar, normalmente um lock. Aqui temos duas threads (Thread 1 e Thread 2) e dois locks (`LOCK_A` e `LOCK_B`) usados em ordem oposta: a Thread 1 pega `LOCK_A` e depois `LOCK_B`; a Thread 2 pega `LOCK_B` e depois `LOCK_A`.

Uma pausa de 50 ms entre as duas aquisições garante que cada thread pegue o seu primeiro lock antes de a outra pedir o segundo, o que torna o travamento reproduzível. Depois disso, cada uma segura um lock e espera o da outra, e as mensagens `T1 concluiu` e `T2 concluiu` nunca aparecem.

O impasse exige as quatro condições de Coffman ao mesmo tempo, e todas estão presentes:
1. Exclusão Mútua: um `threading.Lock` só pertence a uma thread por vez.
2. Manter-e-Esperar: cada thread segura um lock enquanto espera o outro.
3. Não Preempção: ninguém tira um lock à força; só o dono libera, com `release()`, e isso nunca acontece.
4. Espera Circular: a Thread 1 espera pela Thread 2, que espera pela Thread 1.

2. Evidência do Travamento

Os `acquire()` são bloqueantes e sem timeout, então o travamento é real. Para não prender o terminal, as threads são `daemon` e a thread principal funciona como vigia: espera até 3 s com `join(timeout)` e se alguma continuar viva, imprime um diagnóstico e sai com código 1. O diagnóstico faz o papel do `jstack`: `threading.enumerate()` lista as threads e `sys._current_frames()` mostra a linha em que cada uma parou.

Execução: `python3 deadlock_sem_trava.py`

```
[ 0.000s] [Thread 1] quero o LOCK_A...
[ 0.000s] [Thread 2] quero o LOCK_B...
[ 0.000s] [Thread 1] peguei o LOCK_A
[ 0.000s] [Thread 1] dormindo 50ms (dá tempo da Thread 2 pegar o LOCK_B)
[ 0.000s] [Thread 2] peguei o LOCK_B
[ 0.000s] [Thread 2] dormindo 50ms (dá tempo da Thread 1 pegar o LOCK_A)
[ 0.051s] [Thread 1] agora quero o LOCK_B, sem largar o LOCK_A...
[ 0.051s] [Thread 2] agora quero o LOCK_A, sem largar o LOCK_B...

==============================================================
DEADLOCK: nenhum progresso após 3s
==============================================================
Threads vivas (threading.enumerate):
  - Principal: executando este diagnóstico
  - Thread 1: BLOQUEADA em thread_1(), linha 31 -> LOCK_B.acquire()
  - Thread 2: BLOQUEADA em thread_2(), linha 48 -> LOCK_A.acquire()

LOCK_A retido: True | LOCK_B retido: True

Ciclo de espera:
  Thread 1 segura LOCK_A e espera LOCK_B
  Thread 2 segura LOCK_B e espera LOCK_A
```

Cada thread pega o primeiro lock em 0,01 depois da pausa, as duas tentam o segundo em 0,052 s. Dai em diante não há mais progresso, e o diagnóstico confirma ambas paradas em `acquire()` com os dois locks retidos.

3. Solução Proposta e Condição de Coffman Negada

A correção usa Hierarquia de Recursos, uma estratégia de prevenção, ignorar, detectar e recuperar, prevenir e evitar. Os locks ganham uma ordem global (`LOCK_A` < `LOCK_B`) e toda thread pega `LOCK_A` antes de `LOCK_B`.

Condição de Coffman negada: Espera Circular.
Justificativa lógica: as duas threads passam a disputar `LOCK_A` primeiro. Quem perde espera sem segurar nada, e `LOCK_B` continua livre para quem ganhou, que termina e libera os dois (`LOCK_B`, depois `LOCK_A`). Como ninguém pede um lock de ordem menor segurando um de ordem maior, o ciclo não consegue se formar. As outras três condições continuam valendo; quebrar uma já basta.

A pausa de 50 ms foi mantida para mostrar que o que resolve é a ordem de aquisição, e não o tempo.

Execução: `python3 deadlock_com_trava.py`

```
[ 0.001s] [Thread 1] quero o LOCK_A...
[ 0.001s] [Thread 1] peguei o LOCK_A
[ 0.001s] [Thread 2] quero o LOCK_A...
[ 0.052s] [Thread 1] agora quero o LOCK_B...
[ 0.052s] [Thread 1] peguei o LOCK_B
[ 0.052s] [Thread 1] dentro da seção crítica
[ 0.101s] [Thread 1] T1 concluiu
[ 0.101s] [Thread 1] larguei os dois locks
[ 0.101s] [Thread 2] peguei o LOCK_A
[ 0.151s] [Thread 2] agora quero o LOCK_B...
[ 0.152s] [Thread 2] peguei o LOCK_B
[ 0.152s] [Thread 2] dentro da seção crítica
[ 0.204s] [Thread 2] T2 concluiu
[ 0.204s] [Thread 2] larguei os dois locks
[ 0.204s] [Principal] as duas threads terminaram sem deadlock
```

4. Pseudocódigo do Protocolo

Versão que trava:

```
CONSTANTES:
  LOCK_A, LOCK_B = locks distintos

Thread 1:
  adquirir(LOCK_A)
  dormir(50ms)              // aumenta a chance do deadlock
  adquirir(LOCK_B)
  imprimir "T1 concluiu"
  liberar(LOCK_B)
  liberar(LOCK_A)

Thread 2:
  adquirir(LOCK_B)
  dormir(50ms)
  adquirir(LOCK_A)
  imprimir "T2 concluiu"
  liberar(LOCK_A)
  liberar(LOCK_B)
```

Versão corrigida (hierarquia de recursos):

```
Regra global: sempre adquirir LOCK_A antes de LOCK_B, em todas as threads

Thread 1 e Thread 2:
  adquirir(LOCK_A)
  adquirir(LOCK_B)
  // seção crítica
  liberar(LOCK_B)
  liberar(LOCK_A)
```

5. Referências

[1] TANENBAUM, A. S.; BOS, H. Modern Operating Systems. 4. ed. Pearson, 2014. Capítulo 6 (Deadlocks).

[2] SILBERSCHATZ, A.; GALVIN, P. B.; GAGNE, G. Operating System Concepts. 10. ed. Wiley, 2018. Capítulo sobre Deadlocks.

[3] PYTHON SOFTWARE FOUNDATION. threading — Thread-based parallelism. Python 3 Documentation. https://docs.python.org/3/library/threading.html

[4] PYTHON SOFTWARE FOUNDATION. sys — System-specific parameters and functions (sys._current_frames). Python 3 Documentation. https://docs.python.org/3/library/sys.html#sys._current_frames
