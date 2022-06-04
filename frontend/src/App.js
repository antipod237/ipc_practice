import polyglotI18nProvider from 'ra-i18n-polyglot';
import russianMessages from 'ra-language-russian';
import React from 'react';
import { Admin, Resource } from 'react-admin';
import authProvider from './api/authProvider';
import dataProvider from './api/dataProvider';
import './App.less';
import ContractCreate from './components/Contracts/ContractCreate';
import ContractEdit from './components/Contracts/ContractEdit';
import ContractList from './components/Contracts/ContractList';
import ContractShow from './components/Contracts/ContractShow';
import ItemSetsList from './components/Item_sets/ItemSetsList';
import ItemSetsShow from './components/Item_sets/ItemSetsShow';
import ItemSetsEdit from './components/Item_sets/ItemSetsEdit';
import ItemSetsCreate from './components/Item_sets/ItemSetsCreate';
import RoleList from './components/Roles/RoleList';
import RoleShow from './components/Roles/RoleShow';
import UserCreate from './components/Users/UserCreate';
import UserEdit from './components/Users/UserEdit';
import UserList from './components/Users/UserList';
import UserShow from './components/Users/UserShow';
import { checkAppAction } from './utils';

const i18nProvider = polyglotI18nProvider(() => russianMessages, 'ru');

const App = () => (
  <Admin
    title="Erp System"
    dataProvider={dataProvider}
    authProvider={authProvider}
    i18nProvider={i18nProvider}
  >
    {(permissions) => [
      permissions.users ? (
        <Resource
          name="users"
          list={UserList}
          show={UserShow}
          create={checkAppAction(permissions.users, 'create') ? UserCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? UserEdit : null}
          options={{ label: 'Пользователи' }}
        />
      ) : null,
      permissions.users ? (
        <Resource
          name="roles"
          list={RoleList}
          options={{ label: 'Роли' }}
          show={RoleShow}
        />
      ) : null,
      permissions.users ? (
        <Resource
          name="contracts"
          list={ContractList}
          show={ContractShow}
          create={checkAppAction(permissions.users, 'create') ? ContractCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? ContractEdit : null}
          options={{ label: 'Договоры' }}
        />
      ) : null,
      permissions.users ? (
        <Resource
          name="itemsets"
          list={ItemSetsList}
          show={ItemSetsShow}
          create={checkAppAction(permissions.users, 'create') ? ItemSetsCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? ItemSetsEdit : null}
          options={{ label: 'Номенклатура' }}
        />
      ) : null,
      permissions.users ? (
        <Resource
          name="itemsets"
          list={ItemSetsList}
          show={ItemSetsShow}
          create={checkAppAction(permissions.users, 'create') ? ItemSetsCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? ItemSetsEdit : null}
          options={{ label: 'Номенклатура' }}
        />
      ) : null,
    ]}
  </Admin>
);

export default App;
