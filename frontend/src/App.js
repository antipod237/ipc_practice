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
import SuppliersCreate from './components/Suppliers/SuppliersCreate';
import SuppliersList from './components/Suppliers/SuppliersList';
import SuppliersEdit from './components/Suppliers/SuppliersEdit';
import SuppliersShow from './components/Suppliers/SuppliersShow';
import StoresCreate from './components/Stores/StoresCreate';
import StoresList from './components/Stores/StoresList';
import StoresEdit from './components/Stores/StoresEdit';
import StoresShow from './components/Stores/StoresShow';
import ItemSetsList from './components/Item_sets/ItemSetsList';
import ItemSetsShow from './components/Item_sets/ItemSetsShow';
import ItemSetsEdit from './components/Item_sets/ItemSetsEdit';
import ItemSetsCreate from './components/Item_sets/ItemSetsCreate';
import PurchaseList from './components/Purchases/PurchaseList';
import PurchaseCreate from './components/Purchases/PurchaseCreate';
import PurchaseEdit from './components/Purchases/PurchaseEdit';
import PurchaseShow from './components/Purchases/PurchaseShow';
import SalesCreate from './components/Sales/SalesCreate';
import SalesList from './components/Sales/SalesList';
import SalesEdit from './components/Sales/SalesEdit';
import SalesShow from './components/Sales/SalesShow';
import RoleList from './components/Roles/RoleList';
import RoleShow from './components/Roles/RoleShow';
import UserCreate from './components/Users/UserCreate';
import UserEdit from './components/Users/UserEdit';
import UserList from './components/Users/UserList';
import UserShow from './components/Users/UserShow';
import StoreItemsCreate from './components/Store_items/Store_itemsCreate';
import StoreItemsEdit from './components/Store_items/Store_itemsEdit';
import StoreItemsList from './components/Store_items/Store_itemsList';
import StoreItemsShow from './components/Store_items/Store_itemsShow';
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
          name="suppliers"
          list={SuppliersList}
          show={SuppliersShow}
          create={checkAppAction(permissions.users, 'create') ? SuppliersCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? SuppliersEdit : null}
          options={{ label: 'Поставщики' }}
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
          name="stores"
          list={StoresList}
          show={StoresShow}
          create={checkAppAction(permissions.users, 'create') ? StoresCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? StoresEdit : null}
          options={{ label: 'Магазины' }}
        />
      ) : null,
      permissions.users ? (
        <Resource
          name="purchases"
          list={PurchaseList}
          show={PurchaseShow}
          create={checkAppAction(permissions.users, 'create') ? PurchaseCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? PurchaseEdit : null}
          options={{ label: 'Закупки' }}
        />
      ) : null,
      permissions.users ? (
        <Resource
          name="sales"
          list={SalesList}
          show={SalesShow}
          create={checkAppAction(permissions.users, 'create') ? SalesCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? SalesEdit : null}
          options={{ label: 'Продажи' }}
        />
      ) : null,
      permissions.users ? (
        <Resource
          name="storeitems"
          list={StoreItemsList}
          show={StoreItemsShow}
          create={checkAppAction(permissions.users, 'create') ? StoreItemsCreate : null}
          edit={checkAppAction(permissions.users, 'update') ? StoreItemsEdit : null}
          options={{ label: 'Товары' }}
        />
      ) : null,
    ]}
  </Admin>
);

export default App;
