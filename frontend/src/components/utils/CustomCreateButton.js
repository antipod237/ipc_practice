import * as React from 'react';
import { Fab, useMediaQuery } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ContentAdd from '@material-ui/icons/Add';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles(
  (theme) => ({
    floating: {
      color: theme.palette.getContrastText(theme.palette.primary.main),
      margin: 0,
      top: 'auto',
      right: 20,
      bottom: 60,
      left: 'auto',
      position: 'fixed',
      zIndex: 1000,
    },
    floatingLink: {
      color: 'inherit',
    },
    button: {
      color: '#3f51b5',
      fontSize: '0.8125rem',
      padding: '4px 5px',
    },
  }),
  { name: 'RaCreateButton' },
);

const defaultIcon = <ContentAdd component="svg" />;

const CustomCreateButton = ({ onClick, ...props }) => {
  const {
    icon = defaultIcon,
    variant,
  } = props;
  const classes = useStyles(props);
  const isSmall = useMediaQuery((theme) => theme.breakpoints.down('sm'));
  return isSmall ? (
    <Fab
      href=""
      onClick={onClick}
      component={Link}
      color="primary"
      className={classes.floating}
      aria-label="Создать"
    >
      {icon}
    </Fab>
  ) : (
    <Button
      href=""
      onClick={onClick}
      className={classes.button}
      variant={variant}
    >
      {icon}
      Создать
    </Button>
  );
};

export default CustomCreateButton;
