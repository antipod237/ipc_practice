# ipc_practice
Практика Интерпроком 2022

# Предприятие и диаграмма баз данных

Предприятие: "xs5 retail group"

Таблицы базы данных: users, roles, permissions, purchases, item_sets, contracts_item_sets, contracts, suppliers, store items, stores, sales

![database](https://user-images.githubusercontent.com/86552792/168637807-c4906407-053c-4e08-ad85-c9d4911cfab9.png)

# Ролевая модель системы для разных приложений системы

![model](https://user-images.githubusercontent.com/86552792/168633591-e6970f2a-22dd-4f82-a81c-eaf85aef2b3b.png)

# ТЗ

Создать информационную систему для небольшой сети продуктовых магазинов. Система должна позволять отслеживать наличие товаров на складе, отслеживать продажи, создавать запросы на поставки, вести учет поставщиков и заключенных с ними контрактов.

В основе будет:
* БД – Postgres
* Бэк – Python + Starlette
* Клиент – js, react, reactadmin
* Оценка качества кода – Flake 8
