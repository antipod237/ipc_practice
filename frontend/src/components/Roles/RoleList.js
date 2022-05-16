import React from 'react';
import {
  List,
  Datagrid,
  TextField,
} from 'react-admin';

const RoleList = (props) => (
  <List {...props} title="Роли">
    <Datagrid rowClick="show">
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Имя в системе" />
      <TextField source="displayName" label="Отображаемое имя" />
    </Datagrid>
  </List>
);

export default RoleList;
