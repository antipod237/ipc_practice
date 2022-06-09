import React from 'react';
import {
  Edit, SimpleForm, TextInput,
} from 'react-admin';
import { EditActions, EntityTitle } from '../utils';

const StoresEdit = (props) => (
  <Edit title={<EntityTitle filedName="name" />} undoable={false} actions={<EditActions />} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" label="Идентификатор" />
      <TextInput source="address" label="Адрес" />
      <TextInput source="phone_number" label="Телефонный номер" />
      <TextInput source="email" label="Почта" />
    </SimpleForm>
  </Edit>
);

export default StoresEdit;
