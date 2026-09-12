# Manual de uso do Git

Para o nosso projeto, o Git pode ser utilizado seguindo um fluxo simples. O repositório armazena o código e permite que cada integrante trabalhe em sua própria branch, evitando alterações diretas nas branches `main` e `dev`.

O Git já está incluído nos ambientes Nix do projeto. Consulte a [configuração do ambiente de desenvolvimento](configuracao-ambiente.md) para mais informações.

**Execute os comandos a seguir no diretório onde você clonou o projeto.** No exemplo utilizado no tutorial anterior, o diretório é `~/projetos/sistema-curriculo`.

### Verificando a branch atual

Para verificar em qual branch você está:

```bash
git branch
```

A branch marcada com `*` é a branch atual.

Para listar também as branches remotas:

```bash
git branch -a
```

No nosso projeto, a estrutura de branches seguirá, inicialmente, uma organização semelhante a esta:

```text
main
  │
  └── dev
       │
       ├── feature/curriculo
       ├── feature/login
       └── feature/frontend
```

Cada integrante deve trabalhar em uma branch própria.

**NÃO trabalhe diretamente na `main`.**
**NÃO trabalhe diretamente na `dev`.**

### Criando uma branch

Antes de criar uma nova branch, atualize a `dev`:

```bash
git checkout dev
git pull
```

Em seguida, crie sua branch:

```bash
git checkout -b minha-feature
```

Por exemplo:

```bash
git checkout -b feature/cadastro-aluno
```

A partir desse momento, você pode trabalhar nas alterações sem modificar diretamente a `dev`.

### Verificando as alterações

Durante o desenvolvimento, utilize:

```bash
git status
```

Esse comando mostra os arquivos modificados, novos arquivos e outras alterações que ainda não foram registradas em um commit.

### `git add`

Depois de realizar uma alteração, é necessário adicioná-la à área de preparação (*staging*):

```bash
git add .
```

O `.` adiciona todas as alterações do diretório atual.

Também é possível adicionar um arquivo específico:

```bash
git add arquivo.py
```

### `git commit`

O `commit` registra as alterações preparadas em uma nova versão do projeto:

```bash
git commit -m "Adiciona cadastro de alunos"
```

É recomendável realizar commits pequenos e utilizar mensagens que descrevam objetivamente o que foi alterado.

Por exemplo:

```bash
git commit -m "Corrige validação do formulário"
```

### Enviando as alterações: `git push`

O `commit` registra a alteração apenas no repositório local, ou seja, no seu computador.

Para enviar a branch e seus commits para o repositório remoto no GitHub, utilize:

```bash
git push
```

Na primeira vez que uma branch for enviada, pode ser necessário informar a branch de origem:

```bash
git push -u origin minha-feature
```

O fluxo básico é:

```text
git add
   ↓
git commit
   ↓
git push
   ↓
GitHub
```

### `git pull`

O comando `git pull` atualiza o repositório local com as alterações existentes no repositório remoto.

Por exemplo:

```bash
git pull
```

É recomendável atualizar sua branch antes de continuar o desenvolvimento, especialmente quando outros integrantes também estão trabalhando no projeto.

Um fluxo comum durante o desenvolvimento será:

```bash
git pull

# realizar alterações no código

git add .
git commit -m "Descrição da alteração"
git push
```

### Pull Request

É importante diferenciar `git push` de **Pull Request (PR)**.

O `git push` apenas envia seus commits para o repositório remoto.

Depois de enviar sua branch para o GitHub, você deve abrir um **Pull Request** para solicitar que suas alterações sejam incorporadas à `dev`.

O fluxo é:

```text
Sua branch
     │
     │ git push
     ▼
  GitHub
     │
     │ Pull Request
     ▼
    dev
```

No Pull Request, os demais integrantes podem revisar as alterações, verificar o código e solicitar correções, quando necessário.

Após a aprovação, o Pull Request poderá ser incorporado à `dev`.

A `main` seguirá um processo semelhante, recebendo alterações da `dev` por meio de Pull Request quando uma versão estiver pronta para ser integrada.
