import React from 'react';
import {
  DateInput, Edit, SimpleForm, TextInput, NumberInput,
} from 'react-admin';
import { EntityTitle, EditActions } from '../utils';

const ContractEdit = (props) => (
  <Edit title={<EntityTitle filedName="number" />} undoable={false} actions={<EditActions />} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" label="Идентификатор" />
      <TextInput source="number" label="Дело №" />
      <NumberInput source="supplier_id" label="Id поставщика" />
      <DateInput source="start_date" label="Дата подписания договора" />
      <DateInput source="end_date" label="Дата окончания договора" />
    </SimpleForm>
  </Edit>
);

export default ContractEdit;
