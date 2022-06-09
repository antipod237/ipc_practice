import React from 'react';
import {
  Datagrid, List, TextField,
} from 'react-admin';

const StoreItemsList = (props) => (
  <List {...props} bulkActionButtons={false} title="Товары">
    <Datagrid rowClick="show">
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Название" />
      <TextField source="value" label="Количество" />
      <TextField source="max_value" label="Максимальное количество" />
      <TextField source="store_id" label="id магазина" />
      <TextField source="remaining_space" label="Свободное место на складе" />
    </Datagrid>
  </List>
);

export default StoreItemsList;
