import React from 'react';
import {
  Create, SimpleForm, TextInput, NumberInput,
} from 'react-admin';

const StoreItemsCreate = (props) => (
  <Create title="Новый товар" {...props}>
    <SimpleForm>
      <TextInput source="name" label="Название" />
      <NumberInput source="value" label="Количество" />
      <NumberInput source="max_value" label="Максимальное количество" />
      <NumberInput source="store_id" label="id магазина" />
    </SimpleForm>
  </Create>
);

export default StoreItemsCreate;
