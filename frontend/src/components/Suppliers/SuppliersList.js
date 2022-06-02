import React from 'react';
import {
  Datagrid, List, TextField,
} from 'react-admin';

const SuppliersList = (props) => (
  <List {...props} bulkActionButtons={false} title="Поставщики">
    <Datagrid rowClick="show">
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Название" />
      <TextField source="email" label="Почта" />
      <TextField source="phone_number" label="Телефонный номер" />
      <TextField source="address" label="Адрес" />
    </Datagrid>
  </List>
);

export default SuppliersList;
