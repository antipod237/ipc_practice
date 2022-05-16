import React from 'react';
import { List, Datagrid } from 'react-admin';
import OneScreenListActions from './OneScreenListActions';

const OneScreenList = ({
  title,
  empty,
  onRowClick,
  onCreate,
  children,
  ...props
}) => console.log(props) || (
  <List
    title={title}
    empty={empty}
    actions={<OneScreenListActions onClick={onCreate} />}
    {...props}
  >
    <Datagrid
      rowClick={(id, basePath, record) => onRowClick && onRowClick({ id, basePath, record })}
    >
      {children}
    </Datagrid>
  </List>
);

export default OneScreenList;
