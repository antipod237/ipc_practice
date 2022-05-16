import React from 'react';
import {
  SimpleForm,
  Create,
  TextInput,
  ReferenceInput,
  AutocompleteInput,
} from 'react-admin';

const UserCreate = (props) => (
  <Create title="Новый пользователь" {...props}>
    <SimpleForm>
      <TextInput source="username" label="Логин" />
      <TextInput source="password" label="Пароль" />
      <TextInput source="displayName" label="ФИО" />
      <TextInput source="email" label="Электронная почта" />
      <ReferenceInput source="roleId" reference="roles" label="Роль">
        <AutocompleteInput optionText="displayName" />
      </ReferenceInput>
    </SimpleForm>
  </Create>
);

export default UserCreate;
