## DEMOAUTH
Простой пример авторизации на FastApi. В рамках проекта реализованы запрос на 
авторизацию существующего пользователя и форма авторизации (UI). В базе хранятся пользователи с уже захешированными 
паролями. 
### Стек
- [FastApi](https://github.com/tiangolo/fastapi)
- [Pydentic](https://github.com/pydantic/pydantic)
- [Uvicorn](https://github.com/encode/uvicorn)
- [SqlAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [Sqlite](https://github.com/sqlite/sqlite)

### Установка (MacOs M1)

#### 1) Клонирование проекта:
```
git clone git clone git@github.com:justyfay/pybooking.git
```
#### 2) Установка poetry:
```
open /Applications/Python\ 3.12/Install\ Certificates.command
```
```
curl -sSL https://install.python-poetry.org | python3.12 -
```
```
poetry install
```
```
poetry shell
```
В случае с ошибкой **setuptools** в PyCharm выполнить:
```
poetry add --group dev setuptools
```
#### 3) Генерация своего PASSWORD_SALT и SECRET_KEY для добавления цифровой подписи в Cookies:
```
openssl rand -hex 32
```
#### 4) ENV Example:
```
SECRET_KEY=99b4aef3cd966fda701668e41ab8622de476ae2a544ac31e8e22cb22008ba8a4
PASSWORD_SALT=dcd3fd3c419643e56999df7ba5969177301a440fbaa3c67902a9892b48897496
SQLITE_URL=sqlite+aiosqlite:///demo-auth.db
```
#### 5) Добавление своего пользователя в БД:

1) Добавить информацию по юзеру в файл **users.csv**.
2) Придумать пароль пользователю и выполнить его хеширование. Можно через Python IDLE.
<br>Если сервер запущен, то после добавления/изменения пользователя требуется перезапуск.
```
# Run terminal command in project directory
python3.12
```
```
# Code in IDLE
Python 3.12.0 (v3.12.0:0fb18b02c8, Oct  2 2023, 09:45:56) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import hashlib
>>> from env import PASSWORD_SALT
>>> hashlib.sha256(("You_User_Pass" + PASSWORD_SALT).encode()).hexdigest()
'ee46fd585ad056bd10fafd45b216cb61242d1f9c527e6299e400c2f7584452d6'
```
#### 3) Запуск:
```
uvicorn server:app --reload
```
### Тестирование
При запуске, по умолчанию в базе уже будет два пользователя с захешированными паролями.
- Пароль пользователя **user@example.ru** - _UserEx12345_.
- Пароль пользователя **test_manual@google.com** - _Test:manUaL@009j!_.
