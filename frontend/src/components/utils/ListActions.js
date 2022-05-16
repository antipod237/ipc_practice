import React from 'react';
import { usePermissions, TopToolbar, CreateButton } from 'react-admin';
import { checkAppAction } from '../../utils';

const ListActions = ({ basePath, permissionName }) => {
  const { loaded, permissions } = usePermissions(`/${permissionName}`);

  return loaded ? (
    <TopToolbar>
      {checkAppAction(permissions.actions, 'create') ? <CreateButton basePath={basePath} label="Создать" /> : null}
    </TopToolbar>
  ) : <TopToolbar />;
};

export default ListActions;
