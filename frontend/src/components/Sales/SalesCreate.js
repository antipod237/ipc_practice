import React from 'react';
import {
  Create, DateInput, NumberInput, SimpleForm,
} from 'react-admin';

const SalesCreate = (props) => (
  <Create title="Новая продажа" {...props}>
    <SimpleForm>
      <NumberInput source="store_item_id" label="Id товара" />
      <NumberInput source="value" label="Количество товара" />
      <DateInput source="date" label="Дата" />
    </SimpleForm>
  </Create>
);

export default SalesCreate;
