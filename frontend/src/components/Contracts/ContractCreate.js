import React from 'react';
import {
  Create, DateInput, required, SimpleForm, TextInput, NumberInput,
} from 'react-admin';

const ContractCreate = (props) => (
  <Create title="Новый контракт" {...props}>
    <SimpleForm>
      <TextInput source="number" label="Дело №" validate={required()} />
      <NumberInput source="supplier_id" label="Id поставщика" validate={required()} />
      <DateInput source="start_date" label="Дата подписания договора" />
      <DateInput source="end_date" label="Дата окончания договора" />
    </SimpleForm>
  </Create>
);

export default ContractCreate;
