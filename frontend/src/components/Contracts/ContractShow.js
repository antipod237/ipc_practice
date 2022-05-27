import React from 'react';
import {
  DateField, Show, SimpleShowLayout, TextField,
} from 'react-admin';

const ContractShow = (props) => (
  <Show {...props} title="Подробнее о договоре">
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="number" label="Дело №" />
      <TextField source="supplier_id" label="Id поставщика" />
      <DateField source="start_date" label="Дата подписания договора" />
      <DateField source="end_date" label="Дата окончания договора" />
    </SimpleShowLayout>
  </Show>
);

export default ContractShow;
