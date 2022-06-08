import React from 'react';
import {
  Create, DateInput, NumberInput, SimpleForm, BooleanInput,
} from 'react-admin';

const PurchaseCreate = (props) => (
  <Create title="Новая закупка" {...props}>
    <SimpleForm>
      <NumberInput source="item_set_id" label="Id Номенклатуры" />
      <NumberInput source="store_item_id" label="Id товара" />
      <NumberInput source="value" label="Количество товара" />
      <NumberInput source="user_id" label="Id пользователя" />
      <DateInput source="date" label="Дата" />
      <BooleanInput source="is_complete" label="Выполнена?" />
    </SimpleForm>
  </Create>
);

export default PurchaseCreate;
