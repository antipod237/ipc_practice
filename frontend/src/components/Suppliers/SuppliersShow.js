import React from 'react';
import {
  Show, SimpleShowLayout, TextField,
} from 'react-admin';
import { EntityTitle } from '../utils';

const SuppliersShow = (props) => (
  <Show {...props} title={<EntityTitle filedName="name" />}>
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Название" />
      <TextField source="email" label="Почта" />
      <TextField source="phone_number" label="Телефонный номер" />
      <TextField source="address" label="Адрес" />
    </SimpleShowLayout>
  </Show>
);

export default SuppliersShow;
