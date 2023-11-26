## DEMOAUTH
Простой пример авторизации на FastApi. В рамках проекта реализованы запрос на 
авторизацию существующего пользователя и форма авторизации (UI). Авторизация через пользователей из файла users.csv.
Пароли пользователей - 12345.

## Установка (MacOs M1)

#### 1) Клонирование проекта:
```
git clone git clone git@github.com:justyfay/pybooking.git                                                                   ─╯
```
#### 2) Установка poetry:
```
open /Applications/Python\ 3.12/Install\ Certificates.command                                                     ─╯                                                              ─╯
```
```
curl -sSL https://install.python-poetry.org | python3.12 -                                                     ─╯                                                              ─╯
```
```
poetry install                                                                                                                                                   ─╯
```
```
poetry shell                                                                                                                                                   ─╯
```
В случае с ошибкой **setuptools** в PyCharm выполнить:
```
poetry add --group dev setuptools
```
#### 3) Запуск:
```
uvicorn server:app --reload
```
#### 4) ENV Example:
```
SECRET_KEY=99b4aef3cd966fda701668e41ab8622de476ae2a544ac31e8e22cb22008ba8a4
PASSWORD_SALT=dcd3fd3c419643e56999df7ba5969177301a440fbaa3c67902a9892b48897496
SQLITE_URL=sqlite+aiosqlite:///demo-auth.db
```