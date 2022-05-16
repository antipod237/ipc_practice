import React from 'react';
import {
  Create,
  SimpleForm,
} from 'react-admin';
import { makeStyles } from '@material-ui/core/styles';
import styles from './style';
import OneScreenCreateToolbar from './OneScreenCreateToolbar';

const useStyle = makeStyles(styles);

const OneScreenCreate = ({ onCancel, children, ...props }) => {
  const classes = useStyle();
  return (
    <Create component="div" classes={classes} title="Новый тип баннера" onSuccess={onCancel} {...props}>
      <SimpleForm toolbar={<OneScreenCreateToolbar onCancel={onCancel} />}>
        {children}
      </SimpleForm>
    </Create>
  );
};

export default OneScreenCreate;
