import React from 'react';
import {
  Edit, SimpleForm, TextInput,
} from 'react-admin';
import { EditActions, EntityTitle } from '../utils';

const SuppliersEdit = (props) => (
  <Edit title={<EntityTitle filedName="name" />} undoable={false} actions={<EditActions />} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" label="Идентификатор" />
      <TextInput disabled source="name" label="Название" />
      <TextInput source="email" label="Почта" />
      <TextInput source="phone_number" label="Телефонный номер" />
      <TextInput source="address" label="Адрес" />
    </SimpleForm>
  </Edit>
);

export default SuppliersEdit;
