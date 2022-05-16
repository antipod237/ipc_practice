import React from 'react';
import classNames from 'classnames/bind';
import styles from './style.less';

const cx = classNames.bind(styles);

const CustomButton = ({
  onClick,
  variant,
  style,
  children,
}) => (
  <button onClick={onClick} style={style} className={cx(variant, 'Normal')} type="button">{children}</button>
);

export default CustomButton;
