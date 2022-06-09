import React from 'react';
import {
  DateInput, Edit, NumberInput, SimpleForm,
} from 'react-admin';
import { EditActions } from '../utils';

const SalesEdit = (props) => (
  <Edit undoable={false} actions={<EditActions />} {...props}>
    <SimpleForm>
      <NumberInput source="store_item_id" label="Id товара" />
      <NumberInput source="value" label="Количество товара" />
      <DateInput source="date" label="Дата" />
    </SimpleForm>
  </Edit>
);

export default SalesEdit;
