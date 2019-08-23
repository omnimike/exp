/* @flow */

import uuid from '../lib/uuid';

export type TodoStateType = 'complete' | 'pending' | 'cancelled';
export type TodoIdType = string;
export type TodoTextType = string;

export default class Todo {
  id: TodoIdType;
  text: TodoTextType;
  status: TodoStateType;

  constructor({
    id = uuid(),
    text = '',
    status = todoStates.PENDING
  }: {
    id?: TodoIdType,
    text?: TodoTextType,
    status?: TodoStateType
  } = {}) {
    this.id = id;
    this.text = text;
    this.status = status;
  }
}

export const todoStates = {
  COMPLETE: 'complete',
  PENDING: 'pending',
  CANCELLED: 'cancelled'
};

