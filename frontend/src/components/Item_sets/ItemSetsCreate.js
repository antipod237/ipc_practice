import React from 'react';
import {
  Create, required, SimpleForm, TextInput, ArrayInput, SimpleFormIterator, NumberInput,
} from 'react-admin';

const ItemSetsCreate = (props) => (
  <Create title="Новая номенклатура" {...props}>
    <SimpleForm>
      <TextInput source="name" label="Название" validate={required()} />
      <ArrayInput source="contracts" label="Контракты">
        <SimpleFormIterator>
          <NumberInput source="contract_id" label="id:" />
        </SimpleFormIterator>
      </ArrayInput>
    </SimpleForm>
  </Create>
);

export default ItemSetsCreate;
