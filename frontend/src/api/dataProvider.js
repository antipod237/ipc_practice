/* eslint-disable no-console */
import {
  request,
  prepareFile,
  prepareUrl,
} from './utils';

const flatParams = (params) => {
  let result = {};
  if (!params) {
    return params;
  }
  Object.entries(params).forEach(
    (e) => { result = e[1] instanceof Object ? { ...e[1], ...result } : { ...e, ...result }; },
  );
  return result;
};
export default {
  getList: (resource, params) => request('GET', prepareUrl(`/${resource}/`), flatParams(params))
    .then((resp) => {
      const { total } = resp.data;
      return {
        data: resp.data.items.map((value) => ({
          id: value.id,
          ...value,
        })),
        total,
      };
    }),

  getOne: (resource, params) => request('GET', prepareUrl(`/${resource}/${params.id}`))
    .then((resp) => {
      const { data } = resp;
      return {
        data,
      };
    }),

  getMany: (resource, params) => {
    const query = `?id=[${params.ids.toString()}]`;
    return request('GET', prepareUrl(`/${resource}/${query}`))
      .then((resp) => {
        const { total } = resp.data;
        return {
          data: resp.data.items.map((value) => ({
            id: value.id,
            ...value,
          })),
          total,
        };
      });
  },

  getManyReference: () => {},

  create: (resource, params) => prepareFile(params)
    .then((preparedParams) => request('POST', prepareUrl(`/${resource}/`), preparedParams.data)
      .then((resp) => {
        const { data } = resp;
        return {
          data,
        };
      })),

  update: (resource, params) => prepareFile(params)
    .then((preparedParams) => request('PATCH', prepareUrl(`/${resource}/${preparedParams.id}`, preparedParams.subresource), preparedParams.data)
      .then(() => {
        const data = {
          id: preparedParams.id,
        };
        return {
          data,
        };
      })),

  updateMany: () => {},

  delete: () => {},

  deleteMany: () => {},
};
