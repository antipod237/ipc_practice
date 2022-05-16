import React from 'react';
import {
  Show,
  SimpleShowLayout,
  TextField,
  BooleanField,
  ReferenceField,
} from 'react-admin';
import { EntityTitle, ShowActions } from '../utils';

const UserShow = (props) => (
  <Show title={<EntityTitle filedName="displayName" />} actions={<ShowActions permissionName="users" />} {...props}>
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="username" label="Логин" />
      <TextField source="displayName" label="ФИО" />
      <BooleanField source="deactivated" label="Деактивирован?" />
      <TextField source="email" label="Электронная почта" />
      <ReferenceField link="show" label="Роль" source="roleId" reference="roles">
        <TextField source="displayName" />
      </ReferenceField>
    </SimpleShowLayout>
  </Show>
);

export default UserShow;
