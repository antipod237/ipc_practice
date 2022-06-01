import React from 'react';
import {
  Create, required, SimpleForm, TextInput, ArrayInput, SimpleFormIterator, NumberInput,
} from 'react-admin';

const ItemSetsCreate = (props) => (
  <Create title="Новая ноенклатура" {...props}>
    <SimpleForm>
      <TextInput source="name" label="Название" validate={required()} />
      <ArrayInput source="contract" label="Контракты">
        <SimpleFormIterator>
          <NumberInput source="contract_id" />
        </SimpleFormIterator>
      </ArrayInput>
    </SimpleForm>
  </Create>
);

export default ItemSetsCreate;
