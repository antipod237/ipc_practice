import React, { useEffect, useState } from 'react';
import { Drawer } from '@material-ui/core';
import { useRefresh, usePermissions } from 'react-admin';
import { checkAppAction } from '../../../utils';

const OneScreenEntity = ({
  List,
  Create,
  Edit,
  permissionName,
  ...props
}) => {
  const [row, setRow] = useState();
  const refresh = useRefresh();

  const { resource } = props;
  const { loaded, permissions } = usePermissions(`/${permissionName || resource}`);

  useEffect(() => {
    refresh();
  }, [row, refresh]);

  return loaded && (
    <>
      <List
        onCreate={checkAppAction(permissions.actions, 'create') && (() => setRow({ id: 'create' }))}
        onRowClick={checkAppAction(permissions.actions, 'update') && setRow}
        {...props}
      />
      <Drawer anchor="right" open={row && row.id === 'create'}>
        <Create onCancel={() => setRow({})} {...props} />
      </Drawer>
      <Drawer anchor="right" open={row && row.id && row.id !== 'create' && row.record}>
        <Edit
          onCancel={() => setRow({})}
          record={row && row.record}
          {...props}
        />
      </Drawer>
    </>
  );
};

export default OneScreenEntity;
