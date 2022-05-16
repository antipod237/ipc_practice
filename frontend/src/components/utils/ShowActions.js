import React from 'react';
import {
  usePermissions, TopToolbar, ListButton, EditButton,
} from 'react-admin';
import { checkAppAction } from '../../utils';

const ShowActions = ({ basePath, permissionName, data }) => {
  const { loaded, permissions } = usePermissions(`/${permissionName}`);

  return loaded ? (
    <TopToolbar>
      <ListButton basePath={basePath} label="Список" />
      {checkAppAction(permissions.actions, 'update')
        ? <EditButton basePath={basePath} label="Редактировать" record={data} /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

export default ShowActions;
