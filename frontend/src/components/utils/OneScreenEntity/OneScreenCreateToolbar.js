import React from 'react';
import { Toolbar, SaveButton } from 'react-admin';
import { makeStyles } from '@material-ui/core/styles';
import styles from './style';
import CustomButton from '../CustomButton';

const useStyle = makeStyles(styles);

const OneScreenCreateToolbar = ({ onCancel, ...props }) => {
  const classes = useStyle();
  return (
    <Toolbar className={classes.toolbar} {...props}>
      <SaveButton />
      <CustomButton onClick={onCancel} variant="Dangerous" style={{ marginLeft: '1em' }}>Отмена</CustomButton>
    </Toolbar>
  );
};

export default OneScreenCreateToolbar;
