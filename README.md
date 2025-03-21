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

A simple graphical interface to interact with SQLite databases, allowing the creation, opening, manipulation, and execution of SQL queries in an intuitive way.

![alt text](https://github.com/hipolitorodrigues/assets-for-github/blob/c635ca704784fb96353b99b3980c08050958a33e/images/01/img-sqlite_interface1.png)

![alt text](https://github.com/hipolitorodrigues/assets-for-github/blob/c635ca704784fb96353b99b3980c08050958a33e/images/01/img-sqlite_interface2.png)

## 📌 Features
- Create and open SQLite databases.
- Explore available tables and views.
- Execute custom SQL queries.
- Display query results in a user-friendly graphical interface.
- Responsive interface using `tkinter` and `ttkbootstrap`.

## ✅ Notes
- There are 64 buttons in the Top Section. For now, only 4 have functionality: "New DB", "Open DB", "Close DB", and "Update". Other functions will be assigned to the remaining buttons in the future.
- The "Execute" query button is not very visible. It doesn't look much like a button. It’s a mark in the bottom-left corner of the blue area. It works, but a future update will improve this.
- For now, the query is executed only through the "Execute" button mentioned above.
- It executes one query at a time.

## 📚 Translation Progress:
- app.py: 100%
- SQLite_Interface.exe: 80%

![alt text](https://github.com/hipolitorodrigues/assets-for-github/blob/c635ca704784fb96353b99b3980c08050958a33e/images/01/img-sqlite_interface3.png)

![alt text](https://github.com/hipolitorodrigues/assets-for-github/blob/c635ca704784fb96353b99b3980c08050958a33e/images/01/img-sqlite_interface4.png)

## 🛠️ Installation and Usage - EASY MODE (No installation required):

### 1. Download the portable\SQLite_Interface.exe file, double-click it, and enjoy 🚀.

## 🛠️ Installation and Usage - "HARD" MODE:

### 1. Clone the repository
```sh
git clone https://github.com/your-username/just-a-sqlite-interface.git
cd just-a-sqlite-interface
```

### 2. Create and activate a virtual environment (optional, but recommended)
```sh
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the app 🚀

Execute the application with the following command:
```sh
python app.py
```

### 📌 How to use the interface
1. **Create a new database:** Click the "New DB" button and choose where to save the `.db` file.
2. **Open an existing database:** Click "Open DB" and select an SQLite file.
3. **View structure:** The left sidebar will display the tables and views of the connected database.
4. **Execute SQL queries:** Type commands in the query area and click "Execute Query".
5. **Close the database:** Click the "Close DB" button to disconnect.

## 📚 Useful SQLite Commands

- List tables in the database:
  ```sql
  SELECT name FROM sqlite_master WHERE type='table';
  ```
  ```sql
  SELECT * FROM sqlite_master LIMIT 100;
  ```
- Get columns of a table:
  ```sql
  PRAGMA table_info(table_name);
  ```
- Create a new table:
  ```sql
  CREATE TABLE customers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT,
      phone TEXT
  );
  ```
- Insert data into the new table:
  ```sql
  INSERT INTO customers (name, email, phone) VALUES
      ('James Ford', 'jamesford@email.com', '(11) 91234-5678'),
      ('Kate Austen', 'kateausten@email.com', '(21) 92345-6789'),
      ('Sayid Jarrah', 'sayidjarrah@email.com', '(31) 93456-7890');
  ```

## ⭐ Developer

- **Developer**: Hipolito Rodrigues
- **Creation Date**: 03/18/2025
- **Last Update**: 03/19/2025
- **Current Version**: 0.9

---

## 📜 License

This project is licensed under the MIT License. This means you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, as long as you keep the original copyright notice and license included in all copies or substantial portions of the software.

## 🔥 Contributions

Contributions are welcome! Feel free to send problems or pull requests to improve the project.

---
