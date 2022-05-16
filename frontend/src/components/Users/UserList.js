import React from 'react';
import {
  List,
  Datagrid,
  TextField,
  ReferenceField,
} from 'react-admin';
import { ListActions } from '../utils';

const UserList = (props) => (
  <List {...props} actions={<ListActions permissionName="users" />} title="Пользователи">
    <Datagrid rowClick="show">
      <TextField source="id" label="Идентификатор" />
      <TextField source="displayName" label="ФИО" />
      <ReferenceField link="show" label="Роль" source="roleId" reference="roles">
        <TextField source="displayName" />
      </ReferenceField>
    </Datagrid>
  </List>
);

export default UserList;
