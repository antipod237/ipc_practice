import React from 'react';
import { TopToolbar, ListButton, ShowButton } from 'react-admin';

const EditActions = ({ basePath, data }) => (
  <TopToolbar>
    <ListButton basePath={basePath} label="Список" />
    <ShowButton basePath={basePath} label="Просмотр" record={data} />
  </TopToolbar>
);

export default EditActions;
