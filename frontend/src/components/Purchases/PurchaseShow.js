import React from 'react';
import {
  DateField, Show, SimpleShowLayout, TextField, ArrayField, Datagrid, NumberField, BooleanField,
} from 'react-admin';

const PurchaseShow = (props) => (
  <Show {...props} title="Подробнее о закупке">
    <SimpleShowLayout>
      <NumberField source="id" label="Идентификатор" />
      <NumberField source="item_set_id" label="Id номенклатуры" />
      <NumberField source="store_item_id" label="Id товара" />
      <NumberField source="value" label="Кол-во товара" />
      <DateField source="date" label="Дата" />
      <BooleanField source="is_complete" label="Выполнена?" />
      <ArrayField source="item_sets" label="Номенклатура">
        <Datagrid>
          <NumberField source="item_set_id" label="Id номенклатуры" />
          <TextField source="name" label="Наименование" />
        </Datagrid>
      </ArrayField>
      <ArrayField source="store_items" label="Товар">
        <Datagrid>
          <NumberField source="store_item_id" label="Id товара" />
          <TextField source="name" label="Наименование" />
          <NumberField source="value" label="Кол-во" />
        </Datagrid>
      </ArrayField>
      <ArrayField source="users" label="Пользователь">
        <Datagrid>
          <NumberField source="user_id" label="Id пользователя" />
          <TextField source="username" label="Имя пользователя" />
        </Datagrid>
      </ArrayField>
    </SimpleShowLayout>
  </Show>
);

export default PurchaseShow;
