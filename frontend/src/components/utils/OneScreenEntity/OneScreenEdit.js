import React from 'react';
import {
  SimpleForm,
  Edit,
} from 'react-admin';
import { makeStyles } from '@material-ui/core/styles';

import OneScreenCreateToolbar from './OneScreenCreateToolbar';
import styles from './style';

const useStyle = makeStyles(styles);

const OneScreenEdit = ({
  onCancel,
  record,
  children,
  ...props
}) => {
  const classes = useStyle();
  return (record && record.id ? (
    <Edit title=" " onSuccess={onCancel} undoable={false} {...props} id={record.id} classes={classes}>
      <SimpleForm toolbar={<OneScreenCreateToolbar onCancel={onCancel} />}>
        {children}
      </SimpleForm>
    </Edit>
  ) : null);
};

export default OneScreenEdit;
