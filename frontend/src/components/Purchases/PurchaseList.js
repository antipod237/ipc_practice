import React from 'react';
import {
  Datagrid, DateField, List, NumberField, BooleanField,
} from 'react-admin';

const PurchaseList = (props) => (
  <List {...props} bulkActionButtons={false} title="Закупки">
    <Datagrid rowClick="show">
      <NumberField source="id" label="Идентификатор" />
      <NumberField source="item_set_id" label="Id Номенклатуры" />
      <NumberField source="store_item_id" label="Id товара" />
      <NumberField source="value" label="Количество товара" />
      <DateField source="date" label="Дата" />
      <BooleanField source="is_complete" label="Выполнена?" />
    </Datagrid>
  </List>
);

export default PurchaseList;
