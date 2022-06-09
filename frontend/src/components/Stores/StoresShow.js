import React from 'react';
import {
  Show, SimpleShowLayout, TextField,
} from 'react-admin';

const StoresShow = (props) => (
  <Show {...props} title="Подробнее о магазине">
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="address" label="Адрес" />
      <TextField source="phone_number" label="Телефонный номер" />
      <TextField source="email" label="Почта" />
    </SimpleShowLayout>
  </Show>
);

export default StoresShow;
