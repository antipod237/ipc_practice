import React from 'react';
import { TopToolbar } from 'react-admin';
import CustomCreateButton from '../CustomCreateButton';

const OneScreenListActions = ({ onClick }) => (
  <TopToolbar>
    {onClick && <CustomCreateButton onClick={onClick}>Создать</CustomCreateButton>}
  </TopToolbar>
);

export default OneScreenListActions;
