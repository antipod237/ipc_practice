# React Front-end
## Basics
Общая структура и настройки созданы с помощью create-react-app утилиты.
В разработке будут в первую очередь использоваться хуки вместо написания классов.
Ссылки:
- **[React](https://ru.reactjs.org/docs/hello-world.html)**
- **[React Хуки](https://ru.reactjs.org/docs/hooks-intro.html)**
- **[LESS CSS](http://lesscss.org)**

## Code Style
В проекте придерживаемся Airbnb Style Guide для JavaScript ([референс](https://github.com/airbnb/javascript)).
Запоминать гайд целиком не обязательно, т.к. есть линтер ESLint с плагином airbnb. **Подключить линтер к своей IDE/редактору или npm run lint**.
Базовые положения:
- Табуляция в два пробела
- Точки с запятой всегда, где нужно
- Одинарные кавычки для строк
- Длина строки не более 80 символов
- Доступ к методам только через точку (`user.name NOT user['name']`)
- camelCase для переменных и функций
- `const` или `let` вместо `var`
- деструктуризация объектов

## Структура проекта
```
src
|___components
|       ....
|___routes
|       ....
|___assets
|       ....
|___api
```
- В папке `components` помещаются папки с названием компонента, содержащие `UserList.js` с объявлением компонента и `style.less` с его стилями.
- В папке `routes` помещаются папки с названием страницы, содержащие аналогичные `UserList.js` и `style.less`
- Папка `assets` предназначена для хранения картинок, иконок и проч.
- Папка `api` будет содержать файл с объявлением axios и вспомогательными функциями в зависимости от архитектуры.

## Component
В данном проекте используются функциональные (беcклассовые) компоненты на основе стрелочных функций.
Общая структура компонента с возвращаемым значением сразу после стрелки:
```JavaScript
import React from 'react';
import classNames from 'classnames/bind';
import style from './style.less';

const cx = classNames.bind(style);

const Component = ({props}) => (
  <div className={cx('Classname')}>
    {props}
  </div>
);

export default Component;
```
Более комплексная структура с функциями:
```JavaScript
--//--
const Component = ({props}) => {
    const val = 'val';

    const func1 = () => {
        console.log('Hello');
    }

    const func2 = () => {
        console.log('Goodbye')
    }

    return (
        <div>
    );
};
--//--
```
## Router
Страницы по сути представляют собой те же компоненты. Используются в компоненте Router (находится в App.js) для переключения между ними.
Пример:
```JavaScript
<Router>
    <Switch>
        <Route path="/about" component={AboutPage}>
        <Route path="/" component={HomePage}>
    </Switch>
</Router>
```
## Styles
В приоритете адаптивность страницы.
Нейминг классов осуществляется с помощью функции из библиотеки `classnames` для объединения нескольких имен и динамического наименования ([src](https://www.npmjs.com/package/classnames))

Нейминг, наверное, свободный, с помощью существительных, используя PascalCase и какое-то подобие иерархичности (например, `.Card` для родительского элемента и `.CardTitle` для дочернего)
## Axios
Для создания REST запросов будет использоваться библиотека [Axios](https://github.com/axios/axios). Работа с запросами осуществляется в основном с помощью хуков `useState()` и `useEffect()`.
