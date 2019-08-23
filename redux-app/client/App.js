/* @flow */

import React from 'react';
import ReactDOM from 'react-dom';
import {createStore} from 'redux';
import {todoReducer} from './todos/todoReducer';
import TodoAppController from './todos/TodoAppController';
import { Provider } from 'react-redux';

export default class App {
  store: any;

  constructor() {
    this.store = createStore(todoReducer);
  }

  init(el: HTMLElement) {
    ReactDOM.render(
      <Provider store={this.store}>
        <TodoAppController state={this.store.getState()} />
      </Provider>,
      el
    );
  }
}

