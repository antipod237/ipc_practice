import React from 'react';
import Box from '@material-ui/core/Box';
import InboxIcon from '@material-ui/core/SvgIcon/SvgIcon';
import Typography from '@material-ui/core/Typography';
import { useListContext, CreateButton } from 'react-admin';

const Empty = ({ text, hint }) => {
  const { basePath } = useListContext();
  return (
    <Box textAlign="center" m={1}>
      <InboxIcon component="svg" style={{ width: '9em', height: '9em', color: '#8E8E8E' }} />
      <Typography variant="h4" paragraph color="textSecondary" component="div">
        {text}
      </Typography>
      <Typography variant="body1" color="textSecondary" component="div">
        {hint}
      </Typography>
      <CreateButton basePath={basePath} />
    </Box>
  );
};

export default Empty;
