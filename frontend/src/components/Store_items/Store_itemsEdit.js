import React from 'react';
import {
  Edit, SimpleForm, TextInput, NumberInput,
} from 'react-admin';
import { EditActions, EntityTitle } from '../utils';

const StoreItemsEdit = (props) => (
  <Edit title={<EntityTitle filedName="name" />} undoable={false} actions={<EditActions />} {...props}>
    <SimpleForm>
      <TextInput source="name" label="Название" />
      <NumberInput source="value" label="Количество" />
      <NumberInput source="max_value" label="Максимальное количество" />
      <NumberInput source="store_id" label="id магазина" />
    </SimpleForm>
  </Edit>
);

export default StoreItemsEdit;
