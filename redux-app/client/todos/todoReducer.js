/* @flow */

import Todo from './Todo.js';

export type TodoAppStateType = Array<Todo>;

export function todoReducer(): TodoAppStateType {
  return [
    new Todo({text: 'todo 1'}),
    new Todo({text: 'todo 2'})
  ];
}
