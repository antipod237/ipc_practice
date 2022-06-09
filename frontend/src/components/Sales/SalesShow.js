import React from 'react';
import {
  ArrayField, Datagrid, DateField, NumberField, Show, SimpleShowLayout, TextField,
} from 'react-admin';

const SalesShow = (props) => (
  <Show {...props} title="Подробнее о продаже">
    <SimpleShowLayout>
      <NumberField source="id" label="Идентификатор" />
      <NumberField source="store_item_id" label="Id товара" />
      <NumberField source="value" label="Кол-во товара" />
      <DateField source="date" label="Дата" />
      <ArrayField source="store_items" label="Товар">
        <Datagrid>
          <NumberField source="store_item_id" label="Id товара" />
          <TextField source="name" label="Наименование" />
          <NumberField source="value" label="Кол-во" />
        </Datagrid>
      </ArrayField>
    </SimpleShowLayout>
  </Show>
);

export default SalesShow;
