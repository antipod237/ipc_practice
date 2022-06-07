import React from 'react';
import {
  Datagrid, List, TextField,
} from 'react-admin';

const StoresList = (props) => (
  <List {...props} bulkActionButtons={false} title="Магазины">
    <Datagrid rowClick="show">
      <TextField source="id" label="Идентификатор" />
      <TextField source="address" label="Адрес" />
      <TextField source="phone_number" label="Телефонный номер" />
      <TextField source="email" label="Почта" />
    </Datagrid>
  </List>
);

export default StoresList;
