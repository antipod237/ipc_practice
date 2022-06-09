import React from 'react';
import {
  Show, SimpleShowLayout, TextField, ArrayField, Datagrid,
} from 'react-admin';
import { EntityTitle } from '../utils';

const ItemSetsShow = (props) => (
  <Show {...props} title={<EntityTitle filedName="name" />}>
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Название" />
      <ArrayField source="contracts" label="Контракты">
        <Datagrid>
          <TextField source="contract_id" label="id" />
        </Datagrid>
      </ArrayField>
    </SimpleShowLayout>
  </Show>
);

export default ItemSetsShow;
