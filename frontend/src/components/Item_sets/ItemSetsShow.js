import React from 'react';
import {
  Show, SimpleShowLayout, TextField, ArrayField, Datagrid,
} from 'react-admin';

const ItemSetsShow = (props) => (
  <Show {...props} title="Подробнее о номенклатуре">
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
