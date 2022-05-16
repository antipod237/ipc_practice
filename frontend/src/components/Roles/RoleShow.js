import React from 'react';
import {
  Show,
  SimpleShowLayout,
  TextField,
} from 'react-admin';
import { EntityTitle } from '../utils';

const RoleShow = (props) => (
  <Show title={<EntityTitle filedName="displayName" />} {...props}>
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Имя в системе" />
      <TextField source="displayName" label="Отображаемое имя" />
    </SimpleShowLayout>
  </Show>
);

export default RoleShow;
