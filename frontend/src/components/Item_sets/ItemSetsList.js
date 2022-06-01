import React from 'react';
import {
  Datagrid, List, TextField,
} from 'react-admin';

const ItemSetsList = (props) => (
  <List {...props} bulkActionButtons={false} title="Номенклатура">
    <Datagrid rowClick="show">
      <TextField source="id" label="id" />
      <TextField source="name" label="Название" />
    </Datagrid>
  </List>
);

export default ItemSetsList;
