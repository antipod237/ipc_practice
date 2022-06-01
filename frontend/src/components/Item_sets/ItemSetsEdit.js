import React from 'react';
import {
  Edit, SimpleForm, TextInput, ArrayInput, SimpleFormIterator,
} from 'react-admin';
import { EditActions, EntityTitle } from '../utils';

const ItemSetsEdit = (props) => (
  <Edit title={<EntityTitle filedName="Name" />} undoable={false} actions={<EditActions />} {...props}>
    <SimpleForm>
      <TextInput disabled source="id" label="Идентификатор" />
      <TextInput source="name" label="Название" />
      <ArrayInput source="contract">
        <SimpleFormIterator>
          <TextInput source="contract_id" label="id:" />
        </SimpleFormIterator>
      </ArrayInput>
    </SimpleForm>
  </Edit>
);

export default ItemSetsEdit;
