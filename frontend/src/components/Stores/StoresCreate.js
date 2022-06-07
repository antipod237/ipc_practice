import React from 'react';
import {
  Create, SimpleForm, TextInput,
} from 'react-admin';

const StoresCreate = (props) => (
  <Create title="Новый магазин" {...props}>
    <SimpleForm>
      <TextInput source="address" label="Адрес" />
      <TextInput source="phone_number" label="Телефонный номер" />
      <TextInput source="email" label="Почта" />
    </SimpleForm>
  </Create>
);

export default StoresCreate;
