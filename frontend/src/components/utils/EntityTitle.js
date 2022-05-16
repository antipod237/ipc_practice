import React from 'react';

const EntityTitle = ({ filedName, record }) => (
  <span>{record ? record[filedName] : ''}</span>
);

export default EntityTitle;
