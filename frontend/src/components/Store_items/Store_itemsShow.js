import React from 'react';
import {
  Show, SimpleShowLayout, TextField,
} from 'react-admin';
import { EntityTitle } from '../utils';

const StoreItemsShow = (props) => (
  <Show {...props} title={<EntityTitle filedName="name" />}>
    <SimpleShowLayout>
      <TextField source="id" label="Идентификатор" />
      <TextField source="name" label="Название" />
      <TextField source="value" label="Количество" />
      <TextField source="max_value" label="Максимальное количество" />
      <TextField source="store_id" label="id магазина" />
      <TextField source="remaining_space" label="Свободное место на складе" />
    </SimpleShowLayout>
  </Show>
);

export default StoreItemsShow;
