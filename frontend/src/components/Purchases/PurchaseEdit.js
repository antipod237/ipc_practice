import React from 'react';
import {
  DateInput, Edit, SimpleForm, NumberInput, BooleanInput,
} from 'react-admin';
import { EditActions } from '../utils';

const PurchaseEdit = (props) => (
  <Edit undoable={false} actions={<EditActions />} {...props}>
    <SimpleForm>
      <NumberInput source="item_set_id" label="Id Номенклатуры" />
      <NumberInput source="store_item_id" label="Id товара" />
      <NumberInput source="value" label="Количество товара" />
      <NumberInput source="user_id" label="Id пользователя" />
      <DateInput source="date" label="Дата" />
      <BooleanInput source="is_complete" label="Выполнена?" />
    </SimpleForm>
  </Edit>
);

export default PurchaseEdit;
