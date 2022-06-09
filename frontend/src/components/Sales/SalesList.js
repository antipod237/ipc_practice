import React from 'react';
import {
  Datagrid, DateField, List, NumberField,
} from 'react-admin';

const SalesList = (props) => (
  <List {...props} bulkActionButtons={false} title="Продажи">
    <Datagrid rowClick="show">
      <NumberField source="id" label="Идентификатор" />
      <NumberField source="store_item_id" label="Id товара" />
      <NumberField source="value" label="Количество товара" />
      <DateField source="date" label="Дата" />
    </Datagrid>
  </List>
);

export default SalesList;
