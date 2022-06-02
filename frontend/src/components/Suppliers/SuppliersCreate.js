import React from 'react';
import {
  Create, SimpleForm, TextInput,
} from 'react-admin';

const SuppliersCreate = (props) => (
  <Create title="Новый поставщик" {...props}>
    <SimpleForm>
      <TextInput source="name" label="Название" />
      <TextInput source="email" label="Почта" />
      <TextInput source="phone_number" label="Телефонный номер" />
      <TextInput source="address" label="Адрес" />
    </SimpleForm>
  </Create>
);

export default SuppliersCreate;
