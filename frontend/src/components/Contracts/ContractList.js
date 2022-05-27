import React from 'react';
import {
  Datagrid, DateField, List, TextField,
} from 'react-admin';

const ContractList = (props) => (
  <List {...props} bulkActionButtons={false} title="Договоры">
    <Datagrid rowClick="show">
      <TextField source="id" label="Идентификатор" />
      <TextField source="number" label="Дело №" />
      <TextField source="supplier_id" label="Id поставщика" />
      <DateField source="start_date" label="Дата подписания договора" />
      <DateField source="end_date" label="Дата окончания договора" />
    </Datagrid>
  </List>
);

export default ContractList;
