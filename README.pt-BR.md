<div align="center">
   <img height="30" width="40" src="https://github.com/hipolitorodrigues/assets-for-github/blob/985021e61af3982fd9f28be446b106b958f24696/images/01/img-readme-ico.svg">
   <a href="./README.md">
      <img height="30" width="120" src="https://github.com/hipolitorodrigues/assets-for-github/blob/985021e61af3982fd9f28be446b106b958f24696/images/01/img-readme-en.svg">
   </a>
   <a href="./README.pt-BR.md">
      <img height="30" width="60" src="https://github.com/hipolitorodrigues/assets-for-github/blob/985021e61af3982fd9f28be446b106b958f24696/images/01/img-readme-pt-br.svg">
   </a>
</div>

# Just a SQLite Interface

Uma interface gráfica simples para interagir com bancos de dados SQLite, permitindo a criação, abertura, manipulação e execução de consultas SQL de forma intuitiva.

![alt text](https://github.com/hipolitorodrigues/assets-for-github/blob/c635ca704784fb96353b99b3980c08050958a33e/images/01/img-sqlite_interface1.png)

![alt text](https://github.com/hipolitorodrigues/assets-for-github/blob/c635ca704784fb96353b99b3980c08050958a33e/images/01/img-sqlite_interface2.png)

## 📌 Funcionalidades
- Criar e abrir bancos de dados SQLite.
- Explorar tabelas e views disponíveis.
- Executar consultas SQL personalizadas.
- Exibir resultados das consultas em uma interface gráfica amigável.
- Interface responsiva usando `tkinter` e `ttkbootstrap`.

## ✅ Observações
- Há 64 botões na Top Section. Por enquanto apenas 4 têem função. "New DB", "Open DB", "Close DB" e "Update". Outras funções serão atribuídas aos demais botões no futuro.
- O botão para "Executar" a query está pouco visível. Ainda não se parece com um botão. É uma marca no canto inferior esquerdo da área azul. Funciona, mas uma atualização futura irá melhorar isso.
- Por enquanto, a query é executada apenas através do botão "Executar" mensionado acima.
- Executa uma query por vez.

## 📚 Progresso da tradução para o inglês:
- Comentários: 50%
- Avisos de Erro: 70%
- Funções: 30%
- Interface: 100%

## 🛠️ Instalação e Uso - MODO FÁCIL (Não precisa de instalação):

### 1. Baixe o arquivo portable\SQLite_Interface.exe, dois cliques e divirta-se 🚀.

![alt text](https://github.com/hipolitorodrigues/assets-for-github/blob/c635ca704784fb96353b99b3980c08050958a33e/images/01/img-sqlite_interface3.png)

![alt text](https://github.com/hipolitorodrigues/assets-for-github/blob/c635ca704784fb96353b99b3980c08050958a33e/images/01/img-sqlite_interface4.png)

## 🛠️ Instalação e Uso - MODO "DIFÍCIL":

### 1. Clonar o repositório
```sh
git clone https://github.com/seu-usuario/just-a-sqlite-interface.git
cd just-a-sqlite-interface
```

### 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)
```sh
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/macOS
source venv/bin/activate
```

### 3. Instalar dependências
```sh
pip install -r requirements.txt
```

### 4. Usar 🚀

Execute o aplicativo com o seguinte comando:
```sh
python app.py
```

### 📌 Como usar a interface
1. **Criar um novo banco:** Clique no botão "Novo Banco" e escolha onde salvar o arquivo `.db`.
2. **Abrir um banco existente:** Clique em "Abrir Banco" e selecione um arquivo SQLite.
3. **Visualizar estrutura:** A árvore lateral esquerda exibirá tabelas e views do banco conectado.
4. **Executar consultas SQL:** Digite comandos na área de consultas e clique em "Executar Consulta".
5. **Fechar o banco:** Clique no botão "Fechar Banco" para desconectar.

## 📚 Comandos úteis no SQLite

- Listar tabelas do banco:
  ```sql
  SELECT name FROM sqlite_master WHERE type='table';
  ```
  ```sql
  SELECT * FROM sqlite_master LIMIT 100;
  ```
- Obter colunas de uma tabela:
  ```sql
  PRAGMA table_info(nome_da_tabela);
  ```
- Criar uma nova tabela:
  ```sql
  CREATE TABLE clientes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      email TEXT,
      telefone TEXT
  );
  ```
- Inserir dados na nova tabela:
  ```sql
  INSERT INTO clientes (nome, email, telefone) VALUES
      ('James Ford', 'jamesford@email.com', '(11) 91234-5678'),
      ('Kate Austen', 'kateausten@email.com', '(21) 92345-6789'),
      ('Sayid Jarrah', 'sayidjarrah@email.com', '(31) 93456-7890');
  ```

## ⭐ Developer

- **Developer**: Hipolito Rodrigues
- **Creation Date**: 18/03/2025
- **Last Update**: 19/03/2025
- **Current Version**: 0.9

---

## 📜 License

This project is licensed under the MIT License. This means you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, as long as you keep the original copyright notice and license included in all copies or substantial portions of the software.

## 🔥 Contributions

Contributions are welcome! Feel free to send problems or pull requests to improve the project.

---
